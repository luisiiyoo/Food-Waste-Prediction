import traceback
import os
import shutil
from flask import Blueprint, jsonify, make_response, request, flash, redirect, url_for, send_from_directory
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
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename: str = secure_filename(file.filename)
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
    try:
        dir_file = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Exists {dir_file}: {os.path.exists(dir_file)}")
    except Exception as e:
        traceback.print_exc()
    finally:
        if os.path.exists(UPLOAD_FOLDER) and os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
    return "Holas"
