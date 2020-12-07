import pandas
from pandas import DataFrame
from typing import List, Dict, Tuple
from termcolor import cprint, COLORS
from App.Server.Predictor import regression


def build_model(model_names: List[str], x_train: DataFrame, y_train: DataFrame,
                max_cardinality: int, estimators: List[int], svr_kernel: List[str], poly_degree: List[int],
                max_depth: List[int], random_state: int) -> \
        Dict[str, regression.AbstractRegression]:
    """
    Creates a dictionary based on a list of desired regression models

    Args:
        model_names (List[str]): List of regression models names.
        x_train (pandas.DataFrame): Independent variables from the training data.
        y_train (pandas.DataFrame): Dependent variable from the training data.
        max_cardinality (int): Maximum cardinality to apply OneHotEncoder
        estimators (List[int]): List of estimators for Random Forest Regression
        svr_kernel (List[str]): Kernel list names for Support Vector Regression
        poly_degree (List[int]): List of degrees for  Polynomial Regression
        max_depth (List[int]): Array of max_depth for Random Forest and Gradient Boosting
        random_state (int): Number used for initializing the internal random number generator

    Returns:
        Dict[str, AbstractRegression]: Dictionary containing the models specified in the models_names list
    """
    model_dict: Dict[str, regression.AbstractRegression] = dict()
    num_models = len(model_names)
    color_list = list(COLORS.keys())[1:]
    num_colors = len(color_list)
    circular_colors = [color_list[i % num_colors] for i in range(0, num_models)]

    for idx, model_name in enumerate(model_names):
        color = circular_colors[idx]
        if model_name == "MultipleLinearRegression":
            key_model = model_name
            model_dict[key_model] = regression.MultipleLinearRegression(max_cardinality=max_cardinality,
                                                                        print_color=color)
        elif model_name == "SupportVectorRegression":
            for kernel in svr_kernel:
                key_model = f'{model_name}_{kernel}Kernel'
                model_dict[key_model] = regression.SupportVectorRegression(max_cardinality=max_cardinality,
                                                                           kernel=kernel,
                                                                           print_color=color)
        elif model_name == "PolynomialRegression":
            for degree in poly_degree:
                key_model = f'{model_name}_{degree}Degree'
                model_dict[key_model] = regression.PolynomialRegression(max_cardinality=max_cardinality, degree=degree,
                                                                        print_color=color)
        elif model_name == "DecisionTreeRegression":
            key_model = model_name
            model_dict[key_model] = regression.DecisionTreeRegression(max_cardinality=max_cardinality,
                                                                      random_state=random_state,
                                                                      print_color=color)
        elif model_name == "RandomForestRegression":
            for depth in max_depth:
                for num_estimators in estimators:
                    key_model = f'{model_name}_{num_estimators}Estimators_{depth}MaxDepth'
                    model_dict[key_model] = regression.RandomForestRegression(max_cardinality=max_cardinality,
                                                                              random_state=random_state,
                                                                              num_estimators=num_estimators,
                                                                              max_depth=depth,
                                                                              print_color=color)
        elif model_name == 'GradientBoostingRegressor':
            for depth in max_depth:
                for num_estimators in estimators:
                    key_model = f'{model_name}_{num_estimators}Estimators_{depth}MaxDepth'
                    model_dict[key_model] = regression.GradientBoostedDecisionTrees(max_cardinality=max_cardinality,
                                                                                    random_state=random_state,
                                                                                    num_estimators=num_estimators,
                                                                                    max_depth=depth,
                                                                                    print_color=color)
    for _, model in model_dict.items():
        model.train_model(x_train=x_train, y_train=y_train)
    return model_dict


def evaluate_models(model_name: str, model: regression.AbstractRegression, x_train: DataFrame, y_train: DataFrame,
                    x_valid: DataFrame, y_valid: DataFrame, predict_samples: bool, num_folds: int, num_repeats: int,
                    scoring: str, random_state: int) -> Tuple[float, float, float]:
    """
    Creates a dictionary based on a list of desired regression models

    Args:
        model_name (AbstractRegression): Name of the trained regression model
        model (AbstractRegression): The trained regression model
        x_train (pandas.DataFrame): Independent variables from the training data.
        y_train (pandas.DataFrame): Dependent variable from the training data.
        x_valid (pandas.DataFrame): Independent variables from the validation data.
        y_valid (pandas.DataFrame): Dependent variable from the validation data.
        predict_samples: If true, prints the prediction for some validation inputs
        num_folds (int): Number of cross validation folds
        num_repeats (int): Number of repeats for cross validation
        scoring (str): Type of scoring evaluation
        random_state (int): Number used for initializing the internal random number generator

    Returns:
        None
    """
    color = model.print_color
    r2_valid = model.evaluate(x_valid=x_valid, y_valid=y_valid)
    cross_val_r2_mean_train, cross_val_r2_std_train = model.get_cross_validation_mean_score(x_train=x_train,
                                                                                            y_train=y_train,
                                                                                            num_folds=num_folds,
                                                                                            num_repeats=num_repeats,
                                                                                            scoring=scoring,
                                                                                            random_state=random_state)

    cprint(f'{model_name}', color)
    cprint(f'\tCrossVal R2 (Train):  mean: {cross_val_r2_mean_train:.3f} ,  std: {cross_val_r2_std_train:.3f}', color)
    cprint(f'\tR2 (Validation): {r2_valid:.3f}', color)

    # Predicting with some Validation inputs
    if predict_samples:
        idx_samples = x_valid.index[-5:]
        x_sample = x_valid.loc[idx_samples, :]
        y_sample = y_valid.loc[idx_samples]
        y_predict = list(map(lambda val: round(val, 2), model.predict(x_sample)))
        data = {'Prediction': y_predict}
        df_prediction = pandas.DataFrame(data, index=y_sample.index)
        cprint('Example set:', color)
        cols_names = x_sample.columns[-5:]
        sample_set = [x_sample[cols_names], y_sample, df_prediction]
        df = pandas.concat(sample_set, axis=1)
        cprint(df, color)
    return cross_val_r2_mean_train, cross_val_r2_std_train, r2_valid
