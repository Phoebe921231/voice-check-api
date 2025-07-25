from flask import Flask, request, jsonify
import os
import whisper

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/upload', methods=['POST'])
def upload_audio():
    file_path = None
    try:
        audio = request.files['file']
        file_path = os.path.join("static", audio.filename)
        audio.save(file_path)

        result = model.transcribe(file_path)
        text = result['text']

        scam_keywords = ["轉帳", "帳號", "中獎", "付款", "快遞", "警察", "檢察官"]
        is_scam = any(keyword in text for keyword in scam_keywords)

        return jsonify({
            "transcription": text,
            "is_scam": is_scam
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

@app.route("/")
def index():
    return "Voice scam check API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

