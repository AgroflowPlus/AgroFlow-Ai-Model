import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.cli import run_cli
import json

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# ── CHAT ENDPOINT ──────────────────────────────────────
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Call your existing AI logic
        # Since run_cli() is interactive, we need to adapt it
        # This depends on how run_cli() works internally
        
        # If run_cli() returns a response, use it directly
        # Otherwise, you may need to refactor the chatbot module
        response = run_cli(user_message)  # Adjust based on actual function
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── HEALTH CHECK ──────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

# ── START SERVER ──────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
