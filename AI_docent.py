import os
from flask import Flask, request, render_template, jsonify
from gtts import gTTS
from inference import prediction, chat_gpt
import whisper
import openai

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yolo = os.path.join(BASE_DIR, "checkpoint", "best.pt")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "upload_img.jpg")
AUDIO_FILE = os.path.join(UPLOAD_FOLDER, "upload_audio.mp3")

whisper_model = whisper.load_model("medium", device="cuda")  # Whisper 모델 로드

# Flask 라우트 정의
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

# 추가적인 라우트 정의는 생략합니다.

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image file provided'}), 400
    
    image = request.files['image']
    image.save(IMAGE_FILE)

    # YOLO 모델을 사용하여 이미지 예측
    predict = prediction(yolo, IMAGE_FILE)
    number = predict
    artwork = "Mademoiselle Caroline Rivière"
    # ChatGPT API 호출
    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI docent at the Louvre Museum. Answer questions in Korean as if you are explaining artwork to visitors."},
                {"role": "user", "content": f"Tell me about image number {artwork}."}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        gpt_message = gpt_response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({'error': f'Failed to get GPT response: {e}'}), 500

    return jsonify({'file_path': IMAGE_FILE, 'image_number': number, 'gpt_response': gpt_message})

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

        # ChatGPT API를 사용하여 변환된 텍스트 전송
        gpt_response = chat_gpt(GPT_API_KEY, transcription)
        gpt_message = gpt_response.choices[0].message['content']

        # 변환된 텍스트와 GPT 응답을 반환
        return jsonify({'file_path': AUDIO_FILE, 'transcription': transcription, 'gpt_response': gpt_message})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to process audio'}), 500


if __name__ == "__main__":
    # API 키 설정 (환경 변수나 직접 입력)
    GPT_API_KEY = os.getenv("GPT_API_KEY", "")
    openai.api_key = GPT_API_KEY
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
