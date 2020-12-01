from typing import List, Dict, Union, Tuple
import pandas
from sklearn.model_selection import train_test_split
from App.Database.query_data import get_dataset_docs
from App.Server.Predictor import build_model, evaluate_models
from App.Server.Predictor.regression import AbstractRegression
from App.Util.constants import DatasetFields
from config import prediction_config

ID = '_id'


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


def generate_model(catering: str) -> Tuple[str, AbstractRegression, float, float, float]:
    independent_vars, dependent_var = get_dataset(catering)

    # Break off validation set from training data
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
    return model_name, model, *evaluation

    def predict():
        pass
