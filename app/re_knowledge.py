import openai
class REKnowledgeAgent:
    def __init__(self, model: str = "gpt-4"):
        self.model = model

    def explain_term(self, term: str) -> str:
        prompt = (
            f"You are a real estate investment expert. "
            f"Please explain the term '{term}' in clear, concise language. "
            "If the term is not related to real estate investing, respond exactly with: "
            "'I'm sorry, I can only answer real estate-related questions.'"
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful real estate investment expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()

    def answer_question(self, question: str) -> str:
        prompt = (
            "You are a knowledgeable real estate investment advisor. "
            f"Answer the following question thoroughly: '{question}'. "
            "If the question is not related to real estate investing, respond exactly with: "
            "'I'm sorry, I can only answer real estate-related questions.'"
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful real estate investment expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
