from fraudshield import analyze, draft_report

CBI = ("CBI Notice: Your Aadhaar is linked to money laundering. An arrest warrant has been "
       "issued. Stay on Skype video call immediately. Transfer verification fee to RBI safe account.")
PARCEL = ("Aapka parcel customs ne seize kiya hai. Police case registered. Cyber Cell giraftar karegi. "
          "Turant call now karein. Kisi ko mat batana.")
OTP = ("State Bank of India: Your OTP for Rs. 4,500 at Amazon is 829104. "
       "Do not share OTP or your UPI PIN with anyone. SBI never calls asking for OTP.")

def test_cbi_is_danger():
    assert analyze(CBI).verdict == "danger"

def test_hinglish_parcel_is_danger():
    assert analyze(PARCEL).verdict == "danger"

def test_real_otp_is_safe():
    r = analyze(OTP)
    assert r.verdict == "safe" and r.score == 1

def test_short_keywords_not_matched_inside_words():
    r = analyze("Your order was delivered and the amount was debited as needed.")
    assert r.verdict == "safe" and r.score == 0

def test_apk_link_flagged():
    assert analyze("Pay your bill: http://x.com/bill.apk").score >= 3

def test_report_contains_message_and_status():
    text = draft_report(CBI)
    assert "1930" in text and "NOT made any payment" in text and "Aadhaar" in text
