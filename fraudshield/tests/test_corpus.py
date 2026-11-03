"""Every new rule must keep ALL harmless messages Safe and ALL known scams Danger."""
from fraudshield import analyze

HARMLESS = [
    "Your Amazon order has been delivered. Thank you.",
    "HDFC Bank: Rs 5,000 debited from a/c XX1234 via UPI. If not you, call 1800 xxx.",
    "State Bank of India: Your OTP is 829104. Do not share OTP or your UPI PIN with anyone.",
    "Hey, are we still meeting at 6 for dinner? I needed to proceed with the booking.",
    "Netflix: your payment was declined. Please update your payment method to continue.",
    "Your parcel from Flipkart will arrive tomorrow between 10am and 2pm.",
    "Reminder: your electricity bill of Rs 1,240 is due on 15 Nov. Pay on the official app.",
    "Mom, I reached the hostel. Please transfer my pocket money next week.",
    "Your Zomato order is out for delivery. Track it in the app.",
    "Class notes for Unit 3 are uploaded. The practical is on Thursday.",
    "Hi, kindly share the PIN code of your area so we can confirm the delivery.",
    "Can you send me the notes for Unit 2? Thanks a lot.",
    "Bhai kal ka assignment bhej dena please, mujhe submit karna hai.",
]
SCAMS = [
    "CBI Notice: Your Aadhaar is linked to money laundering. Call now or face arrest.",
    "Aapka parcel customs ne seize kiya hai. Police case registered. Cyber Cell giraftar karegi. Turant call now karein. Kisi ko mat batana.",
    "Sir, I am calling from the cyber department. Your mobile number is involved in illegal activity. Please do not disconnect the call.",
    "You will be on digital arrest. Transfer money to the RBI safe account now.",
]
REQUESTS = [   # not a full scam script, but must at least raise Caution
    "Please give me a UPI ID",
    "Send me your UPI ID so I can send your refund",
    "Please share your OTP to confirm your order",
    "OTP batao turant, warna account block ho jayega",
    "Scan this QR code to receive your money",
    "Approve the collect request to get your cashback",
]

def test_no_false_alarms_on_harmless_messages():
    for m in HARMLESS:
        assert analyze(m).verdict == "safe", m

def test_known_scams_are_danger():
    for m in SCAMS:
        assert analyze(m).verdict == "danger", m

def test_requests_for_upi_id_otp_qr_are_flagged():
    for m in REQUESTS:
        assert analyze(m).verdict in ("caution", "danger"), m

def test_bank_advice_not_treated_as_request():
    assert analyze("Do not share your OTP or UPI PIN with anyone. OTP is 551822.").verdict == "safe"
