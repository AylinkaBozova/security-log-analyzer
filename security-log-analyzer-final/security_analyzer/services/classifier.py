"""Transparent, rule-based log classification for educational use."""
import re

_RULES = (
    ("critical", re.compile(r"ransomware|privilege escalation succeeded|malware confirmed", re.I),
     "A high-impact threat phrase was found. Escalate for analyst review."),
    ("high", re.compile(r"multiple failed logins|brute force|unauthorized admin|account locked", re.I),
     "Repeated authentication failures or privileged-access concerns may be present."),
    ("medium", re.compile(r"failed login|invalid password|suspicious|blocked connection|denied", re.I),
     "The log suggests a failed authentication or blocked activity."),
    ("low", re.compile(r"password changed|new device|policy updated|login from new location", re.I),
     "This account or policy change may deserve a routine review."),
)


def classify_log(line: str) -> tuple[str, str]:
    """Return (severity, explanation), prioritizing the most severe matching rule."""
    for severity, pattern, explanation in _RULES:
        if pattern.search(line):
            return severity, explanation
    return "info", "No demo rule matched. Context and surrounding logs still matter."
