import pickle
import os
import time
import pandas
from typing import Dict, List, Set, Tuple
from App.Database import query_data
from App.Server.Preprocessing.BagOfWords import BagOfWords
from App.Util.constants import DIETS, BOW_MAX_FEATURES, MenuFields
from App.Util.constants import BOW_FILE_PATH

ID = '_id'


def build_menus_bow_model(catering: str) -> Tuple[float, List[str]]:
    start: float = time.time()
    bow_file_path = f"{BOW_FILE_PATH}{catering}_menu.pkl"
    menus: List[Dict] = query_data.get_list_menu_docs(catering)
    df = pandas.DataFrame(data=menus).set_index(ID).sort_index()

    bow = BagOfWords(DIETS, BOW_MAX_FEATURES)
    bow.build(df, MenuFields.IS_SERVICE_DAY)
    bow.save_results(bow_file_path)
    features = bow.get_features()

    end: float = time.time()
    time_elapsed = end - start
    return time_elapsed, features


def read_menu_bow_model(catering: str) -> BagOfWords:
    bow_file_path: str = f"{BOW_FILE_PATH}{catering}_menu.pkl"
    if not os.path.exists(bow_file_path) or not os.path.isfile(bow_file_path):
        raise Exception(f"BoW file for {catering} menus does not exist. In order to get the features you need to build "
                        f"the model first.")
    with open(bow_file_path, 'rb', pickle.HIGHEST_PROTOCOL) as f:
        bow: BagOfWords = pickle.load(f)
    return bow


def get_bow_features(catering: str) -> Tuple[List[str], Dict[str, Set[str]]]:
    bow = read_menu_bow_model(catering)
    features = bow.get_features()
    stemmed_words_features = bow.get_stemmed_words_features_dict()
    return features, stemmed_words_features
