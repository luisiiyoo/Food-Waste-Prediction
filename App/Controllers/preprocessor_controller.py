import traceback
from flask import Blueprint, jsonify, make_response, request
from App.Server import preprocessor_server
from App.Util import BREAKFAST, LUNCH
from App.Server import dataset_creator_server

preprocessing_blueprint = Blueprint('preprocessing', __name__, url_prefix='/preprocessing')

FILE_KEY = 'file'
FILE_TYPE_KEY = 'fileType'
CATERING = 'catering'


def validate_bow_payload_request(func):
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


@preprocessing_blueprint.route('/menu/bow/build', methods=['POST'])
@validate_bow_payload_request
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
@validate_bow_payload_request
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
@validate_bow_payload_request
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
