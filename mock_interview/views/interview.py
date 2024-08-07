from flask import Blueprint, render_template, Response,jsonify, request
import cv2
import os
import dlib
import numpy as np
from deepface import DeepFace
from ..models import audio_func as audio
import threading
from flask_login import current_user
from ..models import firebase_func as db
# from ..models import face_detect


interview = Blueprint('interview', __name__)

@interview.route('/interview')
def index():
    return render_template('interview.html')


@interview.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@interview.route('/start_camera')
def start_camera():
    global cap
    cap = cv2.VideoCapture(0)

    # Audio
    global audio_thread, audio_results
    audio_results = {}
    def run_audio():
        global audio_results
        
        audio_results = audio.main()
    
    audio_thread = threading.Thread(target=run_audio)
    audio_thread.start()
    return 'Camera started'

@interview.route('/end_interview', methods=['POST'])
def end_interview():
    global cap, total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count, total_frames, looking_at_camera_frames
    global audio_thread, audio_results
    if cap:
        cap.release()
        cap = None
        
    user_id = current_user.id # 使用current_user.id取得當前使用者的id
    department = request.form.get('department')
    school = request.form.get('school')
    generatedQuestion = request.form.get('question')
    schooldepartment = school + " " + department
    
    print(user_id)
    print(department)
    print(school)
    print(schooldepartment)

    # Retrieve the resume file from the request
    resume = request.files.get('resume')
    if resume is None:
        return jsonify({'error': 'No resume file provided'}), 400

    # Calculate percentages
    stats = {
        'total_emotion_count': total_emotion_count,
        'angry_percent': round(angry_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'disgust_percent': round(disgust_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'fear_percent': round(fear_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'happy_percent': round(happy_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'sad_percent': round(sad_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'surprise_percent': round(surprise_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'neutral_percent': round(neutral_count / total_emotion_count * 100) if total_emotion_count > 0 else 0,
        'percentage_looking_at_camera': round(looking_at_camera_frames / total_frames * 100) if total_frames > 0 else 0
    }
    
    #維綸要在這裡拿圖像辨識參數
    #參數包含：
    #總共偵測幾次情緒 total_emotion_count
    #六種情緒比例 angry_percent,disgust_percent,fear_percent,happy_percent,sad_percent,surprise_percent,neutral_percent
    #眼睛看鏡頭/不看鏡頭的時間比例 percentage_looking_at_camera
    
    # Reset counters
    total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count = (0, 0, 0, 0, 0, 0, 0, 0)
    total_frames = 0
    looking_at_camera_frames = 0

    ### ------------ Audio -------------
    audio.stop_event.set()
    audio_thread.join()

    # 這裡是音訊辨識的結果
    # audio_results = {
    #     "accumulated_transcript": 使用者的逐字稿
    #     "word_count": 每一個音檔的字數
    #     "total_words": 總字數
    #     "recording_times": 總共錄了幾個音檔
    # }
    
    
    
    #完成面試後將資料上傳到資料庫
    ##---------上傳資料庫---------
    interview_id = db.addInterview(school, department, 1, resume,user_id) #新增interview
    question_id = db.addQuestions(department, school, interview_id, schooldepartment, generatedQuestion, user_id)
    ##---------上傳資料庫---------
    
    
    return jsonify({'stats': stats, 'audio_results': audio_results, 'interview_id': interview_id, 'user_id': user_id, 'question_id': question_id})



    
cap = None
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Initialize the camera and dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


# Tunable parameters
EAR_THRESHOLD = 0.21  # Eye Aspect Ratio threshold
HORIZONTAL_GAZE_THRESHOLD_LOW = 0.55
HORIZONTAL_GAZE_THRESHOLD_HIGH = 2.0
VERTICAL_GAZE_THRESHOLD_LOW = 0.5  # Stricter lower threshold for vertical gaze
VERTICAL_GAZE_THRESHOLD_HIGH = 1.5

total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count = (0, 0, 0, 0, 0, 0, 0, 0)
emotion = None
total_frames = 0
looking_at_camera_frames = 0


def eye_aspect_ratio(eye):
    A = np.linalg.norm(np.array([eye[1].x, eye[1].y]) - np.array([eye[5].x, eye[5].y]))
    B = np.linalg.norm(np.array([eye[2].x, eye[2].y]) - np.array([eye[4].x, eye[4].y]))
    C = np.linalg.norm(np.array([eye[0].x, eye[0].y]) - np.array([eye[3].x, eye[3].y]))
    ear = (A + B) / (2.0 * C)
    return ear

def get_iris_position(eye, frame):
    eye_region = np.array([(eye[0].x, eye[0].y), (eye[1].x, eye[1].y), (eye[2].x, eye[2].y),
                           (eye[3].x, eye[3].y), (eye[4].x, eye[4].y), (eye[5].x, eye[5].y)], np.int32)
    (x, y, w, h) = cv2.boundingRect(eye_region)
    eye = frame[y:y + h, x:x + w]
    eye = cv2.resize(eye, (150, 100))
    gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape

    #draw eye line
    # cv2.polylines(frame, [eye_region], isClosed=True, color=(0, 255, 255), thickness=1)


    # Calculate horizontal gaze ratio
    left_side_threshold = threshold_eye[0:height, 0:int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0:height, int(width / 2):width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    horizontal_gaze_ratio = (left_side_white + 1) / (right_side_white + 1)  # Avoid division by zero

    # Calculate vertical gaze ratio
    top_side_threshold = threshold_eye[0:int(height / 2), 0:width]
    top_side_white = cv2.countNonZero(top_side_threshold)
    bottom_side_threshold = threshold_eye[int(height / 2):height, 0:width]
    bottom_side_white = cv2.countNonZero(bottom_side_threshold)
    vertical_gaze_ratio = (top_side_white + 1) / (bottom_side_white + 1)  # Avoid division by zero

    return horizontal_gaze_ratio, vertical_gaze_ratio

def analyze_face(landmarks, frame):
    left_eye = [landmarks.part(n) for n in range(36, 42)]
    right_eye = [landmarks.part(n) for n in range(42, 48)]
    
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    
    eyes_closed = left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD
    eyes_open = not eyes_closed
    
    left_horizontal_gaze, left_vertical_gaze = get_iris_position(left_eye, frame)
    right_horizontal_gaze, right_vertical_gaze = get_iris_position(right_eye, frame)
    
    horizontal_gaze_within_threshold = (HORIZONTAL_GAZE_THRESHOLD_LOW < left_horizontal_gaze < HORIZONTAL_GAZE_THRESHOLD_HIGH)
    # and HORIZONTAL_GAZE_THRESHOLD_LOW < right_horizontal_gaze < HORIZONTAL_GAZE_THRESHOLD_HIGH
    vertical_gaze_within_threshold = (VERTICAL_GAZE_THRESHOLD_LOW < left_vertical_gaze < VERTICAL_GAZE_THRESHOLD_HIGH)
    #and VERTICAL_GAZE_THRESHOLD_LOW < right_vertical_gaze < VERTICAL_GAZE_THRESHOLD_HIGH
    
    looking_at_camera = horizontal_gaze_within_threshold and vertical_gaze_within_threshold
    return eyes_open, eyes_closed, looking_at_camera, left_vertical_gaze,right_vertical_gaze,left_horizontal_gaze,right_horizontal_gaze

def draw_text_with_background(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, scale=0.5, color=(255, 255, 255), thickness=1, bg_color=(0, 0, 0)):
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    top_left = (position[0], position[1] - text_height - baseline)
    bottom_right = (position[0] + text_width, position[1] + baseline)
    cv2.rectangle(frame, top_left, bottom_right, bg_color, cv2.FILLED)
    cv2.putText(frame, text, position, font, scale, color, thickness)

def gen_frames():
    
    global cap,total_frames,looking_at_camera_frames,emotion
    global total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count
    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        frame = cv2.resize(frame, (683, 384))
        
        # Emotion detection start------------------
        try:
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            emotion = analyze[0].get('dominant_emotion')
            
            total_emotion_count += 1
            if emotion == "angry":
                angry_count += 1
            elif emotion == "disgust":
                disgust_count += 1
            elif emotion == "fear":
                fear_count += 1
            elif emotion == "happy":
                happy_count += 1
            elif emotion == "sad":
                sad_count += 1        
            elif emotion == "surprise":
                surprise_count += 1            
            elif emotion == "neutral":
                neutral_count += 1  
                
            # Draw text with background
            text = f"Emotion: {emotion}"
            draw_text_with_background(frame, text, (30, 170))

        except:
            pass

        # Emotion detection end-----------------

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            eyes_open, eyes_closed, looking_at_camera, left_vertical_gaze, right_vertical_gaze, left_horizontal_gaze, right_horizontal_gaze = analyze_face(landmarks, frame)
            
            total_frames += 1
            if looking_at_camera:
                looking_at_camera_frames += 1

            if eyes_open:
                left_vertical_gaze_status = f"Left Vertical Gaze: {left_vertical_gaze:.2f}"
                right_vertical_gaze_status = f"Right Vertical Gaze: {right_vertical_gaze:.2f}"
                draw_text_with_background(frame, left_vertical_gaze_status, (30, 60))
                draw_text_with_background(frame, right_vertical_gaze_status, (30, 80))

                left_horizontal_gaze_status = f"Left Horizontal Gaze: {left_horizontal_gaze:.2f}"
                right_horizontal_gaze_status = f"Right Horizontal Gaze: {right_horizontal_gaze:.2f}"
                draw_text_with_background(frame, left_horizontal_gaze_status, (30, 100))
                draw_text_with_background(frame, right_horizontal_gaze_status, (30, 120))

                if looking_at_camera:
                    draw_text_with_background(frame, "Eyes Open: Looking at Camera", (30, 30))
                else:
                    draw_text_with_background(frame, "Eyes Open: Not Looking at Camera", (30, 30))
            elif eyes_closed:
                draw_text_with_background(frame, "Eyes Closed", (30, 30))
            
            # for n in range(68):  # Draw all landmarks for better visualization
            #     x = landmarks.part(n).x
            #     y = landmarks.part(n).y
            #     cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





    
