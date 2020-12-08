from typing import List, Dict, Union
import time
import pandas
from App.Server.Preprocessor.DatasetCreator import DatasetCreator
from App.Server.preprocessor_server import read_menu_bow_model
from App.Server.predictor_server import remove_prediction_model
from App.Database.db_server import get_list_menu_docs, get_list_register_docs, save_dataset_db
from App.Util.constants import RegisterFields


def get_menus_dataframe_from_db(catering: str) -> pandas.DataFrame:
    """
    Gets a menus dataframe from all the menu documents given a catering collection

    Args:
        catering (string): A valid catering

    Returns:
        pandas.DataFrame: Menus dataframe from all the menu documents in the db

    Raises:
        Exception: If there is no documents on the catering collection
    """
    data: List[Dict] = get_list_menu_docs(catering)
    if len(data) == 0:
        raise Exception(f"Empty menus collection")
    df = pandas.DataFrame(data=data)
    return df


def get_registers_dataframe_from_db(catering: str) -> pandas.DataFrame:
    """
    Gets a registers dataframe from all the register documents given a catering collection

    Args:
        catering (string): A valid catering

    Returns:
        pandas.DataFrame: Registers dataframe from all the register documents in the db

    Raises:
        Exception: If there is no documents on the catering collection
    """
    data: List[Dict] = get_list_register_docs(catering)
    if len(data) == 0:
        raise Exception(f"Empty registers collection")
    df = pandas.DataFrame(data=data)
    return df


def get_registers_dataframe_from_raw_dict(raw_registers: List[Dict], ignore_attend: bool) -> pandas.DataFrame:
    """
    Gets a registers dataframe from a raw dictionary

    Args:
        raw_registers (List[Dict]): List of raw registers dictionary
        ignore_attend (bool): Flag to ignore the `attend` attribute

    Returns:
        pandas.DataFrame: Registers dataframe

    Raises:
        Exception: If the List of raw registers is empty
    """
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
    """
    Creates and saves the training dataset from all the preprocessed menus (BoW features) and grouped records

    Args:
        catering (string): A valid catering

    Returns:
        pandas.DataFrame: Registers dataframe

    Raises:
        Exception: If there is missing a column (attribute) in any menus or registers datasets
    """
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


def transform_test_dataset(catering: str, raw_registers: List[Dict], ignore_attend: bool = True) \
        -> List[Dict[str, Union[str, int]]]:
    """
    Transforms raw registers to valid preprocessed data (BoW) in order to use in the prediction process

    Args:
        catering (string): A valid catering
        raw_registers (List[Dict]): Raw registers to transform into valid test dataset
        ignore_attend (bool = True): Flag to ignore the `attend` attribute

    Returns:
        List[Dict[str, Union[str, int]]]: Test dataset to use in the prediction process

    Raises:
        Exception: If there is missing a attribute on the given data
    """
    try:
        df_registers = get_registers_dataframe_from_raw_dict(raw_registers, ignore_attend)
        df_menus = get_menus_dataframe_from_db(catering)
        bow_menus = read_menu_bow_model(catering)

        dataset_creator = DatasetCreator(df_registers, df_menus, bow_menus)
        dataset: List[Dict[str, Union[str, int]]] = dataset_creator.build(ignore_attend)
        return dataset
    except KeyError as e:
        raise Exception(f"Missing key {e} on one or many registers for {catering}.")
