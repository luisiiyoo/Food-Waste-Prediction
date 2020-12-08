import traceback
from typing import Dict, List
from flask import Blueprint, jsonify, make_response, request
from App.Controllers.request_validators import validate_catering_in_payload_request
from App.Util.constants import CATERING, BREAKFAST, LUNCH
from App.Server import dataset_creator_server
from App.Server import predictor_server

predictor_blueprint = Blueprint('prediction', __name__, url_prefix='/prediction')


@predictor_blueprint.route('/train-performance', methods=['POST'])
@validate_catering_in_payload_request
def get_train_model_performance():
    try:
        catering: List[Dict] = request.json.get(CATERING)
        time_elapsed, model_name, model, cross_val_r2_mean_train, cross_val_r2_std_train, r2_valid = \
            predictor_server.evaluate_train_model_performance(catering)
        response = {
            "time": f"{round(time_elapsed, 4)} sec",
            "catering": catering,
            "model_name": model_name,
            "cross_val_r2_mean_train": cross_val_r2_mean_train,
            "cross_val_r2_std_train": cross_val_r2_std_train,
            "r2_valid": r2_valid
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@predictor_blueprint.route('/build/prediction-model', methods=['POST'])
@validate_catering_in_payload_request
def build_regression_model():
    try:
        catering: List[Dict] = request.json.get(CATERING)
        time_elapsed = predictor_server.build_prediction_model(catering)
        response = {
            "time": f"{round(time_elapsed, 4)} sec",
            "catering": catering,
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@predictor_blueprint.route('/build/train-dataset', methods=['POST'])
@validate_catering_in_payload_request
def create_dataset():
    try:
        catering = request.json.get(CATERING)
        time_elapsed = dataset_creator_server.build_training_dataset(catering)
        response = {
            "saved": "ok",
            "time": f"{round(time_elapsed, 4)} sec",
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@predictor_blueprint.route('/transform/test-data', methods=['POST'])
def transform_test_data():
    try:
        breakfast_data = request.json.get(BREAKFAST)
        lunch_data = request.json.get(LUNCH)
        response_dict = dict()

        if breakfast_data is not None:
            response_dict[BREAKFAST] = dataset_creator_server.transform_test_dataset(BREAKFAST, breakfast_data)
        if lunch_data is not None:
            response_dict[LUNCH] = dataset_creator_server.transform_test_dataset(LUNCH, lunch_data)
        if breakfast_data is None and lunch_data is None:
            return make_response(jsonify({'error': f"Missing {BREAKFAST} or {LUNCH}  fields in the request"}), 400)

        return make_response(jsonify(response_dict), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)


@predictor_blueprint.route('/predict', methods=['POST'])
def predict():
    try:
        breakfast_data = request.json.get(BREAKFAST)
        lunch_data = request.json.get(LUNCH)
        response_dict = dict()

        if breakfast_data is not None:
            response_dict[BREAKFAST] = predictor_server.predict(BREAKFAST, breakfast_data)
        if lunch_data is not None:
            response_dict[LUNCH] = predictor_server.predict(LUNCH, lunch_data)
        if breakfast_data is None and lunch_data is None:
            return make_response(jsonify({'error': f"Missing {BREAKFAST} or {LUNCH}  fields in the request"}), 400)

        return make_response(jsonify(response_dict), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)