import re

class EmotionDetector:
    def __init__(self):
        # Very simple mocked keyword mapping for the demonstration
        self.emotion_map = {
            "Anxious": [
                r"\bpresentation\b", r"\bruin it\b", r"\bnervous\b", r"\banxious\b", r"\bworried\b"
            ],
            "Panic": [
                r"\bheart is beating\b", r"\bcan't breathe\b", r"\bspinning\b", r"\bpanic\b", r"\boverwhelmed\b"
            ],
            "Despair": [
                r"\btired of everything\b", r"\bhopeless\b", r"\bsad\b", r"\bpointless\b"
            ]
        }

    def analyze(self, user_message: str) -> str:
        """
        Classifies the emotion based on simple heuristics for the POC.
        In a real application, this would invoke a model like DistilRoBERTa.
        """
        msg_lower = user_message.lower()
        
        for emotion, patterns in self.emotion_map.items():
            for pattern in patterns:
                if re.search(pattern, msg_lower, re.IGNORECASE):
                    return emotion
                    
        return "Neutral"

    def get_gravity_impact(self, emotion: str) -> float:
        """Returns how much the current message adds to the 'heaviness' score."""
        impact_map = {
            "Panic": 0.4,
            "Despair": 0.3,
            "Anxious": 0.15,
            "Neutral": -0.05 # Gradual recovery
        }
        return impact_map.get(emotion, 0.0)
