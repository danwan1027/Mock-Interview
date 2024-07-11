from flask import Blueprint

# blueprint in views
from .home import home
from .interview import interview
from .firebase_test import firebase_test

def init_views(app):
    app.register_blueprint(home)
    app.register_blueprint(interview)
    app.register_blueprint(firebase_test)