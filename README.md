# FraudShield India

![tests](../../actions/workflows/tests.yml/badge.svg)

Open-source scanner for "digital arrest" and UPI scam messages. Runs fully offline,
stores nothing, and drafts a ready-to-file complaint for the **1930** helpline.
Team Quad Core · MAIT Delhi · Hack the Circle 2026

**Live site:** https://fraudshield-india.ai.studio/  
**Download (Windows):** https://github.com/NamitProYt/fraudshield/releases/latest/download/fraudshield-package.zip

## Quick install on Windows (no commands)
1. Install Python from python.org (tick **Add python.exe to PATH**).
2. Click **Code -> Download ZIP** on GitHub (or use the download link above) and **Extract All**.
3. Double-click **install-windows.bat**. It installs FraudShield and starts the Guardian.
   Next time, double-click **run-guardian-windows.bat**.

## Install
```bash
pip install .                                        # from this folder
# or
pip install git+https://github.com/NamitProYt/fraudshield
```

## Use
```bash
fraudshield check "CBI Notice: Your Aadhaar is linked to money laundering. Call now or face arrest."
fraudshield check -f message.txt --report     # also prints the 1930 complaint draft
fraudshield check "..." --json
```
```python
from fraudshield import analyze, draft_report
r = analyze("CBI Notice: ... arrest ...")
print(r.verdict, r.score, r.reasons)
print(draft_report("..."))
```

## Guardian mode (laptop integration)
```bash
fraudshield watch
```
Leave it running. Whenever you copy a message (WhatsApp Web/Desktop, email, Telegram...),
a pop-up on your screen shows Safe / Caution / High risk with reasons, and a
**Copy 1930 report** button. Runs fully on your laptop; nothing is stored or sent.

## How it works
Rule and signature engine: weighted categories (fake authority, personal hook, threat,
urgency/secrecy, payment ask, risky links). A DistilBERT urgency/coercion model is the planned next engine.

## Test
```bash
pip install pytest && pytest
```
Prototype: results are guidance, not legal advice. MIT licensed.
