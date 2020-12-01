import traceback
from flask import Blueprint, jsonify, make_response, request
from App.Server import preprocessor_server
from App.Util.constants import CATERING
from App.Server import dataset_creator_server
from App.Controllers.request_validators import validate_catering_in_payload_request

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='/preprocessing')


@preprocessing_blueprint.route('/menu/bow/build', methods=['POST'])
@validate_catering_in_payload_request
def build_menu_bow():
    try:
        catering = request.json.get(CATERING)
        time_elapsed, features = preprocessor_server.build_menus_bow_model(catering)
        response = {
            "time": f"{round(time_elapsed, 4)} sec",
            "features": features
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@preprocessing_blueprint.route('/menu/bow/features', methods=['POST'])
@validate_catering_in_payload_request
def get_menu_bow_features():
    try:
        catering = request.json.get(CATERING)
        features, stemmed_words_features = preprocessor_server.get_bow_features(catering)
        response = {
            "features": features,
            "stemmedWordsFeatures": {feature: list(set_words) for feature, set_words in stemmed_words_features.items()}
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@preprocessing_blueprint.route('/create-dataset', methods=['POST'])
@validate_catering_in_payload_request
def create_dataset():
    try:
        catering = request.json.get(CATERING)
        time_elapsed = dataset_creator_server.merge_datasets(catering)
        response = {
            "saved": "ok",
            "time": f"{round(time_elapsed, 4)} sec",
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
