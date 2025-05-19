import json
import openai

class InputParserAgent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def parse(self, message: str) -> dict:
        prompt = (
            "You are an assistant that extracts structured data from user messages for a multi-agent real estate chatbot. "
            "Given a message, return a JSON with fields 'intent' and 'parameters'.\n"
            f"Message: {message}\n"
            "JSON:"  # instruct model to output valid JSON
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Extract intent and parameters from a user message."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse LLM output as JSON: {content}")