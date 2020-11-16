import os
from flask import Blueprint, jsonify, make_response, request, flash, redirect, url_for, send_from_directory
from App.Server import app_info_server
from werkzeug.utils import secure_filename
from config.upload_files import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, UPLOAD_TEMP_NAME

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@preprocessing_blueprint.route('/transform-data', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename: str = secure_filename(file.filename)
            *_, extension = os.path.splitext(filename)

            filename = f'{UPLOAD_TEMP_NAME}{extension}'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('preprocessing.uploaded_file', filename=filename))
    allowed_extensions = ' / '.join(ALLOWED_EXTENSIONS).upper()
    return f'''
    <!doctype html>
    <title>Upload a {allowed_extensions} file</title>
    <h1>Upload a {allowed_extensions} file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@preprocessing_blueprint.route('/uploads/<string:filename>')
def uploaded_file(filename: str):
    return "Holas"
