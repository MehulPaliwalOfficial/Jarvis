import os
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# 📁 LOAD ENV
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "Data", ".env"))

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# =========================
# 🧠 MODEL CONFIG
# =========================
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are JARVIS.

Behavior Rules:
- Be precise, calm, intelligent
- Speak like an assistant, not a chatbot
- Keep responses short unless asked to elaborate
- If unsure, say so clearly
- Prefer structured thinking
"""
)

chat = model.start_chat(history=[])

# =========================
# 🧠 MEMORY (LIGHT CONTEXT)
# =========================
last_user_query = ""
last_ai_response = ""


# =========================
# 🧠 DECISION ENGINE
# =========================
def should_use_ai(query: str) -> bool:
    """
    Decide whether to use AI or not.
    """
    q = query.lower()

    # If it's a known command → don't use AI
    blocked_keywords = [
        "open", "play", "search", "weather",
        "news", "stock", "volume", "system"
    ]

    if any(word in q for word in blocked_keywords):
        return False

    return True


# =========================
# 🧠 RESPONSE ENGINE
# =========================
def Compute_AI_Response(query: str):
    global last_user_query, last_ai_response

    if not GEMINI_KEY:
        return "API key missing, Sir."

    try:
        response = chat.send_message(query).text.strip()

        # Store memory
        last_user_query = query
        last_ai_response = response

        return response

    except Exception as e:
        return f"AI Error: {e}"


# =========================
# 🧠 SMART BRAIN ENTRY
# =========================
def Think(query: str):
    """
    Main brain thinking function.
    This decides whether to use AI or not.
    """

    # Decide
    if should_use_ai(query):
        return Compute_AI_Response(query)

    # If not AI → return signal to main.py
    return None


# =========================
# 🧪 TEST MODE
# =========================
if __name__ == "__main__":
    while True:
        q = input("💬 You: ")
        print("🤖:", Think(q))