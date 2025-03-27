import openai
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

with open("real_estate_data.json", "r") as file:
    real_estate_listings = json.load(file)

def generate_recommendation(prompt):
    system_prompt = f"You are a real estate assistant. Based on the user's request, provide suitable housing recommendations from the following listings:\n{json.dumps(real_estate_listings, indent=2)}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("prompt")
    if not user_prompt:
        return jsonify({"error": "Please provide a prompt."}), 400

    recommendations = generate_recommendation(user_prompt)
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

