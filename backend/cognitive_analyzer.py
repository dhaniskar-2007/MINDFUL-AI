import re

class CognitiveAnalyzer:
    def __init__(self):
        # Patterns for common cognitive distortions (CBT framework)
        self.distortion_configs = {
            "Overgeneralization": {
                "pattern": r"\b(always|never|everyone|nobody|all|none|everything|nothing)\b",
                "weight": 0.3
            },
            "Catastrophizing": {
                "pattern": r"\b(ruin|disaster|terrible|horrible|end|worst|failure|catastrophe|unbearable)\b",
                "weight": 0.4
            },
            "Personalization": {
                "pattern": r"\b(my fault|because of me|i caused|i'm to blame|should have known)\b",
                "weight": 0.25
            },
            "All-or-Nothing": {
                "pattern": r"\b(perfect|complete|total|worthless|useless)\b",
                "weight": 0.2
            }
        }

    def analyze(self, user_message: str) -> list:
        """
        Detects cognitive distortions in the message.
        Returns a list of detected distortions with their types and matching text.
        """
        detected = []
        msg_lower = user_message.lower()
        
        for name, config in self.distortion_configs.items():
            match = re.search(config["pattern"], msg_lower, re.IGNORECASE)
            if match:
                detected.append({
                    "type": name,
                    "evidence": match.group(),
                    "weight": config["weight"]
                })
        
        return detected

    def get_cognitive_load(self, distortions: list) -> float:
        """Calculates the total gravity impact from cognitive distortions."""
        if not distortions:
            return 0.0
        
        # Cumulative weight with diminishing returns
        total_weight = 0.0
        for d in distortions:
            total_weight += d["weight"]
            
        return min(0.6, total_weight)
