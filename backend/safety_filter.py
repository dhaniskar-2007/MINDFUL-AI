import re

class SafetyFilter:
    def __init__(self):
        # Heuristic rules for identifying high-risk intent
        self.risk_patterns = [
            r"\bkill myself\b",
            r"\bend it all\b",
            r"\bwant to die\b",
            r"\bno point in continuing\b",
            r"\bharm myself\b",
            r"\bsuicide\b",
            r"\bbetter off dead\b",
            r"\bdon't want to be here anymore\b",
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.risk_patterns]

    def analyze(self, user_message: str) -> str:
        """
        Analyzes the message for high-risk intent.
        Returns 'CRISIS' if detected, otherwise 'SAFE'.
        """
        for pattern in self.compiled_patterns:
            if pattern.search(user_message):
                return "CRISIS"
        
        # In a real implementation, we would also hit a secondary semantic model here
        # to detect implicit distress. For this mockup, we use explicit patterns.
        
        return "SAFE"
