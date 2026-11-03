"""Rule and signature engine (same logic as the FraudShield website)."""
import re
from dataclasses import dataclass, field
from typing import List

# category -> (points, label, keywords)
CATEGORIES = {
    "authority": (2, "Claims government or police authority", [
        "cbi", "ed", "enforcement directorate", "police", "cyber cell",
        "court", "narcotics", "customs", "trai", "rbi", "income tax",
        "cyber crime", "cyber department", "crime branch", "mumbai police"]),
    "personal_hook": (1, "Mentions personal identity or accounts", [
        "aadhaar", "pan", "sim", "parcel", "courier", "fedex",
        "bank account", "mobile number"]),
    "threat": (3, "Threatens arrest, jail, or legal action", [
        "arrest", "warrant", "money laundering", "case registered",
        "fir", "jail", "blocked", "suspended", "giraftar",
        "illegal activity", "legal action", "case darj",
        "digital arrest", "kyc expired", "block ho"]),
    "urgency_secrecy": (2, "Demands immediate action or complete secrecy", [
        "immediately", "call now", "within 24 hours", "turant",
        "do not tell anyone", "don't disconnect", "stay on video call",
        "confidential", "kisi ko mat batana", "do not disconnect", "skype",
        "anydesk", "teamviewer"]),
    "payment": (3, "Asks for money transfer, fee, or payment credentials", [
        "safe account", "verification fee", "processing fee", "transfer money", "transfer funds",
        "transfer the amount", "upi pin",
        "refund", "rbi account"]),
}

# Phrase patterns: catch REQUESTS ("give me a UPI ID", "share your OTP") that single keywords miss.
# category -> (points, label, [regex, ...])
PATTERNS = {
    "credential_request": (3, "Asks you to share an OTP, PIN, CVV or password", [
        r"\b(give|send|share|tell|provide|read out|bhejo|batao)\b[^.\n]{0,30}\b(otp|cvv|password|pin\b(?!\s*code))",
        r"\b(otp|cvv|pin)\b[^.\n]{0,15}\b(batao|bhejo|bata do|bhej do|dedo|de do)\b",
        r"\byour (card number|cvv)\b"]),
    "upi_request": (3, "Asks for your UPI ID or tells you to scan a QR / approve a payment request", [
        r"\b(give|send|share|tell|provide)\b[^.\n]{0,30}\bupi\s*id\b",
        r"\bscan\b[^.\n]{0,15}\bqr\b",
        r"\b(approve|accept)\b[^.\n]{0,20}\b(collect|payment) request\b"]),
}

_ADVICE = re.compile(r"(do not|don't|never)\s+(share|give|tell|reveal)[^.\n]*[.\n]?")
_SHORT_LINK = re.compile(r"(bit\.ly|tinyurl\.com|is\.gd|cutt\.ly|(^|[^a-z0-9.-])t\.co)/")


@dataclass
class Result:
    score: int
    verdict: str                      # "safe" | "caution" | "danger"
    reasons: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    matches: dict = field(default_factory=dict)

    def to_dict(self):
        return {"score": self.score, "verdict": self.verdict,
                "reasons": self.reasons, "categories": self.categories,
                "matches": self.matches}


def _match(text, kw):
    """Whole-word for short keywords, word-start for longer ones."""
    esc = re.escape(kw)
    if len(kw) <= 4:
        pat = r"(^|[^a-z0-9])" + esc + r"($|[^a-z0-9])"
    else:
        pat = r"(^|[^a-z0-9])" + esc
    return re.search(pat, text) is not None


def analyze(message: str) -> Result:
    lower = message.lower()
    scan = _ADVICE.sub(" ", lower)   # ignore "do not share OTP/UPI PIN" advice

    score, found, reasons, matches = 0, [], [], {}
    for name, (points, label, kws) in CATEGORIES.items():
        hit = [k for k in kws if _match(scan, k)]
        if hit:
            score += points
            found.append(name)
            matches[name] = hit
            reasons.append("%s (%s)" % (label, ", ".join(hit[:3])))

    for name, (points, label, patterns) in PATTERNS.items():
        hit = [m.group(0).strip() for pat in patterns for m in [re.search(pat, scan)] if m]
        if hit:
            score += points
            found.append(name)
            matches[name] = hit
            reasons.append("%s (%s)" % (label, hit[0][:40]))

    if ".apk" in lower:
        score += 3
        reasons.append("Contains an .apk download link (can steal SMS and OTPs)")
    elif _SHORT_LINK.search(lower):
        score += 1
        reasons.append("Contains a shortened link that hides the real website")

    if "authority" in found and "threat" in found:
        score += 2
        reasons.append("Law-enforcement name + arrest threat: the digital arrest signature")

    has_otp = "otp" in lower or "one time password" in lower or "do not share" in lower
    if has_otp and not ({"threat", "payment", "authority", "credential_request", "upi_request"} & set(found)):
        score = 1

    score = min(10, score)
    verdict = "danger" if score >= 7 else "caution" if score >= 3 else "safe"
    if verdict == "safe":
        reasons = []
    return Result(score, verdict, reasons, found, matches)
