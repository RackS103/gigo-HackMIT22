import base64
from io import BytesIO
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory,Response, session
from werkzeug.utils import secure_filename
import json
from PIL import Image
from Predict_from_model import GarbagePredict

class EventSender():
    def __init__(self):
        self.state = {"img":"default","material":"default","suggestion":"default"}
        self.update_ready = 0
    def update(self, image,material,suggestion):
        print("updating")
        self.state = {"img":image,"material":material,"suggestion":suggestion}
        self.update_ready = True
    
    def send(self):
            self.update_ready = 0
            return json.dumps(self.state)


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "AHiygpiyGygiuoiIIuouyuhhu"
result = EventSender()
model = GarbagePredict()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             img = Image.open(file)
#             predicter = GarbagePredict()
#             material,sugg = (predicter.predict(img))
#             result.update(pil2datauri(img),material,sugg)

#     return send_from_directory("./","./index.html")

# @app.route("/update/", methods=["POST","GET"])
# def update(**thing):
#     if result.update_ready:
#             return Response(result.send(),
#                           mimetype="text/event-stream")
#     else: return Response(json.dumps({"img":"default","material":"default","suggestion":"default"}),
#                           mimetype="text/event-stream")

@app.route('/', methods=['GET'])
def index():
    return send_from_directory("./","./index.html")

@app.route('/webcam', methods=['GET', 'POST'])
def webcam(**stuff):
    if request.method == 'POST':
        request_json = request.json
        img = datauri2pil(request_json['img'])
        label, suggestions = model.predict(img)
    
    return json.dumps({'label':label, 'suggestions':str(suggestions)})


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
    print(datauri)
    data = base64.b64decode(datauri.split(',')[1])
    return Image().open(data).convert('RGB')

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

if __name__ == '__main__':
    app.run(port=5000)