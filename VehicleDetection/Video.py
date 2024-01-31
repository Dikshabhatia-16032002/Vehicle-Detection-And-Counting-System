import cv2
from VehicleDetection import app, car_cascade_src, bike_cascade_src


car_cascade = cv2.CascadeClassifier(car_cascade_src)
bike_cascade = cv2.CascadeClassifier(bike_cascade_src)


class DetectVehicles(object):

    def __init__(self, video_path):
        # capturing video
        print(video_path)
        self.video = cv2.VideoCapture(video_path)
        self.car_counter = 0
        self.bike_counter = 0

    def __del__(self):
        # releasing camera
        self.video.release()

    def detect_vehicles(self):

        def centerPoint(x, y, h, w):
            x1 = int(h / 2)
            y1 = int(w / 2)
            cx = x + x1
            cy = y + y1
            return cx, cy

        detect_car = []
        detect_bike = []

        min_width = 20
        min_height = 30
        max_width = 80
        max_height = 80
        count_line_position = 450
        offset = 7

        ret, img = self.video.read()
        img = cv2.resize(img, (1280, 720))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 1.1 2  6.5 17
        cars = car_cascade.detectMultiScale(gray, 1.1, 2)
        bikes = bike_cascade.detectMultiScale(gray, 1.1, 1)
        cv2.line(img, (0, count_line_position), (2500, count_line_position), (200, 20, 20), 3)
        for (x, y, w, h) in cars:
            cv2.putText(img, "car", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 250, 250), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            center = centerPoint(x, y, w, h)
            detect_car.append(center)
            cv2.circle(img, center, 4, (0, 255, 0), -1)
            for (x, y) in detect_car:
                if y < (count_line_position + offset) and y > (count_line_position - offset):
                    self.car_counter += 1
                cv2.line(img, (0, count_line_position), (2500, count_line_position), (0, 20, 20), 3)
                detect_car.remove((x, y))
        for (x, y, w, h) in bikes:
            cv2.putText(img, "bike", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 250, 250), 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            center = centerPoint(x, y, w, h)
            detect_bike.append(center)
            cv2.circle(img, center, 4, (0, 255, 0), -1)
            for (x, y) in detect_bike:
                if y < (count_line_position + offset) and y > (count_line_position - offset):
                    self.bike_counter += 1
                cv2.line(img, (0, count_line_position), (2500, count_line_position), (0, 20, 20), 3)
                detect_bike.remove((x, y))
        print("car_counter", self.car_counter)
        print("bike_counter", self.bike_counter)
        cv2.putText(img, "cars counter" + str(self.car_counter) + " bikes counter " + str(self.bike_counter), (350, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 250, 250), 4)
        cv2.imshow("frame", img)

        ret, jpeg = cv2.imencode('.jpeg', img)
        return jpeg.tobytes()
