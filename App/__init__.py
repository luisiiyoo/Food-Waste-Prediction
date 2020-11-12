from flask import Flask
from flask_cors import CORS
from App.Controllers import app_info_controller


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(app_info_controller)
    return app

