import re

def Sanitize(text):
    if not text:
        return ""

    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = text.replace("*", "")
    text = re.sub(r"\s+", " ", text).strip()

    return text