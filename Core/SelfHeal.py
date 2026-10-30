import os
import sys
import json
import importlib
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_PATH = os.path.join(BASE_DIR, "Logs", "Diagnostics.log")
CONFIG_PATH = os.path.join(BASE_DIR, "Data", "Config.json")

logging.basicConfig(filename=LOG_PATH, level=logging.ERROR)

def fix_config():
    default = {
        "assistant_name": "JARVIS",
        "user_name": "Sir",
        "cpu_limit": 85
    }

    try:
        if not os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as f:
                json.dump(default, f, indent=4)
            return "Config restored."

        with open(CONFIG_PATH, "r") as f:
            json.load(f)

    except:
        with open(CONFIG_PATH, "w") as f:
            json.dump(default, f, indent=4)
        return "Config repaired."

    return None


def reload_module(module_name):
    try:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
            return True
        return False
    except Exception as e:
        logging.error(str(e))
        return False


def run_self_check():
    result = fix_config()
    return result if result else "System stable."