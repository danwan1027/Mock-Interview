import requests
import json
import os
from flask import Blueprint, render_template, request
# from models import firebase_func as ff
from dotenv import load_dotenv

load_dotenv()

rate = Blueprint('rate', __name__)

@rate.route('/rate_advice', methods=['POST'])
def rate_advice():
    data = request.get_json()
    
    
    # 假設你有一個函數用於根據數據進行分析和評分
    # advice_score = analyze_and_rate(data)
    audio_advice = gen_audio_advice(data)
    view_advice = gen_view_advice(data)
    
    # 也可以是結合分析面試回答和面試情緒的函數的評論後再總結
    #但因為太花錢了所以先直接分析一次
    # final_advice = gen_final_advice(audio_advice, view_advice, data)
    final_advice = gen_final_advice(data)
    interview_score = gen_score(final_advice)
    
    
    # 渲染一個新的模板頁面來顯示結果
    return render_template('result.html', advice = final_advice, score = interview_score)



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