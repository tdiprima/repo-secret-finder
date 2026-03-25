"""
One class. One job. Hold a single finding.
"""


class Finding:
    """A single thing we found (good or bad)."""

    def __init__(self, level, message):
        """
        level:   "OK", "WARN", or "FAIL"
        message: What we found, in plain English.
        """
        self.level = level
        self.message = message
