from llm_service import MockLLMService

def test_reflection():
    service = MockLLMService()
    
    test_cases = [
        "I am feeling sad",
        "I feel like my boss hates me",
        "I am struggling with my projects",
        "I'm worried about my future"
    ]
    
    for text in test_cases:
        # Mocking generate_response call with low gravity to trigger reflection
        resp = service.generate_response(text, "LISTENING", {"name": "Neutral"}, [], mode="THERAPIST", current_gravity=0.1)
        print(f"User: {text}")
        print(f"AI:   {resp['text']}")
        print("-" * 20)

if __name__ == "__main__":
    test_reflection()
