from flask import Flask, request, jsonify, render_template
from Agent.agent import create_agent
from Agent.memory import save_user_memory
from Agent.intent import detect_intent
from config import Config
import os

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Use centralized configuration
os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/conversation/", methods=["POST"])
def conversation():
    try:
        data = request.json
        user_input = data.get("input", "")
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Fetch the agent for the user based on user_id
        agent = create_agent(user_id)

        # Fetch conversation history from memory
        memory = agent.memory

        # Determine the intent based on conversation history
        intent = detect_intent(user_input, memory)

        # Take action based on the intent
        if intent == "risk_analysis":
            response = agent.invoke(str(user_id)+","+user_input)
            save_user_memory(user_id, user_input, response["output"])  # Save user-specific memory
            return jsonify({"intent": "risk_analysis", "response": response})

        elif intent == "investment_planning":
            response = agent.invoke(str(user_id)+","+user_input)
            save_user_memory(user_id, user_input, response["output"])  # Save user-specific memory
            return jsonify({"intent": "investment_plan", "response": response})

        elif intent == "unknown":
            response = agent.invoke(str(user_id)+","+user_input)
            save_user_memory(user_id, user_input, response["output"])  # Save user-specific memory
            return jsonify({"intent": "unknown", "response": response})

        return jsonify({"error": "Unable to determine intent"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    # Validate configuration before starting
    if not Config.validate_config():
        print("⚠️  Please check your configuration before starting the application.")
    
    app.run(port=Config.APP_PORT, debug=Config.APP_DEBUG)
