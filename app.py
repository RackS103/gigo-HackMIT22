import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory,Response
from werkzeug.utils import secure_filename
import json
import PIL as pl


class EventSender():
    def __init__(self):
        self.state = {"img":"default","bin":"default"}
        self.update_ready = 0
    def update(self, image,bin_):
        print("updating")
        self.state = {"img":image,"bin":bin_}
        self.update_ready = True
    
    def send(self):
            self.update_ready = 0
            return json.dumps(self.state)


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
classification = "none yet"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

result = EventSender()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(file)
            filename = secure_filename(file.filename)
            pl.Image
            result.update(image = "/uploads/" + filename, bin_ = "trash")

    return send_from_directory("./","./index.html")

@app.route("/update/", methods=["POST","GET"])
def update(**thing):
    if result.update_ready:
            return Response(result.send(),
                          mimetype="text/event-stream")
    else: return Response(json.dumps({"img":"default","bin":"default"}),
                          mimetype="text/event-stream")

@app.route("/script2.js",methods=["POST","GET"])
def script():
    return send_from_directory("./","./script2.js")

@app.route("/uploads/<filename>", methods=["GET","POST"])
def imagesend(filename):
    return send_from_directory("./uploads",filename)


