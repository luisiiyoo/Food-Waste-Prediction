from typing import List, Union
from App.Models import Menu, BreakfastRegister, LunchRegister
from App.Util.helpers import to_dict
from App.Database import db
from config import MongoCollections
from App.Util.constants import BREAKFAST, LUNCH
from App.Util.constants import CATERINGS


def insert_menus_to_db(catering: str, menus: List[Menu], dates: List[str]) -> None:
    if catering == BREAKFAST:
        collection_name = MongoCollections.MENUS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.MENUS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to save data into the database.  Possible values: {CATERINGS}")

    for date in dates:
        db.delete_many('date', date, collection_name)
    db.add_many(to_dict(menus), collection_name)


def insert_registers_to_db(catering: str, registers: List[Union[BreakfastRegister, LunchRegister]], dates: List[str]) -> None:
    if catering == BREAKFAST:
        collection_name = MongoCollections.REGISTERS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.REGISTERS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to save data into the database. Possible values: {CATERINGS}")

    for date in dates:
        db.delete_many('date', date, collection_name)
    db.add_many(to_dict(registers), collection_name)
