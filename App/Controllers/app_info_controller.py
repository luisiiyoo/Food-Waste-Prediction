
from flask import Blueprint, jsonify, make_response
from App.Server import app_info_server

app_info_blueprint = Blueprint('info', __name__, url_prefix='')


@app_info_blueprint.route('/', methods=['GET'])
def index():
    return "Food Waste Predictions is running!"


@app_info_blueprint.route('/health', methods=['GET'])
def health():
    is_health: bool = app_info_server.is_mongo_client_healthy()
    status = 'pass' if is_health else 'fail'
    return make_response(jsonify({'status': status}), 200)
