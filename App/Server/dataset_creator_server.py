from typing import List, Dict, Union
import time
import pandas
from App.Server.Preprocessor.DatasetCreator import DatasetCreator
from App.Server.preprocessor_server import read_menu_bow_model
from App.Server.predictor_server import remove_prediction_model
from App.Database.db_server import get_list_menu_docs, get_list_register_docs, save_dataset_db
from App.Util.constants import RegisterFields


def get_menus_dataframe_from_db(catering: str) -> pandas.DataFrame:
    data: List[Dict] = get_list_menu_docs(catering)
    if len(data) == 0:
        raise Exception(f"Empty menus collection")
    df = pandas.DataFrame(data=data)
    return df


def get_registers_dataframe_from_db(catering: str) -> pandas.DataFrame:
    data: List[Dict] = get_list_register_docs(catering)
    if len(data) == 0:
        raise Exception(f"Empty registers collection")
    df = pandas.DataFrame(data=data)
    return df


def get_registers_dataframe_from_raw_dict(raw_registers: List[Dict], ignore_attend: bool) -> pandas.DataFrame:
    if len(raw_registers) == 0:
        raise Exception(f"Empty registers list provided")
    data: List[Dict] = list()
    for register_dict in raw_registers:
        r_dict = dict()
        r_dict[RegisterFields.DATE] = register_dict[RegisterFields.DATE]
        r_dict[RegisterFields.PERSON] = register_dict[RegisterFields.PERSON]
        r_dict[RegisterFields.DIET] = register_dict[RegisterFields.DIET]
        r_dict[RegisterFields.REQUEST] = register_dict[RegisterFields.REQUEST]
        if not ignore_attend:
            r_dict[RegisterFields.ATTEND] = register_dict[RegisterFields.ATTEND]
        data.append(r_dict)
    df = pandas.DataFrame(data=data)
    return df


def build_training_dataset(catering: str) -> float:
    try:
        start: float = time.time()
        # Remove old prediction model
        remove_prediction_model(catering)

        df_registers = get_registers_dataframe_from_db(catering)
        df_menus = get_menus_dataframe_from_db(catering)
        bow_menus = read_menu_bow_model(catering)

        dataset_creator = DatasetCreator(df_registers, df_menus, bow_menus)
        dataset: List[Dict[str, Union[str, int]]] = dataset_creator.build()

        save_dataset_db(catering, dataset)

        end: float = time.time()
        time_elapsed: float = end - start
        return time_elapsed
    except KeyError as e:
        raise Exception(f"Missing column {e} on the registers or menus collection.")


def transform_test_dataset(catering: str, raw_registers: List[Dict], ignore_attend: bool = True):
    try:
        df_registers = get_registers_dataframe_from_raw_dict(raw_registers, ignore_attend)
        df_menus = get_menus_dataframe_from_db(catering)
        bow_menus = read_menu_bow_model(catering)

        dataset_creator = DatasetCreator(df_registers, df_menus, bow_menus)
        dataset: List[Dict[str, Union[str, int]]] = dataset_creator.build(ignore_attend)
        return dataset
    except KeyError as e:
        raise Exception(f"Missing key {e} on one or many registers for {catering}.")
