from typing import List, Union, Dict
from App.Models import Menu, BreakfastRegister, LunchRegister
from App.Util.helpers import to_dict
from App.Database import db, collection_manager
from App.Util.constants import MenuFields, RegisterFields


def save_menus_to_db(catering: str, menus: List[Menu], dates: List[str]) -> None:
    collection_name: str = collection_manager.get_menu_collection(catering)

    # dropping the documents with same date in order to avoid issues
    for date in dates:
        db.delete_many(MenuFields.DATE, date, collection_name)
    db.add_many(to_dict(menus), collection_name)


def save_registers_to_db(catering: str, registers: List[Union[BreakfastRegister, LunchRegister]],
                         dates: List[str]) -> None:
    collection_name: str = collection_manager.get_register_collection(catering)

    # dropping the documents with same date in order to avoid issues
    for date in dates:
        db.delete_many(RegisterFields.DATE, date, collection_name)
    db.add_many(to_dict(registers), collection_name)


def save_dataset_to_db(catering: str, dataset: List[Dict[str, Union[str, int]]]) -> None:
    collection_name: str = collection_manager.get_database_collection(catering)

    # dropping all documents in order to avoid issues at the training
    db.delete_all(collection_name)
    db.add_many(to_dict(dataset), collection_name)
