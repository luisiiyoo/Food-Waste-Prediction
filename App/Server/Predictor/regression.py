import functools
from typing import List, Tuple, Any
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from App.Server.Predictor.preprocessing import Preprocessing


class AbstractRegression:
    """
    Regression parent class witch is the responsible of all the preprocess, fit, transform and predict processes

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       regression_model (Any): Regression model
       extra_pipeline_process (Tuple[str, Any]): Additional pipeline processes before build the model
       print_color (str): Color used to print in console

    Attributes:
        print_color (str): Color used to print in console
        __max_cardinality (int): Maximum cardinality to apply OneHotEncoder
        __regression_model (Any): Regression model
        __extra_pipeline_process (Tuple[str, Any]): Additional pipeline processes before build the model
        __interested_cols (List[str]): Columns names to use
        __pipeline (Pipeline): Child model regression pipeline
    """

    def __init__(self, max_cardinality: int, regression_model: Any, extra_pipeline_process: Tuple[str, Any] = None,
                 print_color: str = 'white'):
        self.print_color = print_color
        self.__max_cardinality = max_cardinality
        self.__regression_model = regression_model
        self.__extra_pipeline_process = extra_pipeline_process
        self.__interested_cols: List[str] = []
        self.__pipeline = None

    def train_model(self, x_train: DataFrame, y_train: DataFrame):
        """
        Builds and evaluates the model

        Args:
            x_train (pandas.DataFrame): Independent variables to train the model
            y_train (pandas.DataFrame): Dependent variable (target) to train the model

        Returns:
            None
        """
        preprocessor, num_cols, cat_cols_one_hot_encoder, cat_cols_label_encoder = Preprocessing. \
            get_preprocessor_transformer(x_train, self.__max_cardinality)

        self.__interested_cols = num_cols + cat_cols_one_hot_encoder + cat_cols_label_encoder
        pipeline_steps = [('preprocessor', preprocessor),
                          ('model', self.__regression_model)]
        if self.__extra_pipeline_process:
            pipeline_steps.insert(1, self.__extra_pipeline_process)

        self.__pipeline = Pipeline(steps=pipeline_steps)
        x = x_train[self.__interested_cols]
        self.__pipeline.fit(x, y_train)

    def evaluate(self, x_valid: DataFrame, y_valid: DataFrame) -> float:
        """
        Evaluates the trained model using validation dataset

        Args:
            x_valid (pandas.DataFrame): Independent validation variables to predict
            y_valid (pandas.DataFrame): Dependent validation variable to predict (expected result to predict)

        Returns:
            float: R2 score of the validation data
        """
        x = x_valid[self.__interested_cols]
        if self.__pipeline is None:
            raise Exception("The model is not yet trained, you need to train first in order to predict.")
        y_predict = self.__pipeline.predict(x)
        score_valid = r2_score(y_valid, y_predict)
        return score_valid

    def predict(self, x_test: DataFrame) -> List[float]:
        """
        Gets the predictions for testing data

        Args:
            x_test (pandas.DataFrame): Testing independent variables

        Returns:
            List[float]: Testing predictions
        """
        x = x_test[self.__interested_cols]
        if self.__pipeline is None:
            raise Exception("The model is not yet trained, you need to train first in order to predict.")
        y_test = self.__pipeline.predict(x)
        return y_test

    def get_cross_validation_mean_score(self, x_train: DataFrame, y_train: DataFrame, num_folds: int, scoring: str) -> \
            Tuple[float, float]:
        """
        Gets the mean and std score for the training performance on cross validation

        Args:
            x_train (pandas.DataFrame): Independent variables to train the model
            y_train (pandas.DataFrame): Dependent variable (target) to train the model
            num_folds (int): Number of folds to use on cross validation
            scoring (str): Metric name to calculate the score

        Returns:
            float: Mean score obtained on the cross validation
            float: Standard deviation score obtained on the cross validation
        """
        if self.__pipeline is None:
            raise Exception("The model is not yet trained, you need to train first in order to predict.")
        scores = cross_val_score(self.__pipeline, x_train, y_train, cv=num_folds, scoring=scoring)
        return scores.mean(), scores.std()


class MultipleLinearRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `LinearRegression` class

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
    """

    def __init__(self, max_cardinality: int, print_color: str):
        model = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=None)
        super().__init__(max_cardinality=max_cardinality, regression_model=model, print_color=print_color)


class PolynomialRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `PolynomialRegression`

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       degree (int): Polynomial degree to transform the data
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        degree (int): Polynomial degree to transform the data
    """

    def __init__(self, max_cardinality: int, degree: int, print_color: str):
        self.degree = degree
        poly_transformer_step = ('poly_transformer', PolynomialFeatures(degree=self.degree))
        model = LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=None)
        super().__init__(max_cardinality=max_cardinality, regression_model=model,
                         extra_pipeline_process=poly_transformer_step, print_color=print_color)


class SupportVectorRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `SVR` class

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       kernel (str): Support vector regression vector
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        kernel (str): Support vector regression vector
    """

    def __init__(self, max_cardinality: int, kernel: str,
                 print_color: str):
        self.kernel = kernel
        scale_transformer_step = ('scale_transformer', StandardScaler())
        model = SVR(kernel=self.kernel, degree=3, epsilon=0.1, gamma='scale')
        super().__init__(max_cardinality=max_cardinality, regression_model=model,
                         extra_pipeline_process=scale_transformer_step,
                         print_color=print_color)


class DecisionTreeRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `DecisionTreeRegressor` class

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       random_state (int): Number used for initializing the internal random number generator
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _random_state (int): Number used for initializing the internal random number generator
    """

    def __init__(self, max_cardinality: int, random_state: int, print_color: str):
        self._random_state = random_state
        model = DecisionTreeRegressor(random_state=self._random_state, criterion='mse', splitter='best', max_depth=None,
                                      min_samples_split=2, min_samples_leaf=1)
        super().__init__(max_cardinality=max_cardinality, regression_model=model, print_color=print_color)


class RandomForestRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `RandomForestRegressor` class

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       random_state (int): Number used for initializing the internal random number generator
       num_estimators (int): Number of estimators for Random Forest Regression
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _random_state (int): Number used for initializing the internal random number generator
        num_estimators (int): Number of estimators for Random Forest Regression
        max_depth (int): Maximum deep to build the tree
    """

    def __init__(self, max_cardinality: int, random_state: int, num_estimators: int,
                 max_depth: int, print_color: str):
        self._random_state = random_state
        self.num_estimators = num_estimators
        self.max_depth = max_depth
        model = RandomForestRegressor(n_estimators=self.num_estimators, random_state=self._random_state,
                                      criterion='mse', max_depth=self.max_depth)
        super().__init__(max_cardinality=max_cardinality, regression_model=model, print_color=print_color)


class GradientBoostedDecisionTrees(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `RandomForestRegressor` class

    Args:
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       random_state (int): Number used for initializing the internal random number generator
       num_estimators (int): Number of estimators for Random Forest Regression
       max_depth (int): Maximum depth of the individual regression estimators
       print_color (str): Color used to print in console

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _random_state (int): Number used for initializing the internal random number generator
        num_estimators (int): Number of estimators for Random Forest Regression
        max_depth (int): Maximum depth of the individual regression estimators
    """

    def __init__(self, max_cardinality: int, random_state: int, num_estimators: int,
                 max_depth: int, print_color: str):
        self._random_state = random_state
        self.num_estimators = num_estimators
        self.max_depth = max_depth
        model = GradientBoostingRegressor(n_estimators=self.num_estimators, max_depth=self.max_depth,
                                          random_state=self._random_state, learning_rate=0.1, loss='ls')
        super().__init__(max_cardinality=max_cardinality, regression_model=model, print_color=print_color)
