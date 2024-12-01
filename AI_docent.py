import os
import whisper
import time

from flask import Flask, request, render_template, jsonify
from gtts import gTTS
from inference import prediction, gpt_generator

app = Flask(__name__)
@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print(f"Exception occurred: {traceback.format_exc()}")
    return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

GPT_API_KEY = os.getenv("GPT_API_KEY", "API KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yolo = os.path.join(BASE_DIR, "checkpoint", "best.pt")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "upload_img.jpg")
AUDIO_FILE = os.path.join(UPLOAD_FOLDER, "upload_audio.mp3")
TTS_FILE = os.path.join(UPLOAD_FOLDER, "upload_tts.mp3")

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
@app.route('/tourend')
def tourend():
    return render_template("tourend.html")
@app.route('/touring')
def touring():
    return render_template("touring.html")
@app.route('/touring2')
def touring2():
    return render_template("touring2.html")
@app.route('/touring3')
def touring3():
    return render_template("touring3.html")
@app.route('/touring4')
def touring4():
    return render_template("touring4.html")
@app.route('/touring5')
def touring5():
    return render_template("touring5.html")
@app.route('/touring6')
def touring6():
    return render_template("touring6.html")
@app.route('/touring7')
def touring7():
    return render_template("touring7.html")
@app.route('/touring8')
def touring8():
    return render_template("touring8.html")
@app.route('/touring9')
def touring9():
    return render_template("touring9.html")
@app.route('/touring10')
def touring10():
    return render_template("touring10.html")
@app.route('/touring11')
def touring11():
    return render_template("touring11.html")
@app.route('/touring12')
def touring12():
    return render_template("touring12.html")
@app.route('/tourstart')
def tourstart():
    return render_template("tourstart.html")
@app.route('/tourstart2')
def tourstart2():
    return render_template("tourstart2.html")
@app.route('/tourstart3')
def tourstart3():
    return render_template("tourstart3.html")
@app.route('/tourstart4')
def tourstart4():
    return render_template("tourstart4.html")
@app.route('/tourstart5')
def tourstart5():
    return render_template("tourstart5.html")
@app.route('/tourstart6')
def tourstart6():
    return render_template("tourstart6.html")
@app.route('/tourstart7')
def tourstart7():
    return render_template("tourstart7.html")
@app.route('/tourstart8')
def tourstart8():
    return render_template("tourstart8.html")
@app.route('/tourstart9')
def tourstart9():
    return render_template("tourstart9.html")
@app.route('/tourstart10')
def tourstart10():
    return render_template("tourstart10.html")
@app.route('/tourstart11')
def tourstart11():
    return render_template("tourstart11.html")
@app.route('/tourstart12')
def tourstart12():
    return render_template("tourstart12.html")

@app.route('/stt', methods=['POST'])
def stt():
    # 기존 TTS 파일 삭제
    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith("upload_tts_") and file.endswith(".mp3"):
            os.remove(os.path.join(UPLOAD_FOLDER, file))

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    audio.save(AUDIO_FILE)

    try:
        # Whisper 모델로 음성 -> 텍스트 변환
        result = whisper_model.transcribe(AUDIO_FILE)
        transcription = result.get("text", "").strip()
        print(f"Whisper Transcription: {transcription}")

        return jsonify({'transcription': transcription})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to process STT'}), 500
    
@app.route('/gpt-to-tts', methods=['POST'])
def gpt_to_tts():
    # 기존 TTS 파일 삭제
    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith("upload_tts_") and file.endswith(".mp3"):
            os.remove(os.path.join(UPLOAD_FOLDER, file))

    data = request.get_json()
    print(f"Received Data: {data}")  # 요청 데이터 확인
    transcription = data.get("transcription", "")

    if not transcription:
        return jsonify({'error': 'No transcription provided'}), 400

    try:
        # GPT-4 API 호출
        gpt_response = gpt_generator(GPT_API_KEY, None, None, transcription, audio=True)
        gpt_message = gpt_response.get("gpt_response", "응답 없음")
        print(f"GPT Response: {gpt_message}")

        # 고유한 TTS 파일 이름 생성 (타임스탬프 사용)
        tts_filename = f"upload_tts_{int(time.time())}.mp3"
        tts_path = os.path.join(UPLOAD_FOLDER, tts_filename)

        # TTS 음성 파일 생성
        tts = gTTS(text=gpt_message, lang='ko', slow=False)
        tts.save(tts_path)

        return jsonify({
            'gpt_response': gpt_message,
            'audio_url': f'/static/{tts_filename}'
        })
    except Exception as e:
        print(f"Error during GPT processing: {e}")
        return jsonify({'error': 'Failed to process GPT to TTS'}), 500

# GPT 호출 후 TTS 처리
@app.route('/upload-image', methods=['POST'])
def upload_image():
    # 기존 TTS 파일 삭제
    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith("upload_tts_") and file.endswith(".mp3"):
            os.remove(os.path.join(UPLOAD_FOLDER, file))

    if 'image' not in request.files:
        return jsonify({'error': 'No Image file provided'}), 400

    image = request.files['image']
    image.save(IMAGE_FILE)

    try:
        # YOLO 모델을 사용하여 이미지 예측
        artwork, artist = prediction(yolo, IMAGE_FILE)
        # artwork, artist = prediction(yolo, "E:\\python\\code_file\\NLP\\AI-docent\\flask\\static\\test.jpg")

        # 예측이 없을 경우 GPT 호출을 스킵하고 적절한 응답 반환
        if artwork == "미상" and artist == "미상":
            return jsonify({'file_path': IMAGE_FILE, 'message': 'No artwork detected in the uploaded image. Please try with a different image.'})

        # ChatGPT API 호출
        gpt_response = gpt_generator(GPT_API_KEY, artwork, artist, None, False)
        gpt_message = gpt_response.get("gpt_response", "응답 없음")
        print(f"GPT Response: {gpt_message}")

        # TTS 음성 파일 생성
        tts_filename = f"upload_tts_{int(time.time())}.mp3"
        tts_path = os.path.join(UPLOAD_FOLDER, tts_filename)
        tts = gTTS(text=gpt_message, lang='ko', slow=False)
        tts.save(tts_path)

        # 변환된 텍스트와 TTS 파일 URL 반환
        return jsonify({
            'file_path': IMAGE_FILE,
            'gpt_response': gpt_message,
            'audio_url': f'/static/{tts_filename}'
        })
    except Exception as e:
        print(f"Error during image processing: {e}")
        return jsonify({'gpt_response': '이미지 처리 중 오류가 발생했습니다. 다시 시도해주세요.'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
