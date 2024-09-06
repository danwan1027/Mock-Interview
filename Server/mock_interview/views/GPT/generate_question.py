import random
import pdfplumber
import requests
import json
import os
from flask import Blueprint, render_template, request, jsonify
from ...models import firebase_func as db
# from models import firebase_func as ff
from dotenv import load_dotenv

load_dotenv()

generate = Blueprint('generate', __name__)

@generate.route('/generate', methods=['POST'])
def generate_question():
    # 這邊應該要有一個檢查是否有登入的function
    # 以下是確定登入使用者
    # user_id = request.form['user_id']
    
    # 選擇校系
    ################
    ################
    ################
    ################
    department = request.form['department']
    school = request.form['school']
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        text = convert(file)
        genfirstquestion = genfirst_question(text, school, department)
        gensecondquestion = gensecond_question(text, school, department)
        genthirdquestion = genthird_question(text, school, department)
        history_question_sd = history_question(school, department, 1)
        history_question_d = history_question(school, department, 2)
        if genfirstquestion & gensecondquestion & genthirdquestion & history_question_sd & history_question_d:
            return jsonify({'first_question': genfirstquestion, 'second_question': gensecondquestion, 'third_question': genthirdquestion, 'four_question': history_question_sd, 'five_question': history_question_d}), 200
        else:
            return jsonify({'error': 'Error generating questions'}), 500
    else:
        return jsonify({'error': 'Error processing file'}), 500


# 將pdf檔案轉換成文字
def convert(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text
    
    
def load_genquestion_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(current_dir, 'prompt.json')

    with open(prompts_path, 'r', encoding='utf-8') as file:
        prompts = json.load(file)
    return prompts

# 生成第一個問題，跟系所有關
def genfirst_question(school):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    prompt = prompts["first_question"] + school
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


# 生成第二個問題，跟學校系所有關
def gensecond_question(school, department):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    prompt = prompts["second_question"] + school + department
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
    

# 生成第三個問題
def genthird_question(file):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    text = convert(file)
    prompt = prompts["third_question"] + text
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
    

# 生成四五個問題，從資料庫裡拿之前有出現的問題
def history_question(school, department, n):
    schooldepartment = school + department
    if(n == 1):
        question = db.getQuestionBySchoolD(schooldepartment)
    if(n == 2):
        question = db.getQuestionByDepartment(department)
    # random選所有題目中的其中一個
    if question:
        selected_question = random.choice(question)
        return selected_question
    else:
        return "None"
    
    
# 根據前一題的回答再生成新的問題
def genanswer_question(question, response, school, department):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    prompt = prompts["answer_question"] + school + department
    prompt += "，這是前一題的題目: " + question
    prompt += "，這是使用者根據上一題題目的回答: " + response
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