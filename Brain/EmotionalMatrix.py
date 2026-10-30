import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "Data", "Config.json")

EMOTION_STATE = {
    "mood": "neutral",
    "frustration_level": 0,
    "last_inputs": []
}


def Analyze_Sentiment(text):
    text = text.lower()

    negative = ["angry", "frustrated", "hate", "stupid", "error", "not working"]
    positive = ["good", "great", "nice", "perfect", "love"]

    score = 0

    for n in negative:
        if n in text:
            score -= 1

    for p in positive:
        if p in text:
            score += 1

    return score


def Update_State(text):
    score = Analyze_Sentiment(text)

    EMOTION_STATE["last_inputs"].append(text)
    EMOTION_STATE["last_inputs"] = EMOTION_STATE["last_inputs"][-5:]

    if score < 0:
        EMOTION_STATE["frustration_level"] += 1
    elif score > 0:
        EMOTION_STATE["frustration_level"] = max(0, EMOTION_STATE["frustration_level"] - 1)

    if EMOTION_STATE["frustration_level"] >= 3:
        EMOTION_STATE["mood"] = "concerned"
    elif score > 0:
        EMOTION_STATE["mood"] = "positive"
    elif score < 0:
        EMOTION_STATE["mood"] = "serious"
    else:
        EMOTION_STATE["mood"] = "neutral"


def Compute_Behavioral_Context(user_query):
    Update_State(user_query)

    mood = EMOTION_STATE["mood"]

    if mood == "concerned":
        return "[TONE: CALM & SUPPORTIVE. User shows repeated frustration.]"
    elif mood == "serious":
        return "[TONE: PROFESSIONAL & PRECISE]"
    elif mood == "positive":
        return "[TONE: LIGHT & ENGAGED]"
    else:
        return "[TONE: STANDARD OPERATION]"