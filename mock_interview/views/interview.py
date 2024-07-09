from flask import Blueprint,render_template, Response
import cv2

interview = Blueprint('interview', __name__)

@interview.route('/interview')
def index():
    return render_template('interview.html')

@interview.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




cap = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def gen_frames():
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (683, 383))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')