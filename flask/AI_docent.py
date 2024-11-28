import os
from flask import Flask, request, render_template, jsonify
from gtts import gTTS
from inference import prediction, chat_gpt
from inference import prediction
# import whisper

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

yolo = os.path.join(BASE_DIR, "checkpoint", "best.pt")
GPT_API_KEY = "Add API KEY"


UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "upload_img.jpg")
AUDIO_FILE = os.path.join(UPLOAD_FOLDER, "upload_audio.mp3")

# whisper_model = whisper.load_model("large") #우리 사용할 모델 적으면 됨

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

    # try:
    #     # Whisper로 텍스트 변환
    #     transcription = whisper_model.transcribe(AUDIO_FILE)['text']
    #     print(f"Transcription: {transcription}")
    #     print(transcription)

    #     return jsonify({'file_path': AUDIO_FILE, 'transcription': transcription})
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return jsonify({'error': 'Failed to process audio'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
