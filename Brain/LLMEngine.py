from openai import OpenAI
from Core.Config import Config


class LLMEngine:
    def __init__(self, model="gpt-4o-mini"):
        self.api_key = Config.OPENAI_API_KEY
        self.model = model

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt, system="You are Jarvis, an advanced AI system."):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"[LLM ERROR]: {str(e)}"