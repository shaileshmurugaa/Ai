from flask import Flask, request, jsonify, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_text = data.get("text")
    lang = data.get("lang", "en")  # default English

    # Translate to English for processing
    translated_input = GoogleTranslator(source=lang, target="en").translate(user_text)

    # Simple response logic (can replace with GPT API)
    if "sad" in translated_input:
        response_en = "I'm here for you. Stay strong!"
    else:
        response_en = "That's interesting. Tell me more!"

    # Translate response back to user language
    response_local = GoogleTranslator(source="en", target=lang).translate(response_en)

    # Convert to speech
    tts = gTTS(text=response_local, lang=lang)
    audio_path = "response.mp3"
    tts.save(audio_path)

    return jsonify({"text": response_local})

@app.route("/voice")
def get_voice():
    return send_file("response.mp3", mimetype="audio/mpeg")

# ✅ Correct position and indentation
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
