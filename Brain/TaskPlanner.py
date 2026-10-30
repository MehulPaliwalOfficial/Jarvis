import os
import json
from dotenv import load_dotenv
import contextlib

with contextlib.redirect_stderr(open(os.devnull, 'w')):
    import google.generativeai as genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "Data", ".env")
TASK_PATH = os.path.join(BASE_DIR, "Data", "TaskQueue.json")

load_dotenv(ENV_PATH)

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

PLANNER_PROMPT = """
Break user request into structured executable tasks.

Return JSON array ONLY.

Each task must contain:
- task_type
- parameter
- priority (HIGH/MEDIUM/LOW)
- depends_on (list of indexes)

Valid task types:
APP_CONTROL, WEB_SEARCH, MEDIA, WEATHER, EMAIL, WHATSAPP, REMINDER, HARDWARE, CONVERSATION

Rules:
- Must be logically ordered
- Must include dependencies
- Must be executable step-by-step
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=PLANNER_PROMPT,
    generation_config={
        "temperature": 0.2,
        "response_mime_type": "application/json"
    }
)


def Validate(tasks):
    if not isinstance(tasks, list):
        return False

    for t in tasks:
        if "task_type" not in t or "parameter" not in t:
            return False
    return True


def Compile_Task_Graph(query):
    if not GEMINI_KEY:
        return []

    try:
        response = model.generate_content(query)
        tasks = json.loads(response.text)

        if not Validate(tasks):
            return []

        # Add missing defaults safely
        for i, t in enumerate(tasks):
            t.setdefault("priority", "MEDIUM")
            t.setdefault("depends_on", [])

        with open(TASK_PATH, "w") as f:
            json.dump(tasks, f, indent=4)

        return tasks

    except Exception:
        return []