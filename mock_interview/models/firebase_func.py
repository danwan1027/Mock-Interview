import firebase_admin
from firebase_admin import credentials, firestore, storage
from firebase_admin.firestore import SERVER_TIMESTAMP
from instance import config
from datetime import datetime

firebase_config = {
    "type": config.type,
    "project_id": config.project_id,
    "private_key_id": config.private_key_id,
    "private_key": config.private_key,
    "client_email": config.client_email,
    "client_id": config.client_id,
    "auth_uri": config.auth_uri,
    "token_uri": config.token_uri,
    "auth_provider_x509_cert_url": config.auth_provider_x509_cert_url,
    "client_x509_cert_url": config.client_x509_cert_url,
}

cred = credentials.Certificate(firebase_config)

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred, {"storageBucket": config.storage_bucket})

# 初始化firestore
db = firestore.client()
bucket = storage.bucket()

# Users
# 新增user
def addUser(username, password, email):
    user = {
      "username": username,
      "password": password, 
      "email": email,
      # "profile_image": profile_image
    }
    db.collection("User").add(user)



# Interviews
# 新增interview
def addInterview(college:str, department:str, duration:int, resume, user_id:str):

    interview = db.collection('Interviews').document()

    created_at = interview_date = updated_at = SERVER_TIMESTAMP

    blob = bucket.blob(user_id + '/' + interview.id + '.pdf')
    blob.upload_from_string(resume.read(), content_type='application/pdf')
    blob.make_public()
    resume = blob.public_url

    interview.set({
        'college': college, 
        'created_at': created_at,
        'department': department,
        'duration': duration,
        'interview_date': interview_date,
        'resume': resume,
        'updated_at': updated_at, 
        'user_id': user_id,
    })

    

# def test():
#     a = db.collection('a').document()
#     a.set

def getInterview():
    a = db.collection("Interviews").document("dQMdnLnjNjqhgDVmRlO7").get()
    print(a.to_dict()['created_at'])
    return a


# Emotion_Recognition
# 新增Emotion_Recognition
def addEmotionRecognition(emotion, emotion_suggestion, intensity, interview_id, timestamp=SERVER_TIMESTAMP):
    emo = {
      "emotion": emotion,
      "emotion_suggestion": emotion_suggestion, 
      "intensity": intensity,
      "interview_id": interview_id,
      "timestamp": timestamp,
    }
    db.collection("Emotion_Recognition").add(emo)

# Eye_Gaze_Tracking
# 新增Eye_Gaze_Tracking
def addEyeGaze(duration, eye_contact, gaze_coordinates, gaze_suggestion, interview_id):
    eye_gaze = {
      "duration": duration,
      "eye_contact": eye_contact, 
      "gaze_coordinates": gaze_coordinates,
      "gaze_suggestion": gaze_suggestion,
      "interview_id": interview_id,
    }
    db.collection("Eye_Gaze_Tracking").add(eye_gaze)

# Feedback
# 新增Feedback
def addFeedback(comments, created_at, rating, interview_id, user_id):
    feedback = {
      "comments": comments,
      "created_at": created_at, 
      "rating": rating,
      "interview_id": interview_id,
      "user_id": user_id,
    }
    db.collection("Feedback").add(feedback)


# Question_history
# 新增Question_history
def addQuestionHistory(chatgpt_analysis, question_id, response_date, user_id, user_reponse, user_score):
    history = {
      "chatgpt_analysis": chatgpt_analysis,
      "question_id": question_id, 
      "response_date": response_date,
      "user_id": user_id,
      "user_reponse": user_reponse,
      "user_score": user_score,
    }
    db.collection("Question_history").add(history)


# Voice_Transcriptions
# 新增Emotion_Recognition
def addVoiceTranscriptions(audio_file, speech_speed, transcript, interview_id, timestamp):
    voice = {
      "audio_file": audio_file,
      "speech_speed": speech_speed, 
      "transcript": transcript,
      "interview_id": interview_id,
      "timestamp": timestamp,
    }
    db.collection("Voice_Transcriptions").add(voice)



# Questions
# 新增Questions
def addQuestions(question_create_time, question_department, question_school, interview_id, question_schooldepartment, qusetion_text, user_id):
    question = {
      "interview_id": interview_id,
      "question_create_time": question_create_time,
      "question_department": question_department, 
      "question_school": question_school,
      "question_schooldepartment": question_schooldepartment,
      "qusetion_text": qusetion_text, 
      "user_id": user_id,
    }
    db.collection("Questions").add(question)
