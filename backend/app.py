from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from agents.salon_agent import SalonAgent
import sys
import os

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# Enable CORS for all routes so Vercel can connect
CORS(app)

# Initialize the agent once so it maintains memory
try:
    agent = SalonAgent()
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if agent is None:
        return jsonify({"response": "Error: Agent is not initialized. Please check backend logs."})
        
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat?"})
        
    try:
        reply = agent.chat(user_message)
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=False, port=5000)
