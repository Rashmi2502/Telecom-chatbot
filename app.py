from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")  # Retrieve the API key from the environment variable

# Configure the API with the key
genai.configure(api_key=api_key)

# Select the model
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

# Define common greetings, telecom-related keywords, and payment-related keywords
greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
telecom_keywords = ["billing", "internet", "TV", "network", "support", "plan", "service", "connection", "data", "charges", "router", "recharge"]
payment_keywords = ["payment", "pay", "billing", "invoice", "charges", "payment options", "credit card", "debit card", "paypal"]

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message").lower().strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Check for greetings
        if any(greet in user_message for greet in greetings):
            return jsonify({"reply": "Hello! How can I assist you with your telecom-related queries today?"})

        # Check if the message contains payment-related keywords
        if any(keyword in user_message for keyword in payment_keywords):
            return jsonify({"reply": "We offer several payment options: \n1. Online payments via credit/debit cards. \n2. Direct bank transfers. \n3. Mobile wallet payments (like PayPal). \nPlease let me know if you need further details."})

        # Check if the message contains telecom-related keywords
        if not any(keyword in user_message for keyword in telecom_keywords):
            return jsonify({"reply": "Sorry, I can only assist with telecom-related queries. Please ask about billing, internet, TV services, or any other telecom-related topic."})

        # Add instruction for concise response
        user_message += "\n\nPlease respond briefly and to the point. Keep your answer short."

        # Generate a response using Gemini
        response = model.generate_content(user_message)
        chatbot_reply = response.text if response.text else "Sorry, I couldn't understand your query."

        return jsonify({"reply": chatbot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5001)
