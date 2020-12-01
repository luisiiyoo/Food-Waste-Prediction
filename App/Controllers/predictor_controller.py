import traceback
from typing import Dict, List
from flask import Blueprint, jsonify, make_response, request
from App.Controllers.request_validators import validate_catering_in_payload_request
from App.Util.constants import CATERING
from App.Server.predictor_server import generate_model, evaluate_train_model_performance

predictor_blueprint = Blueprint('prediction', __name__, url_prefix='/prediction')


@predictor_blueprint.route('/train-performance', methods=['POST'])
@validate_catering_in_payload_request
def get_train_model_performance():
    try:
        catering: List[Dict] = request.json.get(CATERING)
        time_elapsed, model_name, model, cross_val_r2_mean_train, cross_val_r2_std_train, r2_valid = \
            evaluate_train_model_performance(catering)
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


@predictor_blueprint.route('/build', methods=['POST'])
@validate_catering_in_payload_request
def build_regression_model():
    try:
        catering: List[Dict] = request.json.get(CATERING)
        time_elapsed, model_name, model = generate_model(catering)
        response = {
            "time": f"{round(time_elapsed, 4)} sec",
            "catering": catering,
            "model_name": model_name
        }
        return make_response(jsonify(response), 200)
    except Exception as e:
        traceback.print_exc()
        return make_response(jsonify({'error': str(e)}), 400)
