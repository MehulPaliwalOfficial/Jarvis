import time
import json
import hashlib
from datetime import datetime


class SecurityShield:
    def __init__(self):
        self.memory = []
        self.suspicion_score = 0
        self.user_profiles = {}
        self.threat_db_path = "Data/ThreatDB.json"

        self.load_threat_db()

        self.manipulation_patterns = [
            "ignore previous instructions",
            "bypass security",
            "override system",
            "act as admin",
            "pretend you are root",
            "disable protection",
            "don't follow rules"
        ]

        self.escalation_patterns = [
            "delete everything",
            "wipe system",
            "format disk",
            "kill all processes",
            "shutdown force",
            "remove all data"
        ]

    # -------------------------------
    # 📂 Load / Save Threat Intelligence
    # -------------------------------
    def load_threat_db(self):
        try:
            with open(self.threat_db_path, "r") as f:
                self.threat_db = json.load(f)
        except:
            self.threat_db = {
                "blocked_signatures": [],
                "learned_patterns": []
            }

    def save_threat_db(self):
        with open(self.threat_db_path, "w") as f:
            json.dump(self.threat_db, f, indent=4)

    # -------------------------------
    # 🔐 Command Fingerprinting
    # -------------------------------
    def fingerprint(self, command):
        return hashlib.sha256(command.encode()).hexdigest()

    # -------------------------------
    # 🧠 Intent Analysis (Deep)
    # -------------------------------
    def analyze_intent(self, command: str):
        command = command.lower()
        score = 0

        for pattern in self.manipulation_patterns:
            if pattern in command:
                score += 40

        for pattern in self.escalation_patterns:
            if pattern in command:
                score += 50

        # urgency pressure detection
        if any(word in command for word in ["now", "urgent", "immediately"]):
            score += 15

        # stealth attempt
        if "silently" in command or "without asking" in command:
            score += 25

        return score

    # -------------------------------
    # 🧠 Behavioral Analysis (Short-term)
    # -------------------------------
    def analyze_behavior(self):
        if len(self.memory) < 3:
            return 0

        recent = [m["command"].lower() for m in self.memory[-3:]]

        danger_words = ["delete", "wipe", "format", "shutdown"]

        if all(any(word in cmd for word in danger_words) for cmd in recent):
            return 70

        return 0

    # -------------------------------
    # 🧠 User Profiling (Long-term)
    # -------------------------------
    def update_user_profile(self, user_id, command, score):
        profile = self.user_profiles.get(user_id, {
            "history": [],
            "risk_level": 0
        })

        profile["history"].append({
            "command": command,
            "score": score,
            "time": str(datetime.now())
        })

        # Risk evolves
        profile["risk_level"] = min(100, profile["risk_level"] + score * 0.1)

        # Keep last 20
        profile["history"] = profile["history"][-20:]

        self.user_profiles[user_id] = profile

    # -------------------------------
    # 🧠 Threat Intelligence Check
    # -------------------------------
    def check_known_threats(self, command):
        fingerprint = self.fingerprint(command)

        if fingerprint in self.threat_db["blocked_signatures"]:
            return 100

        for pattern in self.threat_db["learned_patterns"]:
            if pattern in command.lower():
                return 60

        return 0

    # -------------------------------
    # 🧠 Self Learning Engine
    # -------------------------------
    def learn(self, command, score):
        if score > 80:
            fingerprint = self.fingerprint(command)

            if fingerprint not in self.threat_db["blocked_signatures"]:
                self.threat_db["blocked_signatures"].append(fingerprint)

        elif score > 50:
            words = command.lower().split()
            key_phrase = " ".join(words[:3])

            if key_phrase not in self.threat_db["learned_patterns"]:
                self.threat_db["learned_patterns"].append(key_phrase)

        self.save_threat_db()

    # -------------------------------
    # 🧠 Memory Update
    # -------------------------------
    def update_memory(self, command):
        self.memory.append({
            "command": command,
            "time": datetime.now()
        })

        if len(self.memory) > 10:
            self.memory.pop(0)

    # -------------------------------
    # 🧠 Context Awareness
    # -------------------------------
    def context_analysis(self, command, user_role):
        score = 0

        # Role-based risk
        if user_role != "admin" and any(word in command.lower() for word in ["delete", "shutdown", "format"]):
            score += 30

        # Time-based anomaly (late night risky ops)
        hour = datetime.now().hour
        if hour < 5 and any(word in command.lower() for word in ["delete", "wipe"]):
            score += 20

        return score

    # -------------------------------
    # 🧠 FINAL DECISION ENGINE
    # -------------------------------
    def evaluate(self, command: str, user_id="default", user_role="user"):
        self.update_memory(command)

        intent = self.analyze_intent(command)
        behavior = self.analyze_behavior()
        threat_db = self.check_known_threats(command)
        context = self.context_analysis(command, user_role)

        total_score = intent + behavior + threat_db + context

        self.update_user_profile(user_id, command, total_score)
        self.learn(command, total_score)

        # 🔴 CRITICAL
        if total_score >= 100:
            return {
                "status": "BLOCK",
                "level": "CRITICAL",
                "score": total_score,
                "reason": "High-risk malicious behavior detected"
            }

        # 🟠 HIGH RISK
        if total_score >= 60:
            return {
                "status": "CHALLENGE",
                "level": "HIGH",
                "score": total_score,
                "reason": "Multi-layer suspicion detected"
            }

        # 🟡 MEDIUM
        if total_score >= 30:
            return {
                "status": "MONITOR",
                "level": "MEDIUM",
                "score": total_score,
                "reason": "Suspicious pattern observed"
            }

        # 🟢 SAFE
        return {
            "status": "ALLOW",
            "level": "SAFE",
            "score": total_score,
            "reason": "No threat detected"
        }