import openai
import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

with open("real_estate_data.json", "r") as file:
    real_estate_listings = json.load(file)

def generate_recommendation(user_prompt):
    system_prompt = (
        "You are a helpful real estate assistant. Based on the user's request, "
        "provide suitable housing recommendations from the following listings:\n"
        f"{json.dumps(real_estate_listings, indent=2)}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
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

@app.route("/")
def home():
    return "Backend running fine!"

if __name__ == "__main__":
    app.run(debug=True)


