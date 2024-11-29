from flask import Flask, request, jsonify, render_template
import requests
from transformers import pipeline

app = Flask(__name__)

# Bhashini API endpoints (replace placeholders with actual URLs)
BHASHINI_TTS_API = "https://bhashini.gov.in/api/tts"  # Replace with actual endpoint
BHASHINI_STT_API = "https://bhashini.gov.in/api/stt"  # Replace with actual endpoint

# Load Hugging Face pipeline for grammar analysis
grammar_model = pipeline("text-classification", model="aychang/roberta-base-imdb")

# Questions for the linguistic test
QUESTIONS = [
    "How much is a plate of rice?",
    "What time does the market open?",
    "Can you tell me where the bus stand is?",
    "How do I reach the railway station?",
]

# Function to analyze grammar and score the response
def evaluate_grammar(response):
    # Analyze using the grammar model
    result = grammar_model(response)[0]
    # Dummy scoring logic (you can customize this based on output labels)
    score = round(result['score'] * 10, 2)  # Score out of 10
    return score

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_question", methods=["GET"])
def get_question():
    question = QUESTIONS.pop(0) if QUESTIONS else None
    if question:
        # Generate TTS using Bhashini
        tts_response = requests.post(BHASHINI_TTS_API, json={"text": question, "language": "hi"})  # Adjust language code
        audio_url = tts_response.json().get("audio_url")  # Assume Bhashini provides an audio URL
        return jsonify({"question": question, "audio_url": audio_url})
    else:
        return jsonify({"message": "Test completed!"}), 200

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    # Receive user's audio file
    user_audio = request.files["audio"]
    # Send to Bhashini STT for transcription
    stt_response = requests.post(
        BHASHINI_STT_API, files={"audio": user_audio}, data={"language": "hi"}  # Adjust language code
    )
    user_text = stt_response.json().get("transcription")
    
    # Evaluate grammar
    score = evaluate_grammar(user_text)
    return jsonify({"transcription": user_text, "score": score})

if __name__ == "__main__":
    app.run(debug=True)
