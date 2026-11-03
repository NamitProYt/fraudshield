"""FraudShield Guardian: watches your clipboard and warns you BEFORE you reply or pay.

Copy any suspicious message (WhatsApp Web/Desktop, SMS-to-PC, email, Telegram...)
and a pop-up appears instantly. Everything runs on this laptop; nothing is stored or sent.
Uses only Python's built-in tkinter, so there is nothing extra to install.
"""
import sys

try:
    import tkinter as tk
except ImportError:          # pragma: no cover
    tk = None

from .rules import analyze
from .report import draft_report

MIN_LEN = 15
STYLE = {   # background, accent, title
    "danger": ("#F9D5CF", "#E5604D", "HIGH RISK: this looks like a scam"),
    "caution": ("#FCE9C6", "#F0A73A", "CAUTION: double-check this"),
    "safe": ("#D6EEEA", "#2A9D9D", "Looks okay"),
}
ADVICE = {
    "danger": "Police never arrest anyone over a call or video call.\nDo NOT pay or share your UPI PIN. Call 1930.",
    "caution": "Verify directly with your bank or local police before replying.",
    "safe": "No common scam triggers found.",
}
NAVY = "#1F3A4D"


class Guardian:
    def __init__(self, interval_ms=600, show_safe=True):
        if tk is None:
            raise RuntimeError("tkinter is not available. Re-install Python from python.org (it includes tkinter).")
        self.root = tk.Tk()
        self.root.withdraw()
        self.interval = interval_ms
        self.show_safe = show_safe
        self.popup = None
        self.last = self._read()      # ignore whatever is already on the clipboard

    def _read(self):
        try:
            return self.root.clipboard_get()
        except tk.TclError:
            return ""

    def check_once(self):
        """Look at the clipboard once. Returns the Result if a new message was analyzed."""
        text = self._read()
        if not text or text == self.last:
            return None
        self.last = text
        if len(text.strip()) < MIN_LEN:
            return None
        res = analyze(text)
        print("[%s] risk %d/10  %s" % (res.verdict.upper(), res.score, text.strip()[:60].replace("\n", " ")))
        for r in res.reasons:
            print("   - " + r)
        if res.verdict != "safe" or self.show_safe:
            self._show(text, res)
        return res

    def _show(self, text, res):
        if self.popup is not None:
            try:
                self.popup.destroy()
            except tk.TclError:
                pass
        bg, accent, title = STYLE[res.verdict]
        win = tk.Toplevel(self.root)
        self.popup = win
        win.title("FraudShield India")
        win.configure(bg=accent, padx=3, pady=3)
        win.attributes("-topmost", True)
        win.bind("<Escape>", lambda e: win.destroy())

        body = tk.Frame(win, bg=bg, padx=16, pady=14)
        body.pack(fill="both", expand=True)
        tk.Label(body, text="FraudShield India  |  risk %d/10" % res.score, bg=bg, fg=NAVY,
                 font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(body, text=title, bg=bg, fg=NAVY, font=("Georgia", 14, "bold"),
                 wraplength=360, justify="left").pack(anchor="w", pady=(2, 6))
        for r in res.reasons[:4]:
            tk.Label(body, text="- " + r, bg=bg, fg=NAVY, font=("Segoe UI", 10),
                     wraplength=360, justify="left").pack(anchor="w")
        tk.Label(body, text=ADVICE[res.verdict], bg=bg, fg=NAVY, font=("Segoe UI", 10, "bold"),
                 wraplength=360, justify="left").pack(anchor="w", pady=(8, 8))

        if res.verdict != "safe":
            row = tk.Frame(body, bg=bg)
            row.pack(anchor="w")
            tk.Button(row, text="Copy 1930 report", bg=NAVY, fg="white", relief="flat", padx=10,
                      command=lambda: self._copy_report(text, res, win)).pack(side="left", padx=(0, 8))
            tk.Button(row, text="Dismiss", relief="flat", padx=10, command=win.destroy).pack(side="left")
        else:
            win.after(3000, lambda: win.winfo_exists() and win.destroy())

        win.update_idletasks()
        w, h = win.winfo_reqwidth(), win.winfo_reqheight()
        x = win.winfo_screenwidth() - w - 24
        y = win.winfo_screenheight() - h - 80
        win.geometry("+%d+%d" % (x, y))

    def _copy_report(self, text, res, win):
        report = draft_report(text, res)
        self.root.clipboard_clear()
        self.root.clipboard_append(report)
        self.root.update()
        self.last = report            # do not re-analyze our own report
        print("1930 complaint draft copied to clipboard. Paste it into cybercrime.gov.in")
        win.destroy()

    def _tick(self):
        self.check_once()
        self.root.after(self.interval, self._tick)

    def run(self):
        print("FraudShield Guardian is running. Copy any message to check it. Ctrl+C to stop.")
        self._tick()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


def run(show_safe=True):
    try:
        Guardian(show_safe=show_safe).run()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0
