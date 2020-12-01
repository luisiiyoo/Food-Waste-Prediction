from typing import List, Tuple
from pandas import DataFrame
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


class Preprocessing:
    """""
    Preprocessing class with static methods to deal with missing values and encode the categorical variables

    Args:
       None

    Attributes:
        None
    """
    @staticmethod
    def get_preprocessor_transformer(data: DataFrame, max_cardinality: int) -> \
            Tuple[ColumnTransformer, List[str], List[str], List[str]]:
        """
        Returns a preprocessor pipeline to deal with missing values and encode the categorical variables

        Args:
            data (pandas.DataFrame): Dependent variables
            max_cardinality (int): Maximum cardinality to apply OneHotEncoder

        Returns:
            ColumnTransformer: Preprocessor transformer
            List[str]: Numerical column names
            List[str]: Categorical column names used to one hot encode
            List[str]: Categorical column names used to label encode
        """
        cat_cols_one_hot_encoder, cat_cols_label_encoder = Preprocessing.get_categorical_cols(
            data, max_cardinality)
        numerical_cols = Preprocessing.get_numerical_cols(data)

        num_transformer = SimpleImputer(strategy='mean')
        cat_one_hot_transformer = Pipeline(steps=[
            ('simple_imputer', SimpleImputer(strategy='most_frequent')),
            ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
        ])

        preprocessor_transformer = ColumnTransformer(
            transformers=[
                ('num_transformer', num_transformer, numerical_cols),
                ('cat_one_hot_transformer', cat_one_hot_transformer, cat_cols_one_hot_encoder)
            ])
        return preprocessor_transformer, numerical_cols, cat_cols_one_hot_encoder, cat_cols_label_encoder

    @staticmethod
    def get_categorical_cols(data: DataFrame, max_cardinality: int) -> Tuple[List[str], List[str]]:
        """
        Returns a list that contains the column names for categorical variables that satisfies the maximum number of
        unique values (max_cardinality) and another list that doesn't satisfy the maximum number of unique values

        Args:
            data (pandas.DataFrame): Dependent variables
            max_cardinality (int): Maximum number of unique values

        Returns:
            List[str]: Categorical column names that has equal or lower cardinality than `max_cardinality`
            List[str]: Categorical column names that has greater cardinality than `max_cardinality`
        """
        type_required = "object"
        cols_names = data.columns
        categorical_cols_satisfies = []
        categorical_cols_no_satisfies = []
        for cname in cols_names:
            if data[cname].dtype == type_required:
                if data[cname].nunique() <= max_cardinality:
                    categorical_cols_satisfies.append(cname)
                else:
                    categorical_cols_no_satisfies.append(cname)
        return categorical_cols_satisfies, categorical_cols_no_satisfies

    @staticmethod
    def get_numerical_cols(data: DataFrame) -> List[str]:
        """
        Returns a list that contains the column names for numerical variables

        Args:
            data (pandas.DataFrame): Dependent variables

        Returns:
            List[str]: Numerical column names
        """
        # Select numerical columns
        type_required = ['int64', 'float64']
        cols_names = data.columns
        numerical_cols = [cname for cname in cols_names if data[cname].dtype in type_required]
        return numerical_cols
