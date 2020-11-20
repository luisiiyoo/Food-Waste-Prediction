import traceback
import os
from typing import Dict
from flask import Blueprint, jsonify, make_response, request
from werkzeug.utils import secure_filename
from config.upload_files import MENUS_ALLOWED_EXTENSIONS, UPLOAD_FOLDER, REGISTERS_ALLOWED_EXTENSIONS
from App.Server import preprocessing_server

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='')

FILE_KEY = 'file'
FILE_TYPE_KEY = 'fileType'


def validate_upload_file_request(func):
    def wrapper():
        extensions = MENUS_ALLOWED_EXTENSIONS if str(request.url).find('menu') != -1 else REGISTERS_ALLOWED_EXTENSIONS
        file = request.files.get(FILE_KEY)
        if FILE_KEY not in request.files:
            return jsonify({'error': f"No '{FILE_KEY}' field was provided on the form-data request."}), 400
        if not file or file.filename == '':
            return jsonify({'error': f"No selected file."}), 400
        if not is_allowed_file(file.filename, extensions):
            allowed_extensions = ' or '.join(extensions).lower()
            return jsonify({'error': f"Please upload a valid file with {allowed_extensions} extension."}), 400
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        return func()

    wrapper.__name__ = func.__name__
    return wrapper


def is_allowed_file(filename: str, extensions: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@preprocessing_blueprint.route('/menu/transform_file', methods=['GET'])
def upload_menu_file():
    allowed_extensions = ' / '.join(MENUS_ALLOWED_EXTENSIONS).upper()
    return f'''
            <!doctype html>
            <title>Upload a menu file with {allowed_extensions} extension</title>
            <h1>Upload a menu file with {allowed_extensions} extension</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name={FILE_KEY}>
              <input type=submit value=Upload>
            </form>
            '''


@preprocessing_blueprint.route('/menu/transform_file', methods=['POST'])
@validate_upload_file_request
def transform_menu_file():
    try:
        file = request.files.get(FILE_KEY)
        filename: str = secure_filename(file.filename)
        full_path_file = os.path.join(UPLOAD_FOLDER, filename)
        file.save(full_path_file)

        data_transformed: Dict[str, Dict] = preprocessing_server.transform_menu_data(full_path_file)
        return make_response(jsonify(data_transformed), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
    finally:
        if os.path.exists(full_path_file) and os.path.isfile(full_path_file):
            os.remove(full_path_file)


@preprocessing_blueprint.route('/register/transform_file', methods=['GET'])
def upload_register_file():
    allowed_extensions = ' / '.join(REGISTERS_ALLOWED_EXTENSIONS).upper()
    return f'''
            <!doctype html>
            <title>Upload a register file with {allowed_extensions} extension</title>
            <h1>Upload a register file with {allowed_extensions} extension</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name={FILE_KEY}>
              <input type=submit value=Upload>
            </form>
            '''


@preprocessing_blueprint.route('/register/transform_file', methods=['POST'])
@validate_upload_file_request
def transform_register_file():
    try:
        file = request.files.get(FILE_KEY)
        filename: str = secure_filename(file.filename)
        full_path_file = os.path.join(UPLOAD_FOLDER, filename)
        file.save(full_path_file)

        data_transformed: Dict[str, Dict] = preprocessing_server.transform_register_data(full_path_file)
        return make_response(jsonify(data_transformed), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
    finally:
        if os.path.exists(full_path_file) and os.path.isfile(full_path_file):
            os.remove(full_path_file)
