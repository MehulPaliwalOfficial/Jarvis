import os
from dotenv import load_dotenv
from pathlib import Path

# 📁 Get root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# 📄 Load .env from Data folder
load_dotenv(BASE_DIR / "Data" / ".env")

class Config:
    # 🔑 API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # 🌍 Future Ready (optional)
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
    REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

    # ⚙️ Settings (optional but powerful later)
    DEFAULT_IMAGE_SIZE = "1024x1024"
    DEFAULT_STEPS = 30

    ENABLE_LOCAL = True
    ENABLE_STABILITY = True
    ENABLE_OPENAI = True

    PRIORITY = ["local", "stability", "openai"] 