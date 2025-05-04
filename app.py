import time
import pyrebase
import openai
import traceback
from flask import Flask, request, jsonify ,session
from flask_cors import CORS
import random
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
# Use a strong secret key - this is used to encrypt the session
app.secret_key = "your-strong-secret-key-change-this-in-production"

# Configure CORS with more specific settings
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5000", "http://127.0.0.1:5000", "null"],
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

# Session configuration - critical for persistence
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on filesystem
app.config['SESSION_PERMANENT'] = True     # Make sessions persistent
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SESSION_COOKIE_SAMESITE'] = None  # For development - in prod use 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False    # For development - in prod use True with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
# ----------------------------------------------------------------------------
# 1. llm setup
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# 2. Firebase Connection & Setup
# ----------------------------------------------------------------------------
firebaseConfig = {
 

};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# ----------------------------------------------------------------------------
# 3. Conversation Storage Functions
# ----------------------------------------------------------------------------
def store_message(user_id, role, content):
    """Store a message in Firebase under the user's conversation history."""
    data = {
          # millisecond timestamp
    }
    # Push the new message under conversations/<user_id>


def get_conversation_history(user_id):
    """
    Retrieve all messages for a given user, ordered by timestamp.
    Returns a list of dictionaries: [{"role": "...", "content": "..."}, ...].
    """
    messages = db.child("conversations").child(user_id).order_by_child("timestamp").get()
    conversation = []
    if messages.each():
        for msg in messages.each():
            conversation.append(msg.val())
    return conversation

# ----------------------------------------------------------------------------
# 4. Helper Functions (Tips, Emojis, etc.)
# ----------------------------------------------------------------------------
def add_emoji(response):
    emoji_map = {
        "sad": "😔", "happy": "😊", "anxious": "😟", "excited": "😃",
        "angry": "😠", "stress": "😩", "support": "🤗", "love": "❤️",
        "sorry": "☹️😟", "bullying": "😞", "understand": "🤍",
    }
    for word, emoji in emoji_map.items():
        if word in response.lower():
            return f"{response} {emoji}"
    return response

def get_stress_and_headache_tips():
    return (
        "Based on your mention of a headache or stress, you might benefit from these tips:\n"
        "- Take short breaks to breathe deeply or do light stretching.\n"
        "- Drink plenty of water throughout the day.\n"
        "- Identify any stress triggers and try to manage or reduce them.\n"
        "- Ensure you get enough sleep (7–9 hours) when possible.\n\n"
        "How have you been feeling since you last mentioned your headache?"
    )

def call_openai_with_retry(messages, max_retries=3, delay=2):
    """Call OpenAI with retry logic to handle transient errors."""
    for attempt in range(max_retries):
        try:
            response = openai_client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=messages,
                timeout=10
            )
            return response
        except Exception as e:
            print(f"OpenAI connection error on attempt {attempt+1}/{max_retries}: {e}")
            time.sleep(delay)
    raise Exception("Max retries exceeded for OpenAI call.")

# ----------------------------------------------------------------------------
# 5. Flask Chat Endpoint (Using Firebase for Conversation Storage)
# ----------------------------------------------------------------------------
user_id_store = None

@app.route("/check-session", methods=["GET"])
def check_session():
    global user_id_store
    if user_id_store:
        return jsonify({"message": "Session active", "userId": user_id_store})
    else:
        return jsonify({"message": "No active session", "userId": None})

@app.route("/save-user", methods=["POST"])
def save_user():
    global user_id_store
    data = request.get_json()
    user_id = data.get("userId")
    if not user_id:
        return jsonify({"error": "No user id provided"}), 400
    
    # Store the user id in global variable
    user_id_store = user_id
    print(f"User ID saved in global variable: {user_id_store}")
    
    # Set as a cookie too (backup method)
    response = jsonify({"message": "User ID saved", "userId": user_id})
    response.set_cookie('user_id', user_id, max_age=86400)  # 24 hour cookie
    
    return response

@app.route("/chat", methods=["POST"])
def chat():
    global user_id_store
    data = request.json
    user_input = data.get("message", "")
    
    # First try getting user ID from global variable
    user_id = user_id_store

    if not user_id:
        user_id = request.cookies.get('user_id')
    
    print(f"Retrieved user ID: {user_id}")
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    try:
        # (A) Retrieve conversation history from Firebase for this user
        conversation_history = get_conversation_history(user_id)

    
@app.route("/feel-good-lists", methods=["GET"])
def feel_good_lists():

    return jsonify(feel_good_data)

if __name__ == "__main__":
    app.run(debug=True,port=5000)