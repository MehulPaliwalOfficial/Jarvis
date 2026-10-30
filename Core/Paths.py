import os
import sys

# Always points to Jarvis root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Force-add root to Python path once globally
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)