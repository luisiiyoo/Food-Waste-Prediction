import traceback
from flask import Blueprint, jsonify, make_response, request
from App.Server import dataset_creation_server

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='/preprocessing')

FILE_KEY = 'file'
FILE_TYPE_KEY = 'fileType'
CATERING = 'catering'


@preprocessing_blueprint.route('/menu-bow/build', methods=['POST'])
def build_menu_bow():
    try:
        catering = request.json.get(CATERING)
        if catering is None:
            return jsonify({'error': f"No '{CATERING}' field was provided"}), 400

        data = dataset_creation_server.build_menus_bow_model(catering)
        return make_response(jsonify(data), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
