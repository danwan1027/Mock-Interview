import requests
import json
from flask import Blueprint, render_template, request
from models import firebase_func as ff

rate = Blueprint('rate', __name__)

@rate.route('/rate')
def rate_addvice():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        text = txt(file)
        addvice = genaddvice(text)
        score = pt.genscore(text)
        return render_template('/wstfu/score.html', addvice = addvice, score = score)
    else:
        return 'Error processing file', 500
    
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


# 生成建議
def genaddvice(text):
    endpoint = "https://api.openai.com/v1/completions"
    prompt = "請幫我對這個學生的面試回答給出回答方面的建議，告訴他那些地方可以改進，並且用繁體中文回答且在200token內完成，以下是學生的回答:" + text
    headers = {
        "Content-Type": "application/json",
        #"API-KEY" over here
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