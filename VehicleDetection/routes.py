from VehicleDetection import app
from flask import render_template, request, redirect, url_for, Response,session
from werkzeug.utils import secure_filename
from VehicleDetection.Video import DetectVehicles
import os

app.secret_key = "579162fdrfughhxtds4rd886fjur65edfg"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"

@app.route('/')
def index():
    return render_template('detect_vehicle.html')


@app.route('/save', methods=['POST'])
def save():
    file = request.files['video']
    print(file.filename)
    # read the file using cap = cv2.VideoCapture(video_src)
    filename = secure_filename(file.filename)
    video_path = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), 'static/Upload', filename)
    file.save(video_path)
    session['filename'] = video_path
    return redirect(url_for('show'))

@app.route('/show')
def show():
    return render_template('show.html')

def gen(camera):
    while True:
        # get camera frame
        frame = camera.detect_vehicles()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/detect')
def detect():
    return Response(gen(DetectVehicles(session.get('filename'))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
