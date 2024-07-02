from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # config
    app.config.from_object('config.development')
    # app.config.from_object('config.product')
    app.config.from_pyfile('config.py')
    
    # blueprint
    from .views import init_views
    init_views(app)
    
    return app