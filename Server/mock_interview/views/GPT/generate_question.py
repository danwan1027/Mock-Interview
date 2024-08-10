import pdfplumber
import requests
import json
import os
from flask import Blueprint, render_template, request, jsonify
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
        generated_question = genquestion(text, school, department)
        # generated_question = "test"
        if generated_question:
            return jsonify({'generated_question': generated_question})
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

def genquestion(text, school, department):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    prompt = prompts["sc_dep_resume_question"] + "\n"
    prompt += "以下是面試者欲申請的學校: " + school + "\n"
    prompt += "以下是面試者欲申請的系所: " + department + "\n"
    prompt += "以下是面試者的自我介紹: " + text
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
    
    
def load_genquestion_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(current_dir, 'prompt.json')

    with open(prompts_path, 'r', encoding='utf-8') as file:
        prompts = json.load(file)
    return prompts