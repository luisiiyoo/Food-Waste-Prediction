from typing import List, Dict, Union
import time
import pandas
from App.Server.Preprocessing.DatasetCreator import DatasetCreator
from App.Server.preprocessing_server import read_menu_bow_model
from App.Database.query_data import get_list_menu_docs, get_list_register_docs
from App.Database.save_data import save_dataset_to_db


def merge_datasets(catering: str) -> float:
    start: float = time.time()
    registers: List[Dict] = get_list_register_docs(catering)
    df_registers = pandas.DataFrame(data=registers)

    menus: List[Dict] = get_list_menu_docs(catering)
    df_menus = pandas.DataFrame(data=menus)

    bow_menus = read_menu_bow_model(catering)

    dataset_creator = DatasetCreator(df_registers, df_menus, bow_menus)
    dataset: List[Dict[str, Union[str, int]]] = dataset_creator.build()

    save_dataset_to_db(catering, dataset)

    end: float = time.time()
    time_elapsed: float = end - start
    return time_elapsed
