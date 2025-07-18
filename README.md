# 🧠 Dr.Druggs – A Therapy Chatbot

<img width="1920" height="1080" alt="Dr Drugg's Architecture" src="https://github.com/user-attachments/assets/2ba25ba6-773c-4e20-a727-6248983134d3" />

Your AI-powered mental health companion built using Python, NLP, and web technologies.

# youtube link: https://youtu.be/vHBq3-fSR0E

Dr.Druggs is a conversational therapy chatbot designed to provide a supportive empathetic interface for users seeking mental health assistance. It's not a replacement for professional therapy, but an approachable and educational tool to promote mental wellness through conversation.

🌟 Features
🤖 AI-Powered Conversations using NLP

🧘 Emotionally intelligent responses with basic sentiment analysis

💬 Pre-trained intents and responses for common mental health topics

🌐 Web-based interface for interactive use

🛠️ Easy to modify and expand (open source)

🧰 Tech Stack
Tech	Description
Python	Core chatbot logic and NLP processing
Flask	Lightweight web server & routing
HTML/CSS/JS	Frontend user interface
NLTK / JSON	Natural language tools & intents model

🚀 Getting Started
1. Clone the repository:
git clone https://github.com/krishnamuttevi/Dr.Druggs-A-Therapy-Chatbot.git
cd Dr.Druggs-A-Therapy-Chatbot
2. Install dependencies:
pip install -r requirements.txt
3. Run the chatbot locally:
python app.py
Open your browser and go to:
http://127.0.0.1:5000/

🧠 How It Works
User sends a message through the web interface.

NLTK and custom intents determine the user's intent.

The bot generates a relevant response based on predefined patterns.

The conversation continues interactively in a chat-like UI.

### 📁 Project Structure

```
Dr.Druggs-A-Therapy-Chatbot/
├── app.py                 # Main Flask app
├── intents.json           # Intent definitions and training data
├── static/                # CSS, JS files
├── templates/             # HTML files
├── chatbot_model.pkl      # Trained model (if applicable)
├── README.md              # Project documentation
```



🔒 Disclaimer
This chatbot is intended for educational purposes only and is not a substitute for licensed mental health care. If you're experiencing a crisis or need support, please reach out to a professional or emergency services.

📢 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

