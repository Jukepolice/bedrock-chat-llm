from flask import Flask, request, jsonify
import json
import re
import ollama

app = Flask(__name__)

with open('gaben_knowledge.json', 'r') as f:
    gaben_knowledge = json.load(f)

def find_helpful_info(player_message):
    message_lower = player_message.lower()
    for entry in gaben_knowledge:
        for keyword in entry["question_keywords"]:
            if re.search(r'\b' + re.escape(keyword) + r'\b', message_lower):
                return entry["answer"]
    return None

@app.route('/gaben', methods=['POST'])
def gaben_endpoint():
    data = request.json
    player = data.get('player')
    message = data.get('message')
    helpful_info = find_helpful_info(message)

    if helpful_info:
        prompt = (
            f"{player} asked: \"{message}\"\n"
            f"Helpful info for Gaben: \"{helpful_info}\"\n"
            f"Respond as a Minecraft server assistant named Gaben. Greet {player} directly. Act friendly and respond as short as possible. Don't use emojis, symbols, or special characters like commas, hyphens, or apostrophe's."
        )

    else:
        prompt = (
            f"{player} asked: \"{message}\"\n"
            f"Respond as a Minecraft server assistant named Gaben. Act friendly and respond as short as possible. Don't use emojis, symbols, or special characters like commas, hyphens, or apostrophe's."
            f"If unsure, kindly suggest they ask an admin."
        )

    response = ollama.generate(
        model='gemma3',
        prompt=prompt
    )

    reply = response.get('response', "Sorry, I couldn't come up with an answer!")

    return jsonify({
        "action": "message",
        "content": reply
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9595)
