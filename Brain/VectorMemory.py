import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(BASE_DIR, "Data", "Memory.json")


def load():
    if not os.path.exists(FILE):
        return {"memory": []}

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add(text):
    data = load()
    data["memory"].append({
        "text": text,
        "time": str(datetime.now())
    })
    save(data)