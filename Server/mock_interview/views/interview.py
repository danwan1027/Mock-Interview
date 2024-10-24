from random import randint
from flask import Blueprint, render_template, Response,jsonify, request, url_for, g
import cv2
import os
import dlib
import numpy as np
from deepface import DeepFace
import pdfplumber
import os
from ..models import audio_func as audio
import threading
from flask_login import current_user
from ..models import firebase_func as db
from ..views import frontend_redesign_router as frr
from ..views import generate_question as gq
from ..views import rate_advice as ra
import pyaudio
import wave
import threading
from google.oauth2 import service_account
from google.cloud import speech
# from GPT import generate_question as gq
# from ..models import face_detect

# Set the path for the client file
client_file = 'instance/mock-interview.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials = credentials)

interview = Blueprint('interview', __name__)

views_dir = os.path.dirname(__file__)
resume_path = os.path.join(views_dir, 'resume.pdf')

@interview.route('/test', methods=['POST'])
def test():
    user_id = current_user.id
    department = request.form.get('department')
    school = request.form.get('school')
    resume = request.files.get('resume')
    interview_id = db.addInterview(school, department, 1, resume, user_id)
    db.addEmotionRecognition("sad", "可以更嚴肅並且減少展現緊張的情緒", "test", interview_id, 100, 10, 20, 20, 10, 10, 10, 20)
    db.addEyeGaze(1, True, "focus", "可以更專注地看面試官，建議不要有過多的眼神迴避", interview_id, 40)
    db.addFeedback("總體來說表現還是不錯的，可以在多提升自己的專注度，在專業知識方面也回答得不錯", 75, interview_id, user_id)
    
    #呼叫 fronted_redesign_route.py 的 interviewReview function
    return frr.interviewReview(interview_id)
    
    
@interview.route('/interview')
def index():
    return render_template('interview.html')

class AudioRecorder:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.frames = []
            self.thread = threading.Thread(target=self._record)
            self.thread.start()
            return True
        return False

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.thread.join()
            self._save_audio()

            audio_data = b''.join(self.frames)

            audio = speech.RecognitionAudio(content=audio_data)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code='cmn-Hant-TW',
                enable_automatic_punctuation=True
            )

            response = client.recognize(config=config, audio=audio)
            if response.results:
                recorded = response.results[0].alternatives[0].transcript
                print("Recorded Text: " + recorded, flush=True)
                
                user_id = request.json.get('user_id')
                interview_id = request.json.get('interview_id')
                question_id = request.json.get('question_id')
                questionText = request.json.get('questionText')

                # 將使用者的回答給gpt獲得建議和評分
                gpt_analysis = ra.gen_record_advice(recorded, questionText)
                score = randint(60, 100)

                # 新增至資料庫
                history_id = db.addQuestionHistory(gpt_analysis, question_id, user_id, recorded, score, interview_id)
                db.addVoiceTranscriptions(len(recorded.split()), recorded, history_id)
            return recorded
        return "False"

    def _record(self):
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()

    def _save_audio(self):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

recorder = AudioRecorder()

@interview.route('/start_recording')
def start_recording():
    if recorder.start_recording():
        return jsonify({"status": "Recording started"})
    return jsonify({"status": "Already recording"})

@interview.route('/stop_recording', methods=['POST'])
def stop_recording():
    record_text = recorder.stop_recording()
    return jsonify({"record_text": record_text})



def convert(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

@interview.route('/next_question', methods=['POST'])
def nextQuestion():
    # user_id = current_user.id
    user_id = request.form.get('user_id')
    department = request.form.get('department')
    school = request.form.get('school')
    interview_id = request.form.get('interview_id')
    resume = request.files.get('resume')
    count = request.form.get('count')
    # count string to int
    count = int(count)
    
    # 追問
    question_text = request.form.get('question_text')
    response = request.form.get('response')
    askbool = request.form.get('askbool')
    
    if(askbool == "false"):
        question = gq.answer_question(question_text, response, school, department)
    # elif(count == 1):
        # question = gq.gensecond_question(school, department)
        # question = "請問你認為清大的工業工程與管理學系有什麼吸引你的特質？"
    elif(count == 1):
        question = gq.genthird_question(resume)
        # question = "你在履歷中提到了你在工業工程與管理學系的經驗，可以談談你的經驗嗎？"
    # elif(count == 3 or count == 4):
        # question = gq.history_question("國立清華大學", "工業工程與管理學系", count-3)
        # question = "此題將在資料庫中自動搜索"
    
    question_id = db.addQuestions(department, school, interview_id, school + department, question, user_id)
    
    return jsonify({"question_id": question_id, "question": question, "askbool": askbool})


@interview.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@interview.route('/start_camera', methods=['POST'])
def start_camera():
    count = request.args.get('count')
    global cap
    cap = cv2.VideoCapture(0)
    # user_id = current_user.id
    user_id = request.form.get('user_id')
    department = request.form.get('department')
    school = request.form.get('school')
    resume = request.files.get('resume')
    interview_id = db.addInterview(school, department, 1, resume, user_id)
    
    # interview_id = db.addInterview(school, department, 1, resume_content, user_id)
    # interview_id = "bQWxr4ucsCpU5WJ1Ovyv"
    
    # 產生第一個問題
    question = gq.gensecond_question(school, department)
    # question = "請問你認為工業工程與管理學系能為社會帶來什麼？"
    schooldepartment = f"{school}{department}"
    question_id = db.addQuestions(department, school, interview_id, schooldepartment, question, user_id)
    
    return jsonify({"interview_id": interview_id, "question_id": question_id, "question": question})
    
@interview.route('/end_interview', methods=['POST'])
def end_interview():
    global cap, total_emotion_count, angry_count, disgust_count, fear_count, happy_count, sad_count, surprise_count, neutral_count, total_frames, looking_at_camera_frames
    if cap:
        cap.release()
        cap = None
    
    
    interview_id = request.json.get('interviewId')
    # user_id = current_user.id # 使用current_user.id取得當前使用者的id
    user_id = request.json.get('user_id')
    department = request.json.get('department')
    school = request.json.get('school')
    schooldepartment = f"{school}{department}"
    
    print(user_id)
    print(department)
    print(school)
    print(schooldepartment)
    
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
    
    # 把stats每個參數轉string
    str_total_emotion_count = str(stats['total_emotion_count'])
    str_angry_percent = str(stats['angry_percent'])
    str_disgust_percent = str(stats['disgust_percent'])
    str_fear_percent = str(stats['fear_percent'])
    str_happy_percent = str(stats['happy_percent'])
    str_sad_percent = str(stats['sad_percent'])
    str_surprise_percent = str(stats['surprise_percent'])
    str_neutral_percent = str(stats['neutral_percent'])
    str_percentage_looking_at_camera = str(stats['percentage_looking_at_camera'])
    
    

    # genearate advice
    emotion_advice = ra.gen_emotion_advice(str_total_emotion_count, str_angry_percent, str_disgust_percent, str_fear_percent, str_happy_percent, str_sad_percent, str_surprise_percent, str_neutral_percent)
    eye_gaze_advice = ra.gen_eye_gaze_advice(str_percentage_looking_at_camera)
    # final_advice = ra.gen_final_advice(emotion_advice, eye_gaze_advice)
    # emotion_advice = "可以以更嚴肅但不失親切的態度面對，且更好的把緊張和恐懼的心理隱藏起來"
    # eye_gaze_advice = "可以更專注地看面試官，建議不要有過多的眼神迴避，聽取面試官的問題時可以看著面試官的眼睛"
    final_advice = "總體來說表現還是不錯的，可以在多提升自己的專注度，在專業知識方面也回答得不錯"
    
    feedback_rate = randint(70, 100)
    
    
    #完成面試後將資料上傳到資料庫
    ##---------上傳資料庫---------
    db.addEmotionRecognition(stats['total_emotion_count'], emotion_advice, stats['percentage_looking_at_camera'], interview_id, stats['total_emotion_count'], stats['angry_percent'], stats['disgust_percent'], stats['fear_percent'], stats['happy_percent'], stats['sad_percent'], stats['surprise_percent'], stats['neutral_percent'])
    db.addEyeGaze(1, True, "test", eye_gaze_advice, interview_id, stats['percentage_looking_at_camera'])
    db.addFeedback(final_advice, feedback_rate, interview_id, user_id)
    ##---------上傳資料庫---------
    
    return stats

    
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
        frame = cv2.flip(frame, 1)
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





    
