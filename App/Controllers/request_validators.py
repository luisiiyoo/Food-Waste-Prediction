import os
from typing import Dict, List
from flask import jsonify, make_response, request
from App.Util.constants import BREAKFAST, LUNCH, FILE, MENU, CATERING
from config.uploading_config import MENUS_ALLOWED_EXTENSIONS, UPLOAD_FOLDER, REGISTERS_ALLOWED_EXTENSIONS


def validate_catering_in_payload_request(func):
    def wrapper():
        try:
            caterings_opts = (BREAKFAST, LUNCH)
            catering = request.json.get(CATERING)
            if catering is None:
                return jsonify({'error': f"No '{CATERING}' field was provided"}), 400
            if catering not in caterings_opts:
                return jsonify(
                    {'error': f"'{catering}' is an invalid catering. Catering options: {caterings_opts}"}), 400
            return func()
        except AttributeError:
            return jsonify({'error': f"No '{CATERING}' field was provided"}), 400

    wrapper.__name__ = func.__name__
    return wrapper


def validate_upload_file_request(func):
    def wrapper():
        try:
            extensions = MENUS_ALLOWED_EXTENSIONS if str(request.url).find(MENU) != -1 \
                else REGISTERS_ALLOWED_EXTENSIONS
            file = request.files.get(FILE)
            if FILE not in request.files:
                return jsonify({'error': f"No '{FILE}' field was provided in the form-data request."}), 400
            if not file or file.filename == '':
                return jsonify({'error': f"No selected file."}), 400
            if not is_allowed_file(file.filename, extensions):
                allowed_extensions = ' or '.join(extensions).lower()
                return jsonify({'error': f"Please upload a valid file with {allowed_extensions} extension."}), 400
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            return func()
        except AttributeError:
            return jsonify({'error': f"No '{FILE}' field was provided in the form-data request."}), 400

    wrapper.__name__ = func.__name__
    return wrapper


def validate_insert_data_payload_request(func):
    def wrapper():
        breakfast: List[Dict] = request.json.get(BREAKFAST)
        lunch: List[Dict] = request.json.get(LUNCH)
        if breakfast is None:
            return make_response(jsonify({'error': f"No '{BREAKFAST}' field was provided in the request."}), 400)
        if lunch is None:
            return make_response(jsonify({'error': f"No '{LUNCH}' field was provided in the request."}), 400)
        return func()

    wrapper.__name__ = func.__name__
    return wrapper


def is_allowed_file(filename: str, extensions: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
