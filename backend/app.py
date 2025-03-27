import openai
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

conversations = {}

def generate_recommendation(messages):
    """
    `messages` is a list of dicts:
      [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
        ...
      ]
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    conversation_id = data.get("conversation_id", "default")  
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    if conversation_id not in conversations:
        conversations[conversation_id] = [
            {"role": "system", "content": "You are a helpful real estate assistant."}
        ]

    conversations[conversation_id].append({"role": "user", "content": user_prompt})

    model_response = generate_recommendation(conversations[conversation_id])

    conversations[conversation_id].append({"role": "assistant", "content": model_response})

    return jsonify({
        "conversation_id": conversation_id,
        "response": model_response
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
