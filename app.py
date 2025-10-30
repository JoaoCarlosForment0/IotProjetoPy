import os
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers = {
    'Content-Type': 'application/json',
    'x-goog-api-key': TOKEN
}

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get('prompt')
    if not user_input:
        return jsonify({'Error': 'prompt obrigatorio'}), 400
    
    payload = {
        'contents': [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
        }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    print("Status:", response.status_code)
    print("Resposta:", response.text)

    if response.status_code == 200:
        ai_response = response.json()
        try:
            answer = (
                ai_response["candidates"][0]["content"]["parts"][0]["text"]
                if "content" in ai_response["candidates"][0]
                else ai_response["candidates"][0]["output"]
            )
        except Exception:
            answer = ai_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return jsonify({'response': answer})
    else:
        return jsonify({'error': 'erro ao acessar api', "detalhe": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)