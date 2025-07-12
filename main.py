from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 Gemini API key and URL
GEMINI_API_KEY = "AIzaSyCdT03StbfefLzQUxTAZmR2YX9WfK60L1Q"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Gemini API থেকে উত্তর আনা
def ask_gemini(question):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }
    response = requests.post(GEMINI_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "❌ No valid response from Gemini."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# হোম রুট: JSON এ ডিটেইলস + ক্রেডিট
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🚀 Welcome to Gemini API",
        "developer": {
            "name": "SAHIL",
            "telegram": "https://t.me/YAMRAJSAHIL2",          
        },
        "credit": "Developed by @YAMRAJSAHIL2"
    })

# /ask রুট: প্রশ্নের উত্তর + স্পষ্ট ক্রেডিট আলাদা JSON এ
@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("text")
    if not question:
        return jsonify({"error": "Missing 'text' query parameter. Example: /ask?text=Who are you?"})
    
    answer = ask_gemini(question)
    credit = "Developed by @YAMRAJSAHIL2"
    
    return jsonify({
        "question": question,
        "answer": answer,
        "credit": credit
    })

if __name__ == "__main__":
    app.run()