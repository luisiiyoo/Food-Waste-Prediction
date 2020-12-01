from config import MongoCollections
from App.Util.constants import BREAKFAST, LUNCH
from App.Util.constants import CATERINGS


def get_menu_collection(catering: str) -> str:
    if catering == BREAKFAST:
        collection_name = MongoCollections.MENUS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.MENUS_LUNCH
    else:
        raise Exception(
            f"Invalid catering '{catering}' for getting the menus collection. Valid catering values: {CATERINGS}")
    return collection_name


def get_register_collection(catering: str) -> str:
    if catering == BREAKFAST:
        collection_name = MongoCollections.REGISTERS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.REGISTERS_LUNCH
    else:
        raise Exception(
            f"Invalid catering '{catering}' for getting the registers collection. Valid catering values: {CATERINGS}")
    return collection_name


def get_database_collection(catering: str) -> str:
    if catering == BREAKFAST:
        collection_name = MongoCollections.DATASET_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.DATASET_LUNCH
    else:
        raise Exception(
            f"Invalid catering '{catering}' for getting the database collection. Valid catering values: {CATERINGS}")
    return collection_name
