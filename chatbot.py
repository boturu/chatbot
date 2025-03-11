import openai
import os
import json
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

openai.api_key = os.getenv("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")

user_sessions = {}

def get_chat_response(user_id, user_input):
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {"role": "system", "content": "You are a helpful AI chatbot assisting users with their queries."}
        ]
    
    user_sessions[user_id].append({"role": "user", "content": user_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=user_sessions[user_id],
            temperature=0.7,
            max_tokens=250
        )
        bot_response = response["choices"][0]["message"]["content"]
        user_sessions[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Error fetching response: {e}")
        return "Sorry, I encountered an issue while processing your request."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id", "default_user")
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    bot_response = get_chat_response(user_id, user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
