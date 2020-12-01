import traceback
import os
from typing import Dict, List
from flask import Blueprint, jsonify, make_response, request
from termcolor import colored
from werkzeug.utils import secure_filename
from App.Models import Menu, AbstractRegister
from App.Util.helpers import to_dict
from App.Util.constants import BREAKFAST, LUNCH, COLOR_BREAKFAST, COLOR_LUNCH, FILE
from config.uploading_config import MENUS_ALLOWED_EXTENSIONS, UPLOAD_FOLDER, REGISTERS_ALLOWED_EXTENSIONS
from App.Server.data_collector_server import transform_menu_data, transform_register_data, insert_menus, \
    insert_registers
from App.Controllers.request_validators import validate_upload_file_request, validate_insert_data_payload_request

data_collector_blueprint = Blueprint('data_collector', __name__, url_prefix='/data_collector')


@data_collector_blueprint.route('/menu/transform_file', methods=['GET'])
def upload_menu_file():
    allowed_extensions = ' / '.join(MENUS_ALLOWED_EXTENSIONS).upper()
    return f'''
            <!doctype html>
            <title>Upload a menu file with {allowed_extensions} extension</title>
            <h1>Upload a menu file with {allowed_extensions} extension</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name={FILE}>
              <input type=submit value=Upload>
            </form>
            '''


@data_collector_blueprint.route('/register/transform_file', methods=['GET'])
def upload_register_file():
    allowed_extensions = ' / '.join(REGISTERS_ALLOWED_EXTENSIONS).upper()
    return f'''
            <!doctype html>
            <title>Upload a register file with {allowed_extensions} extension</title>
            <h1>Upload a register file with {allowed_extensions} extension</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name={FILE}>
              <input type=submit value=Upload>
            </form>
            '''


@data_collector_blueprint.route('/menu/transform_file', methods=['POST'])
@validate_upload_file_request
def transform_menu_file():
    try:
        file = request.files.get(FILE)
        filename: str = secure_filename(file.filename)
        full_path_file = os.path.join(UPLOAD_FOLDER, filename)
        file.save(full_path_file)

        dict_menus: Dict[str, List[Menu]] = transform_menu_data(full_path_file)
        response: Dict[str, Dict] = {catering: to_dict(menus) for catering, menus in dict_menus.items()}
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
    finally:
        if os.path.exists(full_path_file) and os.path.isfile(full_path_file):
            os.remove(full_path_file)


@data_collector_blueprint.route('/register/transform_file', methods=['POST'])
@validate_upload_file_request
def transform_register_file():
    try:
        file = request.files.get(FILE)
        filename: str = secure_filename(file.filename)
        full_path_file = os.path.join(UPLOAD_FOLDER, filename)
        file.save(full_path_file)

        dict_registers: Dict[str, List[AbstractRegister]] = transform_register_data(full_path_file)
        response: Dict[str, AbstractRegister] = {catering: to_dict(registers) for catering, registers in
                                                 dict_registers.items()}
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
    finally:
        if os.path.exists(full_path_file) and os.path.isfile(full_path_file):
            os.remove(full_path_file)


@data_collector_blueprint.route('/menu/insert', methods=['POST'])
@validate_insert_data_payload_request
def insert_menus_data():
    try:
        breakfast_menus: List[Dict] = request.json.get(BREAKFAST)
        lunch_menus: List[Dict] = request.json.get(LUNCH)

        print(colored('Saving Breakfast menus on the db.', COLOR_BREAKFAST))
        insert_menus(BREAKFAST, breakfast_menus)
        print(colored('Saving Lunch menus on the db.', COLOR_LUNCH))
        insert_menus(LUNCH, lunch_menus)

        return make_response(jsonify({'status': 'ok'}), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@data_collector_blueprint.route('/register/insert', methods=['POST'])
@validate_insert_data_payload_request
def insert_registers_data():
    try:
        breakfast_registers: List[Dict] = request.json.get(BREAKFAST)
        lunch_registers: List[Dict] = request.json.get(LUNCH)

        print(colored('Saving Breakfast registers on the db.', COLOR_BREAKFAST))
        insert_registers(BREAKFAST, breakfast_registers)
        print(colored('Saving Lunch registers on the db.', COLOR_LUNCH))
        insert_registers(LUNCH, lunch_registers)

        return make_response(jsonify({'status': 'ok'}), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
