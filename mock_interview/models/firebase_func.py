import firebase_admin
from firebase_admin import credentials, firestore, storage
from firebase_admin.firestore import SERVER_TIMESTAMP
from instance import config
from typing import List

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

# 刪除user
def delUser(user_id:str):
    user = db.collection('User').document(user_id)
    user.delete()

def getUserID(email):
    docs = db.collection('User').where('email', '==', email).stream()
    for doc in docs:
        print('{} => {}'.format(doc.id, doc.to_dict()))





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

# 刪除interview
def delInterview(interview_id:str):
    interview = db.collection('Interviews').document(interview_id)
    interview.delete()

    

# def test():
#     a = db.collection('a').document()
#     a.set

def getInterview():
    a = db.collection("Interviews").document("dQMdnLnjNjqhgDVmRlO7").get()
    print(a.to_dict()['created_at'])
    return a


# Emotion_Recognition
# 新增Emotion_Recognition
def addEmotionRecognition(emotion:str, emotion_suggestion:str, intensity:str, interview_id:str):

    emo = db.collection('Emotion_Recognition').document()
    timestamp = SERVER_TIMESTAMP

    emo.set({
        "emotion": emotion,
        "emotion_suggestion": emotion_suggestion, 
        "intensity": intensity,
        "interview_id": interview_id,
        "timestamp": timestamp,
    })

# 刪除Emotion_Recognition
def delEmotionRecognition(Emotion_Recognition_id:str):
    emo = db.collection('Emotion_Recognition').document(Emotion_Recognition_id)
    emo.delete()

# Eye_Gaze_Tracking
# 新增Eye_Gaze_Tracking
def addEyeGaze(duration:int, eye_contact:bool, gaze_coordinates:str, gaze_suggestion:str, interview_id:str):

    eye_gaze = db.collection('Eye_Gaze_Tracking').document()

    eye_gaze.set({
        "duration": duration,
        "eye_contact": eye_contact, 
        "gaze_coordinates": gaze_coordinates,
        "gaze_suggestion": gaze_suggestion,
        "interview_id": interview_id,
    })

# 刪除Eye_Gaze_Tracking
def delEyeGaze(eye_gaze_id:str):
    eye_gaze = db.collection('Eye_Gaze_Tracking').document(eye_gaze_id)
    eye_gaze.delete()


# Feedback
# 新增Feedback
def addFeedback(comments:str, rating:int, interview_id:str, user_id:str):

    feedback = db.collection('Feedback').document()
    created_at = SERVER_TIMESTAMP

    feedback.set({
        "comments": comments,
        "created_at": created_at, 
        "rating": rating,
        "interview_id": interview_id,
        "user_id": user_id,
    })

# 刪除Feedback
def delFeedback(feedback_id:str):
    feedback = db.collection('Feedback').document(feedback_id)
    feedback.delete()


# Question_history
# 新增Question_history
def addQuestionHistory(chatgpt_analysis:str, question_id:str, user_id:str, user_reponse:str, user_score:int):

    history = db.collection('Question_history').document()
    response_date = SERVER_TIMESTAMP

    history.set({
        "chatgpt_analysis": chatgpt_analysis,
        "question_id": question_id, 
        "response_date": response_date,
        "user_id": user_id,
        "user_reponse": user_reponse,
        "user_score": user_score,
    })

# 刪除Question_history
def delQuestionHistory(history_id:str):
    history = db.collection('Question_history').document(history_id)
    history.delete()


# Voice_Transcriptions
# 新增Emotion_Recognition
def addVoiceTranscriptions(audio_file, speech_speed:List[int], transcript:str, interview_id:str):

    voice = db.collection('Voice_Transcriptions').document()
    timestamp = SERVER_TIMESTAMP

    voice.set({
        "audio_file": audio_file,
        "speech_speed": speech_speed, 
        "transcript": transcript,
        "interview_id": interview_id,
        "timestamp": timestamp,
    })

# 刪除Voice_Transcriptions
def delVoiceTranscriptions(voice_id:str):
    voice = db.collection('Voice_Transcriptions').document(voice_id)
    voice.delete()



# Questions
# 新增Questions
def addQuestions(question_department:str, question_school:str, interview_id:str, question_schooldepartment:str, qusetion_text:str, user_id:str):
    
    question = db.collection('Voice_Transcriptions').document()
    question_create_time = SERVER_TIMESTAMP

    question.set({
        "interview_id": interview_id,
        "question_create_time": question_create_time,
        "question_department": question_department, 
        "question_school": question_school,
        "question_schooldepartment": question_schooldepartment,
        "qusetion_text": qusetion_text, 
        "user_id": user_id,
    })

# 刪除Questions
def delQuestions(question_id:str):
    question = db.collection('Questions').document(question_id)
    question.delete()
    
