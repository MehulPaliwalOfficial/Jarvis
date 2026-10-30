import json
import time
import threading
from datetime import datetime

TASKS_FILE = "Data/Tasks.json"


# -------------------------
# FILE HANDLING
# -------------------------

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            if "reminders" not in data:
                data["reminders"] = []
            return data
    except:
        return {"reminders": []}


def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------
# TRIGGER SYSTEM
# -------------------------

def trigger_reminder(reminder):
    text = reminder.get("text", "Reminder")
    print(f"\n🔔 REMINDER: {text}\n")


# -------------------------
# MAIN LOOP
# -------------------------

def scheduler_loop():
    while True:
        data = load_tasks()
        now = datetime.now()
        updated = False

        for r in data["reminders"]:

            # Fix old data automatically
            if "done" not in r:
                r["done"] = False
                updated = True

            if "text" not in r and "task" in r:
                r["text"] = r["task"]
                updated = True

            if r.get("done"):
                continue

            if "time" not in r:
                continue

            try:
                reminder_time = datetime.strptime(
                    r["time"], "%Y-%m-%d %H:%M:%S"
                )
            except:
                continue

            if now >= reminder_time:
                trigger_reminder(r)
                r["done"] = True
                updated = True

        if updated:
            save_tasks(data)

        time.sleep(2)


# -------------------------
# START FUNCTION
# -------------------------

def start_scheduler():
    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True
    )
    thread.start()