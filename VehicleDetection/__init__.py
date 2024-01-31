from flask import Flask
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/project 6th sem/vehicle Detection/detect/VehicleDetectionSystem/VehicleDetection'
car_cascade_src = os.path.join(app.config['UPLOAD_FOLDER'], 'models/cars.xml')
bike_cascade_src = os.path.join(app.config['UPLOAD_FOLDER'], 'models/cascade.xml')
from VehicleDetection import routes