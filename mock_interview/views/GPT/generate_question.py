import pdfplumber
import requests
import json
from flask import Blueprint, render_template, request
from models import firebase_func as ff

generate = Blueprint('generate', __name__)

@generate.route('/generate')
def generate_question():
    # 這邊應該要有一個檢查是否有登入的function
    # 以下是確定登入使用者
    # user_id = request.form['user_id']
    
    # 選擇校系
    ################
    ################
    ################
    ################
    # 上傳履歷
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        text = convert(file)
        generated_question = genquestion(text)
        if generated_question:
            # 儲存到資料庫
            ff.addQuestions(
                question_department="資訊管理學系",  # 可以根据你的需求设置
                question_school="國立中央大學",     # 可以根据你的需求设置
                #待更改
                interview_id = 1,        # 可以根据你的需求设置
                question_schooldepartment="國立中央大學, 資訊管理學系",  # 可以根据你的需求设置
                qusetion_text=generated_question,
                user_id = 1
            )
            return render_template('result.html', generated_question=generated_question)
        else:
            return 'Error generating questions', 500
    else:
        return 'Error processing file', 500


# 將pdf檔案轉換成文字
def convert(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def genquestion(text):
    endpoint = "https://api.openai.com/v1/completions"
    prompts = load_genquestion_prompt()
    prompt = prompts["sc_dep_resume_question"] + text
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
    
    
def load_genquestion_prompt():
    with open('prompts.json', 'r', encoding='utf-8') as file:
        prompts = json.load(file)
    return prompts