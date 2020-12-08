import os
import time
from typing import List, Dict, Tuple, Callable
import pandas
from sklearn.model_selection import train_test_split
from App.Database.db_server import get_dataset_docs
from App.Server.Predictor import build_regression_model, evaluate_models
from App.Server.Predictor.regression import AbstractRegression
from App.Util.constants import DatasetFields, PREDICTION_MODEL_FILE_PATH
from App.Util.helpers import save_object_to_pkl_file, read_object_from_pkl_file
from config import prediction_config

ID = '_id'
PREDICTION = "prediction"


def get_file_name_model(catering: str) -> str:
    """
    Gets the proper full path file name of the prediction model

    Args:
        catering (string): A valid catering

    Returns:
        str: Full path file name of the prediction model
    """
    return f"{PREDICTION_MODEL_FILE_PATH}{catering}.pkl"


def get_dataset(catering: str) -> List[Dict]:
    """
    Gets the dataset related to a given catering

    Args:
        catering (string): A valid catering

    Returns:
        List[Dict]: Dataset of the given catering

    Raises:
        Exception: If the training dataset is empty
    """
    dataset = get_dataset_docs(catering)
    if len(dataset) == 0:
        raise Exception("Empty training dataset, you need to build first the training dataset before use it.")
    return dataset


def get_vars_from_dataset(catering: str) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    """
    Gets all the attributes (columns) in the training dataset

    Args:
        catering (string): A valid catering

    Returns:
        pandas.DataFrame: Records of the independent variable from the dataset
        pandas.DataFrame: Records of the dependent variable from the dataset
    """
    dataset = get_dataset(catering)
    df = pandas.DataFrame(data=dataset).set_index(ID)
    df[DatasetFields.DATE] = pandas.to_datetime(df[DatasetFields.DATE])
    df = df.sort_values(by=[DatasetFields.DATE, DatasetFields.DIET], ascending=True)
    # Remove rows with missing target, separate target from predictors
    df.dropna(axis=0, subset=[prediction_config.TARGET_COLUMN], inplace=True)

    y = df[prediction_config.TARGET_COLUMN]
    X = df.drop([prediction_config.TARGET_COLUMN, *prediction_config.EXCLUDE_COLS], axis=1)
    return X, y


def evaluate_train_model_performance(catering: str) -> Tuple[float, str, AbstractRegression, float, float, float]:
    """
    Evaluates the training process dividing all the data into two dataset (training and validation)

    Args:
        catering (string): A valid catering

    Returns:
        float: Time elapsed
        str: Model name
        AbstractRegression: Model created from the divided training dataset
        float: Mean of the cross-validation R2 score from the training data
        float: Standard deviation of the cross-validation R2 score from the training data
        float: R2 score from the validation data
    """
    start: float = time.time()
    independent_vars, dependent_var = get_vars_from_dataset(catering)
    x_train, x_valid, y_train, y_valid = train_test_split(independent_vars, dependent_var,
                                                          test_size=prediction_config.TEST_SIZE_PROPORTION,
                                                          random_state=prediction_config.RANDOM_STATE)
    models_dict = build_regression_model(x_train=x_train, y_train=y_train,
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
                                 y_valid=y_valid, predict_samples=prediction_config.PREDICT_SAMPLES,
                                 num_repeats=prediction_config.NUM_FOLDS, num_folds=prediction_config.NUM_FOLDS,
                                 scoring=prediction_config.SCORING, random_state=prediction_config.RANDOM_STATE)
    cross_val_r2_mean_train, cross_val_r2_std_train, r2_valid = evaluation
    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed, model_name, model, cross_val_r2_mean_train, cross_val_r2_std_train, r2_valid


def remove_prediction_model(catering: str) -> None:
    """
    Removes the prediction model file in order to avoid unwanted behaviors in the training/prediction process

    Args:
        catering (string): A valid catering

    Returns:
        None
    """
    regression_model_file_path = get_file_name_model(catering)
    if os.path.exists(regression_model_file_path):
        os.remove(regression_model_file_path)


def build_prediction_model(catering: str) -> float:
    """
    Trains and builds a prediction model given a catering

    Args:
        catering (string): A valid catering

    Returns:
        float: time elapsed
    """
    start: float = time.time()
    remove_prediction_model(catering)
    independent_vars, dependent_var = get_vars_from_dataset(catering)
    models_dict = build_regression_model(x_train=independent_vars, y_train=dependent_var,
                                         model_names=prediction_config.MODELS,
                                         max_cardinality=prediction_config.MAX_CARDINALITY,
                                         estimators=prediction_config.ESTIMATORS,
                                         svr_kernel=prediction_config.SVR_KERNEL,
                                         poly_degree=prediction_config.POLY_DEGREE,
                                         max_depth=prediction_config.MAX_DEPTH,
                                         random_state=prediction_config.RANDOM_STATE)

    model_name: str = list(models_dict.keys())[0]
    model: AbstractRegression = models_dict[model_name]
    save_object_to_pkl_file(model, get_file_name_model(catering))

    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed


def read_prediction_model(catering: str) -> AbstractRegression:
    """
    Reads a pre-built prediction model given a catering

    Args:
        catering (string): A valid catering

    Returns:
        AbstractRegression: Pre-built prediction model

    Raises:
        Exception: if the pre-built prediction model was not found
    """
    file_path = get_file_name_model(catering)
    try:
        regression_model: AbstractRegression = read_object_from_pkl_file(file_path)
    except Exception as e:
        if str(e).find('file does not exist') != -1:
            raise Exception(
                f"The prediction model file for {catering} does not exist. In order to predict you need to build the "
                f"model first.")
        raise e
    return regression_model


def validate_raw_test_data(func: Callable) -> Callable:
    """
    Decorator that validates the attributes of a given raw test data

    Args:
        func (Callable): Function to call after the validation

    Returns:
        Callable: Wrapper function

    Raises:
        Exception: if there is missing or extra fields on the raw data
    """

    def decorator(catering: str, raw_test_data: List[Dict]):
        # Obtaining the fields that must have the test data
        required_fields = set(get_dataset(catering)[0].keys())
        required_fields.discard(DatasetFields.ATTEND)
        for data in raw_test_data:
            data_fields = set(data.keys())
            if required_fields != data_fields:
                missing = required_fields - data_fields
                no_required = data_fields - required_fields
                missing_str = f"One or more records not contain {missing} field(s). " if missing else ''
                no_required_str = f"Fields not required: {no_required}. " if no_required else ''
                raise Exception(f"{missing_str}{no_required_str}")
        return func(catering, raw_test_data)

    decorator.__name__ = func.__name__
    return decorator


@validate_raw_test_data
def predict(catering: str, raw_test_data: List[Dict]) -> List[Dict]:
    """
    Predicts the attendance from a list of raw preprocessed test data

    Args:
        catering (string): A valid catering
        raw_test_data (List[Dict]): List of raw preprocessed test data

    Returns:
        List[Dict]: List of predictions
    """
    model: AbstractRegression = read_prediction_model(catering)
    test_data = pandas.DataFrame(data=raw_test_data).set_index(ID)

    predictions = list(map(lambda val: round(val, 2), model.predict(test_data)))

    predictions_dicts: List[Dict] = list()
    for pd_row, prediction in zip(test_data.iterrows(), predictions):
        idx, row = pd_row
        predictions_dicts.append({
            ID: idx,
            DatasetFields.DATE: row[DatasetFields.DATE],
            DatasetFields.DIET: row[DatasetFields.DIET],
            DatasetFields.REQUEST: row[DatasetFields.REQUEST],
            PREDICTION: prediction
        })
    return predictions_dicts
