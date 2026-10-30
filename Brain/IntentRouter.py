import os
import json
import contextlib
from dotenv import load_dotenv

with contextlib.redirect_stderr(open(os.devnull, 'w')):
    import google.generativeai as genai

# =========================
# 📁 ENV SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "Data", ".env")
load_dotenv(ENV_PATH)

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# =========================
# 🧠 PROMPT
# =========================
ROUTER_PROMPT = """
You are an intent classification engine.

Return ONLY valid JSON.

Detect:
1. Intents
2. Entities (city, app, song, person, etc.)

Allowed intents:
APP_CONTROL, WEB_SEARCH, MEDIA, WEATHER, HARDWARE,
EMAIL, WHATSAPP, REMINDER, CONVERSATION

Return format:
{
  "intents": [
    {
      "intent": "TYPE",
      "confidence": 0.0-1.0,
      "entities": {}
    }
  ]
}
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=ROUTER_PROMPT,
    generation_config={
        "temperature": 0.0,
        "response_mime_type": "application/json"
    }
)

# =========================
# 🧹 NORMALIZE
# =========================
def Normalize_Text(text):
    return text.lower().strip()

# =========================
# 🔁 FALLBACK
# =========================
def Rule_Based_Fallback(text):
    text = Normalize_Text(text)
    intents = []

    if any(x in text for x in ["open", "launch", "start"]):
        intents.append({"intent": "APP_CONTROL", "confidence": 0.7, "entities": {}})

    if any(x in text for x in ["play", "song", "music", "youtube"]):
        intents.append({"intent": "MEDIA", "confidence": 0.75, "entities": {}})

    if any(x in text for x in ["weather", "temperature"]):
        intents.append({"intent": "WEATHER", "confidence": 0.8, "entities": {}})

    if any(x in text for x in ["battery", "cpu", "ram", "system"]):
        intents.append({"intent": "HARDWARE", "confidence": 0.8, "entities": {}})

    if any(x in text for x in ["email", "mail"]):
        intents.append({"intent": "EMAIL", "confidence": 0.75, "entities": {}})

    if any(x in text for x in ["whatsapp", "message"]):
        intents.append({"intent": "WHATSAPP", "confidence": 0.75, "entities": {}})

    if any(x in text for x in ["remind", "reminder"]):
        intents.append({"intent": "REMINDER", "confidence": 0.75, "entities": {}})

    if not intents:
        intents.append({"intent": "CONVERSATION", "confidence": 0.6, "entities": {}})

    return {"intents": intents}

# =========================
# 🏆 FINALIZER
# =========================
def Finalize_Output(data):
    intents = data.get("intents", [])

    # Safety fallback
    if not intents:
        return Rule_Based_Fallback("")

    # Ensure structure
    for item in intents:
        item.setdefault("intent", "CONVERSATION")
        item.setdefault("confidence", 0.5)
        item.setdefault("entities", {})

    # Sort by confidence
    intents = sorted(intents, key=lambda x: x["confidence"], reverse=True)

    return {
        "primary_intent": intents[0]["intent"],
        "intents": intents
    }

# =========================
# 🧠 ROUTER
# =========================
def Route_Intent(user_query):
    query = Normalize_Text(user_query)

    if not GEMINI_KEY:
        return Finalize_Output(Rule_Based_Fallback(query))

    try:
        response = model.generate_content(query)
        data = json.loads(response.text)

        if "intents" not in data:
            return Finalize_Output(Rule_Based_Fallback(query))

        return Finalize_Output(data)

    except Exception as e:
        print(f"[IntentRouter ERROR]: {e}")
        return Finalize_Output(Rule_Based_Fallback(query))