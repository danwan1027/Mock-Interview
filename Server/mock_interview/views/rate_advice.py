import requests
import json
import os
from flask import Blueprint, render_template, request
# from models import firebase_func as ff
from dotenv import load_dotenv
from ..models import firebase_func as db

load_dotenv()

rate = Blueprint('rate', __name__)

@rate.route('/rate_advice', methods=['POST'])
def rate_advice():
    data = request.get_json()
    
    
    # 假設你有一個函數用於根據數據進行分析和評分
    # advice_score = analyze_and_rate(data)
    # audio_advice = gen_audio_advice(data)
    # view_advice = gen_view_advice(data)
    # emotion_advice = gen_view_advice(data) # gen_emotion_advice(data)才是對的，先用view_advice代替
    # 也可以是結合分析面試回答和面試情緒的函數的評論後再總結
    #但因為太花錢了所以先直接分析一次
    # final_advice = gen_final_advice(audio_advice, view_advice, data)
    final_advice = gen_final_advice(data)
    # interview_score = gen_score(final_advice)
    
    ######## test省token ##########
    audio_advice = "test"
    view_advice = "test"
    emotion_advice = "test"
    # final_advice = "test"
    interview_score = 75
    ###############################
    
    
    #上傳結果至資料庫
    db.addEmotionRecognition(data['stats']['total_emotion_count'], emotion_advice, data['stats']['percentage_looking_at_camera'], data['interview_id'])
    db.addEyeGaze(1, True, data['stats']['percentage_looking_at_camera'], view_advice, data['interview_id'])
    #db.addVoiceTranscriptions(None, None, audio_advice, data['interview_id'])
    db.addFeedback(final_advice, interview_score, data['interview_id'], data['user_id'])
    db.addQuestionHistory(final_advice, data['question_id'], data['user_id'], data['audio_results']['accumulated_transcript'], interview_score)

    
    
    # 渲染一個新的模板頁面來顯示結果
    return render_template('result.html', advice = final_advice, score = interview_score)


# 題目回答的分析
def gen_record_advice(text, question_text):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["record_advice"] + question_text
    prompt += "，以下是面試者的回答: " + text
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 200
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None



# 生成建議
def gen_final_advice(stat):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["interview_advice"] + stat['audio_results']['accumulated_transcript'] + "，以下是各個狀態的分數: "
    prompt += "憤怒的情緒: " + str(stat['stats']['angry_percent']) + "%"
    prompt += "，噁心的情緒: " + str(stat['stats']['disgust_percent']) + "%"
    prompt += "，高興的情緒: " + str(stat['stats']['happy_percent']) + "%"
    prompt += "，驚訝的情緒: " + str(stat['stats']['surprise_percent']) + "%"
    prompt += "，恐懼的情緒: " + str(stat['stats']['fear_percent']) + "%"
    prompt += "，悲傷的情緒: " + str(stat['stats']['sad_percent']) + "%"
    prompt += "，中性的情緒: " + str(stat['stats']['neutral_percent']) + "%"
    prompt += "以下是面試者的專注程度: " + str(stat['stats']['percentage_looking_at_camera']) + "%"
    prompt += "。請根據你認為一個面試者應該有的態度和情緒和該有的專注度來給予評價。"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 200
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None

# 生成回答內容的建議
def gen_audio_advice(stat):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["audio_advice"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 200
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None


# 生成對於面試情緒、狀態的建議
def gen_view_advice(stat):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["view_advice"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 200
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None


# 生成整體面試的分數
def gen_score(advice):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = advice + " " + prompts["interview_score"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 20
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None
    
    
# 生成整體回答內容的建議
def gen_allanswer_advice(question1, question2, answer1, answer2):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["allanswer_advice"] + question1 + "，以下是面試者對第一題的回答: " + answer1
    prompt += "，以下是面試的第二題題目: " + answer2 + "，以下是面試者對第二題的問題: " + question2
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 100
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None
    
    
# 生成面試情緒的建議
def gen_emotion_advice(total_emotion_count, angry_percent, disgust_percent, fear_percent, happy_percent, sad_percent, surprise_percent, neutral_percent):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["emotion_advice"] + total_emotion_count
    prompt += "，憤怒的情緒: " + angry_percent + "%"
    prompt += "，噁心的情緒: " + disgust_percent + "%"
    prompt += "，恐懼的情緒: " + fear_percent + "%"
    prompt += "，高興的情緒: " + happy_percent + "%"
    prompt += "，悲傷的情緒: " + sad_percent + "%"
    prompt += "，驚訝的情緒: " + surprise_percent + "%"
    prompt += "，中性的情緒: " + neutral_percent + "%"
    prompt += "。請根據你認為一個面試者應該有的情緒來給予評價，不一定要給出正面的評價，多以檢討錯誤的態度。"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 100
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None



# 生成眼睛專注的建議
def gen_eye_gaze_advice(percentage_looking_at_camera):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genadvice_prompt()
    prompt = prompts["eye_gaze"] + percentage_looking_at_camera + "%"
    prompt += "。請根據你認為一個面試者應該有的專注度來給予評價，若低於75%的專注度就是不夠專注，低於60%就要給予嚴厲的批評。"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 100
    }
    
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        error_message = f"Failed to retrieve data: Status code {response.status_code}, Response: {response.text}"
        print(error_message)
        return None


# 載入生成建議的prompt
def load_genadvice_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(current_dir, 'prompt.json')

    with open(prompts_path, 'r', encoding='utf-8') as file:
        prompts = json.load(file)
    return prompts



# 將txt檔案轉換成文字
# 不用管這段，這是把語音轉成txt之後再把txt轉成文字   
def txt(file_path):
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        text = file.read().decode("utf-8")
        return text
