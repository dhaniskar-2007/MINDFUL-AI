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
        self.distortion_patterns = {
            "Overgeneralization": r"\b(always|never|everyone|nobody|all|none)\b",
            "Catastrophizing": r"\b(ruin|disaster|terrible|horrible|end|worst|failure)\b",
            "Personalization": r"\b(my fault|because of me|i caused)\b"
        }
        self.topic_map = {
            "Work": [r"work", r"job", r"office", r"boss", r"career"],
            "Health": [r"health", r"sleep", r"exercise", r"diet", r"sick"],
            "Relations": [r"friend", r"family", r"partner", r"mom", r"dad", r"people"]
        }
        
    def detect_distortions(self, text: str) -> list:
        found = []
        for name, pattern in self.distortion_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                found.append({"type": name, "text": re.search(pattern, text, re.IGNORECASE).group()})
        return found

    def extract_topics(self, text: str) -> dict:
        found = {}
        for topic, patterns in self.topic_map.items():
            for p in patterns:
                if re.search(p, text, re.IGNORECASE):
                    found[topic] = 0.2 # Impact per mention
        return found

    def generate_response(self, user_message: str, current_state: str, emotion: str, mode: str = "THERAPIST", current_gravity: float = 0.3) -> dict:
        response_text = ""
        new_state = current_state
        distortions = self.detect_distortions(user_message)
        topics = self.extract_topics(user_message)

        # 1. Handle Reflector Mode (Passive)
        if mode == "REFLECTOR":
            response_text = self._get_reflection_response(user_message)
            new_state = "LISTENING"
        
        # 2. Handle Therapist Mode (Active CBT/DBT)
        else:
            # Gravity Alert
            if current_gravity > 0.7 and emotion != "Panic":
                response_text = "I can feel things are getting quite heavy for you right now. Let's take a slow breath together before we dive deeper into this."
                new_state = "LISTENING"
            
            # CBT/DBT Logic
            elif current_state == "CBT_RESTRUCTURING":
                response_text = "That's a helpful perspective. What if we tried to think of one small step you could take today to prepare, rather than focusing on the worst-case scenario?"
                new_state = "LISTENING"
                
            elif current_state == "DBT_GROUNDING":
                 response_text = "Great job. Now, can you listen closely and tell me 4 things you can hear right now?"
                 new_state = "DBT_GROUNDING_STEP_2"
                 
            elif emotion == "Anxious":
                response_text = "It sounds like you're carrying a lot of anxiety right now. "
                if distortions:
                    d = distortions[0]
                    response_text += f"I noticed you used the word '{d['text']}', which might be a bit of '{d['type']}'. Can we look at the evidence together? "
                response_text += "Has there been a time in the past where things didn't end in disaster?"
                new_state = "CBT_RESTRUCTURING"
                
            elif emotion == "Panic":
                response_text = "You're safe right now. I'm here with you. Let's try the 5-4-3-2-1 technique. Can you tell me 5 things you can see?"
                new_state = "DBT_GROUNDING"
            
            else:
                response_text = self._get_reflection_response(user_message)
                new_state = "LISTENING"

        return {
            "text": response_text,
            "state": new_state,
            "detected_emotion": emotion,
            "distortions": distortions,
            "topics": topics
        }

    def _get_reflection_response(self, user_message: str) -> str:
        msg_lower = re.sub(r'[^\w\s]', '', user_message.lower().strip())
        for pattern, response_template in self.reflections:
            match = re.search(pattern, msg_lower)
            if match:
                return response_template.format(*match.groups())
        
        if len(user_message.split()) > 2:
            return f"You mentioned: '{user_message}'. I appreciate you sharing that. What thoughts come to mind when you say that?"
        return "I'm listening. Please continue."

    def get_crisis_response(self) -> str:
        return "I'm hearing that you are feeling an overwhelming amount of pain right now, and I want you to know that you are not alone. Please reach out to someone who can support you. If you are in the US, please call or text 988 to speak with a trained counselor for free."
