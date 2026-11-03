"""Draft a complaint text for the 1930 helpline / cybercrime.gov.in."""
from datetime import datetime
from .rules import analyze, Result


def draft_report(message: str, result: Result = None) -> str:
    result = result or analyze(message)
    authority = result.matches.get("authority")
    claimed = ", ".join(a.upper() for a in authority) if authority else "an unknown sender"
    flags = "\n".join("- " + r for r in result.reasons) or "- Suspicious urgency and extortion request."
    when = datetime.now().strftime("%d %b %Y, %H:%M")
    return (
        "COMPLAINT DRAFT FOR CYBERCRIME HELPLINE 1930 / CYBERCRIME.GOV.IN\n"
        "Date & Time: %s\n\n"
        "INCIDENT SUMMARY:\n"
        "I received a suspicious message claiming to be from %s. The sender tried to "
        "intimidate me with false allegations and unlawful demands.\n\n"
        "SUSPICIOUS MESSAGE RECEIVED:\n\"%s\"\n\n"
        "RED FLAGS DETECTED:\n%s\n\n"
        "CURRENT STATUS:\n"
        "I have NOT made any payment or shared my banking credentials / UPI PIN. "
        "I request investigation and blocking of the sender's contact details.\n"
    ) % (when, claimed, message.strip(), flags)
