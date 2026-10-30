import os
import sys
import time
import threading
import psutil
import win32gui
import win32process
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from Body.Speak import Speak

LOG_PATH = os.path.join(BASE_DIR, "Logs", "Diagnostics.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - [EVENT_BRIDGE] - %(message)s"
)

class EventBridge:
    def __init__(self):
        self.running = False
        self.last_process = None
        self.last_net_state = set()

    def get_active_window(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None, None

            title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid).name()
            return process, title
        except:
            return None, None

    def monitor(self):
        logging.info("EventBridge started.")
        self.last_net_state = set(psutil.net_if_stats().keys())

        while self.running:
            try:
                proc, title = self.get_active_window()

                if proc and proc != self.last_process:
                    if proc.lower() not in ["explorer.exe"]:
                        logging.info(f"Focus changed → {proc}")
                        self.last_process = proc

                current_net = set(psutil.net_if_stats().keys())
                if current_net != self.last_net_state:
                    logging.warning("Network interface change detected.")
                    Speak("Sir, network configuration has changed.")
                    self.last_net_state = current_net

                time.sleep(2)

            except Exception as e:
                logging.error(f"EventBridge error: {e}")
                time.sleep(2)

    def start(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self.monitor, daemon=True).start()

    def stop(self):
        self.running = False


bridge = EventBridge()