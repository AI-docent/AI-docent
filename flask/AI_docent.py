# 주석 처리는 debug + gpt api 제외라서 실제로 돌릴땐 주석 처리만 조금 신경쓰면 됨

import os
from flask import Flask, request, render_template, jsonify
from gtts import gTTS
from inference import prediction, chat_gpt
import whisper
import openai

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 파일 크기 16MB 설정
GPT_API_KEY = os.getenv("GPT_API_KEY", "")

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

@app.route('/android_free')
def android_free():
    return render_template("android_free.html")

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
    # artwork = "Mademoiselle Caroline Rivière"
    # ChatGPT API 호출
    # try:
    #     gpt_response = chat_gpt(GPT_API_KEY, artwork)
    #     gpt_message = gpt_response['choices'][0]['message']['content'].strip()
    # except Exception as e:
    #     return jsonify({'error': f'Failed to get GPT response: {e}'}), 500

    # return jsonify({'file_path': IMAGE_FILE, 'image_number': number, 'gpt_response': gpt_message})
    return jsonify({'file_path': IMAGE_FILE, 'image_number': number, 'gpt_response': predict})

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    # 오디오 파일 저장
    audio = request.files['audio']
    audio.save(AUDIO_FILE)

    try:
        # Whisper 모델로 음성 -> 텍스트 변환
        result = whisper_model.transcribe(AUDIO_FILE)
        transcription = result.get("text", "").strip()
        print(f"Whisper Transcription: {transcription}")

        # 변환된 텍스트 반환
        return jsonify({'transcription': transcription})
    except Exception as e:
        print(f"Whisper Error: {e}")
        return jsonify({'error': 'Failed to process audio with Whisper'}), 500
    
@app.route('/chat-gpt', methods=['POST'])
def chat_gpt():
    # 변환된 텍스트 받아오기
    data = request.get_json()
    transcription = data.get("transcription")
    print("gpt tran",transcription)
    # if not transcription:
    #     return jsonify({'error': 'No transcription provided'}), 400

    try:
        # ChatGPT API 호출
        # gpt_response = chat_gpt(GPT_API_KEY, transcription)
        # gpt_message = gpt_response['choices'][0]['message']['content'].strip()
        # print(gpt_message)
        
        # GPT 응답 반환
        # return jsonify({'gpt_response': gpt_message})
        return jsonify({'gpt_response': "test 성공"})
    except Exception as gpt_error:
        print(f"ChatGPT Error: {gpt_error}")
        return jsonify({'error': 'Failed to process with ChatGPT'}), 500


if __name__ == "__main__":
    # API 키 설정 (환경 변수나 직접 입력)
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
