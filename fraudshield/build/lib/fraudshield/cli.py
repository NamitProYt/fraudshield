"""Command line: fraudshield check "message"  |  fraudshield check -f msg.txt --report"""
import argparse
import json
import sys

from .rules import analyze
from .report import draft_report

LABEL = {"safe": "SAFE - looks okay",
         "caution": "CAUTION - double-check this",
         "danger": "DANGER - this looks like a scam"}
ADVICE = {"danger": "Police never arrest anyone over a call or video call. "
                    "Do NOT pay or share your UPI PIN. Call 1930.",
          "caution": "Verify directly with your bank or local police before replying.",
          "safe": "No common scam triggers found. Never share your OTP or UPI PIN."}


def main(argv=None):
    p = argparse.ArgumentParser(prog="fraudshield",
                                description="Check a message for digital-arrest / UPI scam patterns.")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("check", help="analyze a message")
    c.add_argument("message", nargs="?", help="message text (or use -f, or pipe via stdin)")
    c.add_argument("-f", "--file", help="read the message from a text file")
    c.add_argument("--report", action="store_true", help="also print a 1930 complaint draft")
    c.add_argument("--json", action="store_true", help="print result as JSON")
    w = sub.add_parser("watch", help="watch the clipboard and warn when you copy a scam message")
    w.add_argument("--no-safe", action="store_true", help="only pop up for caution/danger")
    args = p.parse_args(argv)

    if args.cmd == "watch":
        from .watch import run
        return run(show_safe=not args.no_safe)

    if args.cmd != "check":
        p.print_help()
        return 0

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    elif args.message:
        text = args.message
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        p.error("give a message, -f FILE, or pipe text in")
    if not text.strip():
        p.error("the message is empty")

    res = analyze(text)
    if args.json:
        print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
    else:
        print("[%s]  risk %d/10" % (LABEL[res.verdict], res.score))
        for r in res.reasons:
            print("  - " + r)
        print("\n" + ADVICE[res.verdict])
    if args.report and res.verdict != "safe":
        print("\n" + "=" * 60 + "\n" + draft_report(text, res))
    return 2 if res.verdict == "danger" else 0


if __name__ == "__main__":
    sys.exit(main())
