from emotion_detector import EmotionDetector

def test():
    detector = EmotionDetector()
    
    test_cases = [
        "I am feeling very anxious about my presentation.",
        "I can't breathe, my heart is beating so fast, I think I'm dying.",
        "I'm just tired of everything and feel hopeless.",
        "I am really angry at my boss.",
        "I'm doing okay today.",
        "I am anxious and panicking right now." # Overlap case
    ]
    
    for text in test_cases:
        emotion = detector.analyze(text)
        gravity = detector.get_gravity_impact(emotion)
        print(f"Text: {text}")
        print(f"  Emotion: {emotion['name']} (Intensity: {emotion['intensity']})")
        print(f"  Gravity Impact: {gravity:.3f}")
        print("-" * 20)

if __name__ == "__main__":
    test()
