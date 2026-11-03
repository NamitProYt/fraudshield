"""FraudShield India: spot 'digital arrest' and UPI scam messages."""
from .rules import analyze, Result
from .report import draft_report

__all__ = ["analyze", "Result", "draft_report"]
__version__ = "0.2.1"
