import os
from flask import Flask
from flask_cors import CORS
from App.Controllers import app_info_blueprint, data_collector_blueprint, preprocessing_blueprint, predictor_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    CORS(app)
    app.register_blueprint(app_info_blueprint)
    app.register_blueprint(data_collector_blueprint)
    app.register_blueprint(preprocessing_blueprint)
    app.register_blueprint(predictor_blueprint)
    return app

