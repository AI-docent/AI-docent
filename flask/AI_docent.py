from flask import Flask, request, render_template

from inference import prediction #, chat_gpt

app = Flask(__name__)

yolo = "flask/model_checkpoint/yolo.pt"

@app.route('/')
def select():
    return render_template('select.html')

@app.route('/free')
def free():
    return render_template("free.html")

@app.route('/tour')
def tour():
    return render_template("tour.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/touring')
def touring():
    return render_template("touring.html")

@app.route('/tourstart')
def tourstart():
    return render_template("tourstart.html")

if __name__ == "__main__":
    app.run(debug=True)
