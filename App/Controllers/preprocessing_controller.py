import traceback
import os
from flask import Blueprint, jsonify, make_response, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from config.upload_files import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from App.Util import constants

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='')

FILE_KEY = 'file'
FILE_TYPE_KEY = 'fileType'


def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@preprocessing_blueprint.route('/transform-data', methods=['GET'])
def transform_file_page():
    allowed_extensions = ' / '.join(ALLOWED_EXTENSIONS).upper()
    return f'''
            <!doctype html>
            <title>Upload a {allowed_extensions} file</title>
            <h1>Upload a {allowed_extensions} file</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name={FILE_KEY}>
              <input type=submit value=Upload>
            </form>
            '''


@preprocessing_blueprint.route('/transform_data_file', methods=['POST'])
def transform_data_file():
    file = request.files.get(FILE_KEY)
    if FILE_KEY not in request.files:
        return jsonify({'error': f"No '{FILE_KEY}' field was provided on the form-data request."}), 400
    if not file or file.filename == '':
        return jsonify({'error': f"No selected file."}), 400
    if not is_allowed_file(file.filename):
        allowed_extensions = ' or '.join(ALLOWED_EXTENSIONS).lower()
        return jsonify({'error': f"Please upload a valid file with {allowed_extensions} extension."}), 400
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filename: str = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        file_type: str = request.form.get(FILE_TYPE_KEY)
        file_type = file_type.lower() if file_type else file_type
        if file_type not in constants.FILE_TYPES:
            return make_response(jsonify({'error': f"No '{FILE_TYPE_KEY}' field was provided on the form-data"
                                                   f" request. Available types are: {constants.FILE_TYPES}."}), 400)
        else:
            # call funtion to extract the data
            return file_type
    except Exception as e:
        traceback.print_exc()
    finally:
        full_path_file = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(full_path_file) and os.path.isfile(full_path_file):
            os.remove(full_path_file)
