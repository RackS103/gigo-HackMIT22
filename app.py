import base64
from io import BytesIO
from flask import Flask, request, send_from_directory
import json
from PIL import Image
from Predict_from_model import GarbagePredict


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "AHiygpiyGygiuoiIIuouyuhhu"
model = GarbagePredict()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return send_from_directory("./","./index.html")

@app.route('/webcam', methods=['GET', 'POST'])
def webcam(**stuff):
    if request.method == 'POST':
        request_json = request.json
        img = datauri2pil(request_json['img'])
        label, suggestions = model.predict(img)
    
    return json.dumps({'label':label, 'suggestions':list(suggestions)})


@app.route("/script2.js",methods=["POST","GET"])
def script():
    return send_from_directory("./","./script2.js")

@app.route("/styles.css",methods=["POST","GET"])
def css():
    return send_from_directory("./","./styles.css")

@app.route("/styles.css",methods=["POST","GET"])
def styles():
    return send_from_directory("./","./styles.css")

@app.route("/uploads/<filename>", methods=["GET","POST"])
def imagesend(filename):
    return send_from_directory("./uploads",filename)

def datauri2pil(datauri):
    raw_data = datauri.split(",")[1]
    data = base64.b64decode(raw_data)
    return Image.open(BytesIO(data)).convert('RGB')

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

if __name__ == '__main__':
    app.run(port=5000)