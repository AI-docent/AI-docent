import os
from flask import Flask, request, render_template, jsonify
from gtts import gTTS
from inference import prediction, chat_gpt
from inference import prediction
import whisper

app = Flask(__name__)

yolo = "checkpoint/best.pt"
GPT_API_KEY = "Add API KEY"

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "upload_img.jpg")
AUDIO_FILE = os.path.join(UPLOAD_FOLDER, "upload_audio.mp3")

whisper_model = whisper.load_model("large") #우리 사용할 모델 적으면 됨

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/select')
def select():
    return render_template("select.html")

@app.route('/free')
def free():
    return render_template("free.html")

@app.route('/tour')
def tour():
    return render_template("tour.html")

@app.route('/touring')
def touring():
    return render_template("touring.html")

@app.route('/tourstart')
def tourstart():
    return render_template("tourstart.html")

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image file provided'}), 400
    
    image = request.files['image']
    image.save(IMAGE_FILE)

    predict = prediction(yolo, IMAGE_FILE)
    # predict = prediction(yolo, 'E:/python/code_file/NLP/AI-docent/flask/static/test.jpg')

    gpt_response = chat_gpt(GPT_API_KEY, predict[0])
    gpt_message = gpt_response.choices[0].message['content']

    return jsonify({'file_path': IMAGE_FILE, 'gpt_response': gpt_message})

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    # 오디오 파일 저장
    audio = request.files['audio']
    audio.save(AUDIO_FILE)

    try:
        # Whisper로 텍스트 변환
        transcription = whisper_model.transcribe(AUDIO_FILE)['text']
        print(f"Transcription: {transcription}")
        print(transcription)

        return jsonify({'file_path': AUDIO_FILE, 'transcription': transcription})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to process audio'}), 500

if __name__ == "__main__":
    app.run(debug=True)
