import os
import time
import pandas
from typing import Dict, List, Set, Tuple
from App.Database.db_server import get_list_menu_docs, delete_dataset_db
from App.Server.Preprocessor.BagOfWords import BagOfWords
from App.Server.predictor_server import remove_prediction_model
from App.Util.constants import DIETS, BOW_MAX_FEATURES, BOW_FILE_PATH, MenuFields
from App.Util.helpers import save_object_to_pkl_file, read_object_from_pkl_file

ID = '_id'


def remove_menu_bow_model(catering: str) -> None:
    bow_file_path = get_file_name_model(catering)
    if os.path.exists(bow_file_path):
        os.remove(bow_file_path)


def get_file_name_model(catering: str) -> str:
    return f"{BOW_FILE_PATH}{catering}_menu.pkl"


def build_menus_bow_model(catering: str) -> Tuple[float, List[str]]:
    start: float = time.time()
    # Drop older bow file, dataset and prediction model because the features can change
    remove_menu_bow_model(catering)
    delete_dataset_db(catering)
    remove_prediction_model(catering)

    menus: List[Dict] = get_list_menu_docs(catering)
    df = pandas.DataFrame(data=menus).set_index(ID).sort_index()

    bow = BagOfWords(DIETS, BOW_MAX_FEATURES)
    bow.build(df, MenuFields.IS_SERVICE_DAY)
    save_object_to_pkl_file(bow, get_file_name_model(catering))
    features = bow.get_features()

    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed, features


def read_menu_bow_model(catering: str) -> BagOfWords:
    bow_file_path = get_file_name_model(catering)
    try:
        bow: BagOfWords = read_object_from_pkl_file(bow_file_path)
    except Exception as e:
        if str(e).find('file does not exist') != -1:
            raise Exception(
                f"BoW file for {catering} menus does not exist. In order to get the features you need to build "
                f"the model first.")
        raise e
    return bow


def get_bow_features(catering: str) -> Tuple[List[str], Dict[str, Set[str]]]:
    bow = read_menu_bow_model(catering)
    features = bow.get_features()
    stemmed_words_features = bow.get_stemmed_words_features_dict()
    return features, stemmed_words_features
