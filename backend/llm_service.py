import re

class MockLLMService:
    def __init__(self):
        self.reflections = [
            (r"i am feeling (.+)", "I hear that you are feeling {0}. Can you tell me more about what's causing that?"),
            (r"i feel (.+)", "It sounds like you feel {0}. How long have you been feeling this way?"),
            (r"i am (.+)", "Why do you think you are {0}?"),
            (r"i'm (.+)", "You mentioned you're {0}. I'm here to support you through that."),
            (r"my (.+) is (.+)", "I understand your {0} is {1}. How does that affect you?"),
            (r"i have (.+)", "Tell me more about having {0}."),
        ]
        
        self.topic_map = {
            "Work": [r"work", r"job", r"office", r"boss", r"career"],
            "Health": [r"health", r"sleep", r"exercise", r"diet", r"sick"],
            "Relations": [r"friend", r"family", r"partner", r"mom", r"dad", r"people"]
        }

    def extract_topics(self, text: str) -> dict:
        found = {}
        for topic, patterns in self.topic_map.items():
            for p in patterns:
                if re.search(p, text, re.IGNORECASE):
                    found[topic] = 0.2
        return found

    def generate_response(self, user_message: str, current_state: str, emotion_info: dict, distortions: list, mode: str = "THERAPIST", current_gravity: float = 0.3) -> dict:
        response_text = ""
        new_state = current_state
        emotion = emotion_info["name"]
        
        # 🟢 Low Gravity (0.0 - 0.3): Reflection and Awareness
        if current_gravity <= 0.3:
            response_text = self._get_reflection_response(user_message)
            new_state = "LISTENING"

        # 🟡 Moderate Gravity (0.3 - 0.7): CBT-based restructuring
        elif current_gravity < 0.7:
            if distortions:
                d = distortions[0]
                response_text = f"I noticed a pattern of '{d['type']}' in what you said ('{d['evidence']}'). Would you like to try questioning that thought together? What evidence do we have that it's true?"
                new_state = "CBT_RESTRUCTURING"
            elif emotion == "Anxious":
                response_text = "It sounds like anxiety is pulling quite hard right now. Let's try to break down one thing you can control in this situation."
                new_state = "CBT_BREAKDOWN"
            else:
                response_text = "Things are feeling a bit heavy. I'm here to listen, but we could also try a short exercise to lighten the load. What feels most helpful right now?"
                new_state = "RECOVERY_OPTION"

        # 🔴 High Gravity (> 0.7): Immediate grounding and distress tolerance
        else:
            if emotion == "Panic" or current_gravity > 0.85:
                response_text = "Stop for a moment. You're safe. Let's practice the 5-4-3-2-1 grounding technique. Tell me 5 things you see around you right now."
                new_state = "DBT_GROUNDING_5"
            else:
                response_text = "I can feel how much weight you're carrying right now. Let's focus on your breath for just 30 seconds before we talk more. Can you take a slow breath in with me?"
                new_state = "GROUNDING_BREATH"

        return {
            "text": response_text,
            "state": new_state,
            "detected_emotion": emotion,
            "distortions": distortions,
            "topics": self.extract_topics(user_message)
        }

    def _get_reflection_response(self, user_message: str) -> str:
        msg_lower = re.sub(r'[^\w\s]', '', user_message.lower().strip())
        for pattern, response_template in self.reflections:
            match = re.search(pattern, msg_lower)
            if match:
                return response_template.format(*match.groups())
        
        if len(user_message.split()) > 2:
            return f"I appreciate you sharing that. What thoughts come to mind when you process that?"
        return "I'm listening. Please go on."

    def get_crisis_response(self) -> str:
        return "I'm hearing that you are in a lot of pain right now. You are not alone. Please reach out to someone who can help. If you're in the US, call or text 988. I'll stay here with you, but I want to make sure you're safe."
