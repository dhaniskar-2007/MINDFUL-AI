import re

class EmotionDetector:
    def __init__(self):
        # Expanded emotion mapping with keywords and associated intensity (1-10)
        self.emotion_configs = {
            "Anxious": {
                "patterns": [r"\bpresentation\b", r"\bruin it\b", r"\bnervous\b", r"\banxious\b", r"\bworried\b", r"\bfret\b", r"\btense\b"],
                "intensity": 4,
                "gravity": 0.15
            },
            "Panic": {
                "patterns": [r"\bheart is beating\b", r"\bcan't breathe\b", r"\bspinning\b", r"\bpanic\b", r"\boverwhelmed\b", r"\bsuffocating\b", r"\bdying\b"],
                "intensity": 9,
                "gravity": 0.4
            },
            "Despair": {
                "patterns": [r"\btired of everything\b", r"\bhopeless\b", r"\bsad\b", r"\bpointless\b", r"\bgive up\b", r"\bdarkness\b", r"\bmiserable\b"],
                "intensity": 8,
                "gravity": 0.35
            },
            "Anger": {
                "patterns": [r"\bangry\b", r"\bfurious\b", r"\bhate\b", r"\bannoyed\b", r"\birritated\b", r"\bmad\b"],
                "intensity": 6,
                "gravity": 0.2
            },
            "Neutral": {
                "patterns": [],
                "intensity": 1,
                "gravity": -0.05
            }
        }

    def analyze(self, user_message: str) -> dict:
        """
        Classifies the emotion and intensity.
        Returns a dict with emotion name and intensity.
        """
        msg_lower = user_message.lower()
        
        for emotion, config in self.emotion_configs.items():
            if emotion == "Neutral": continue
            for pattern in config["patterns"]:
                if re.search(pattern, msg_lower, re.IGNORECASE):
                    # Check for intensifiers
                    intensity = config["intensity"]
                    if re.search(r"\b(very|extremely|really|so|too)\b", msg_lower):
                        intensity = min(10, intensity + 2)
                    
                    return {"name": emotion, "intensity": intensity}
                    
        return {"name": "Neutral", "intensity": 1}

    def get_gravity_impact(self, emotion_info: dict) -> float:
        """Returns how much the current message adds to the 'heaviness' score."""
        name = emotion_info["name"]
        intensity = emotion_info["intensity"]
        
        base_gravity = self.emotion_configs.get(name, self.emotion_configs["Neutral"])["gravity"]
        
        # Scale gravity by intensity (intensity 1-10)
        # For Neutral, intensity is 1, so it stays -0.05
        # For others, we scale the base impact
        if name == "Neutral":
            return base_gravity
        
        # Intensity scaling: 4/5 is baseline. 10 is 2x impact. 1 is 0.25x impact.
        multiplier = intensity / 5.0
        return base_gravity * multiplier
