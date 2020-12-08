from typing import List, Union, Dict
from App.Models import Menu, BreakfastRegister, LunchRegister
from App.Util.helpers import to_dict
from App.Database import db, collection_manager
from App.Util.constants import MenuFields, RegisterFields


def delete_dataset_db(catering: str) -> None:
    collection_name: str = collection_manager.get_dataset_collection(catering)
    db.delete_all(collection_name)


def save_menus_db(catering: str, menus: List[Menu], dates: List[str]) -> None:
    collection_name: str = collection_manager.get_menu_collection(catering)

    # dropping the documents with same date in order to avoid issues
    for date in dates:
        db.delete_many(MenuFields.DATE, date, collection_name)
    db.add_many(to_dict(menus), collection_name)


def save_registers_db(catering: str, registers: List[Union[BreakfastRegister, LunchRegister]],
                      dates: List[str]) -> None:
    collection_name: str = collection_manager.get_register_collection(catering)

    # dropping the documents with same date in order to avoid issues
    for date in dates:
        db.delete_many(RegisterFields.DATE, date, collection_name)
    db.add_many(to_dict(registers), collection_name)


def save_dataset_db(catering: str, dataset: List[Dict[str, Union[str, int]]]) -> None:
    delete_dataset_db(catering)
    collection_name: str = collection_manager.get_dataset_collection(catering)
    db.add_many(to_dict(dataset), collection_name)


def get_list_menu_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_menu_collection(catering)
    return [document for document in db.find_all(collection_name)]


def get_list_register_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_register_collection(catering)
    return [document for document in db.find_all(collection_name)]


def get_dataset_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_dataset_collection(catering)
    return [document for document in db.find_all(collection_name)]
