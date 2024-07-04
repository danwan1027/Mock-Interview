from flask import Blueprint, render_template, request, redirect, url_for
from ..models import firebase_func as db

firebase_test = Blueprint('firebase_test', __name__)

@firebase_test.route('/firebase')
def firebase():
    # db.test()
    return render_template('firebase_test.html')

@firebase_test.route('/upload', methods=['GET', 'POST'])
def upphoto():
    file = request.files['pdfFile']
    db.addInterview("a", "a", 1, file, "ascsa")
    return 'success'

@firebase_test.route('/adduser', methods=['GET', 'POST'])
def adduser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    db.addUser(username, password, email)
    return redirect('/firebase')