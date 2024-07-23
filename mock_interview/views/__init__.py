from flask import Blueprint

# blueprint in views
from .home_view import home_view
from .interview import interview
from .firebase_test_view import firebase_test_view
from .GPT.generate_question import generate
from .GPT.rate_advice import rate
from .login_view import login_view

def init_views(app):
    app.register_blueprint(home_view)
    app.register_blueprint(interview)
    app.register_blueprint(firebase_test_view)
    app.register_blueprint(login_view)
    # wstfu blueprint 
    app.register_blueprint(generate)
    app.register_blueprint(rate)