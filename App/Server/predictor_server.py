import time
from typing import List, Dict, Union, Tuple
import pandas
from sklearn.model_selection import train_test_split
from App.Database.query_data import get_dataset_docs
from App.Server.Predictor import build_model, evaluate_models
from App.Server.Predictor.regression import AbstractRegression
from App.Util.constants import DatasetFields, REGRESSION_MODEL_FILE_PATH
from App.Util.helpers import save_object_to_pkl_file, read_object_from_pkl_file
from config import prediction_config

ID = '_id'


def get_file_name_model(catering: str) -> str:
    return f"{REGRESSION_MODEL_FILE_PATH}{catering}.pkl"


def get_dataset(catering: str) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    dataset = get_dataset_docs(catering)
    df = pandas.DataFrame(data=dataset).set_index(ID)
    df[DatasetFields.DATE] = pandas.to_datetime(df[DatasetFields.DATE])
    df = df.sort_values(by=[DatasetFields.DATE, DatasetFields.DIET], ascending=True)
    # Remove rows with missing target, separate target from predictors
    df.dropna(axis=0, subset=[prediction_config.TARGET_COLUMN], inplace=True)

    y = df[prediction_config.TARGET_COLUMN]
    X = df.drop([prediction_config.TARGET_COLUMN, *prediction_config.EXCLUDE_COLS], axis=1)
    return X, y


def evaluate_train_model_performance(catering: str) -> Tuple[float, str, AbstractRegression, float, float, float]:
    start: float = time.time()
    independent_vars, dependent_var = get_dataset(catering)
    x_train, x_valid, y_train, y_valid = train_test_split(independent_vars, dependent_var,
                                                          test_size=prediction_config.TEST_SIZE_PROPORTION,
                                                          random_state=prediction_config.RANDOM_STATE)
    models_dict = build_model(x_train=x_train, y_train=y_train,
                              model_names=prediction_config.MODELS,
                              max_cardinality=prediction_config.MAX_CARDINALITY,
                              estimators=prediction_config.ESTIMATORS,
                              svr_kernel=prediction_config.SVR_KERNEL,
                              poly_degree=prediction_config.POLY_DEGREE,
                              max_depth=prediction_config.MAX_DEPTH,
                              random_state=prediction_config.RANDOM_STATE)

    model_name = list(models_dict.keys())[0]
    model = models_dict[model_name]
    evaluation = evaluate_models(model_name=model_name, model=model, x_train=x_train, y_train=y_train, x_valid=x_valid,
                                 y_valid=y_valid, predict_samples=True)

    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed, model_name, model, *evaluation


def generate_model(catering: str) -> Tuple[float]:
    start: float = time.time()
    regression_model_file_path = get_file_name_model(catering)
    independent_vars, dependent_var = get_dataset(catering)
    models_dict = build_model(x_train=independent_vars, y_train=dependent_var,
                              model_names=prediction_config.MODELS,
                              max_cardinality=prediction_config.MAX_CARDINALITY,
                              estimators=prediction_config.ESTIMATORS,
                              svr_kernel=prediction_config.SVR_KERNEL,
                              poly_degree=prediction_config.POLY_DEGREE,
                              max_depth=prediction_config.MAX_DEPTH,
                              random_state=prediction_config.RANDOM_STATE)

    model_name: str = list(models_dict.keys())[0]
    model: AbstractRegression = models_dict[model_name]
    save_object_to_pkl_file(model, regression_model_file_path)

    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed


def read_regression_model(catering: str) -> AbstractRegression:
    file_path = get_file_name_model(catering)
    try:
        regression_model: AbstractRegression = read_object_from_pkl_file(file_path)
    except Exception as e:
        if str(e).find('file does not exist') != -1:
            raise Exception(
                f"The regression model file for {catering} does not exist. In order to predict you need to build the "
                f"model first.")
        raise e
    return regression_model


def predict():
    pass
