import os
from flask import Flask
from flask_cors import CORS
from App.Controllers import app_info_blueprint, dataset_creation_blueprint, preprocessing_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    CORS(app)
    app.register_blueprint(app_info_blueprint)
    app.register_blueprint(dataset_creation_blueprint)
    app.register_blueprint(preprocessing_blueprint)
    return app

