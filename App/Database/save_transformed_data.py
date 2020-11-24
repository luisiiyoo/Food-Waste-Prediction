from typing import Dict, List, Set, Union
from termcolor import colored
from App.Util.constants import COLOR_LUNCH, COLOR_BREAKFAST
from App.Models import Menu, BreakfastRegister, LunchRegister, RegistersCollection
from App.Util.helpers import to_dict
from App.Database import db
from config import MongoCollections
from App.Util.constants import BREAKFAST, LUNCH
from App.Util.constants import CATERINGS


def save_menus(dict_menus: Dict[str, List[Menu]]) -> None:
    print(colored('Saving Breakfast menus on the db...', COLOR_BREAKFAST), end=" ")
    breakfast_menus: List[Menu] = dict_menus.get(BREAKFAST)
    breakfast_dates: Set[str] = {menu.date for menu in breakfast_menus}
    save_menu_data(BREAKFAST, breakfast_menus, breakfast_dates)
    print(colored('done', COLOR_BREAKFAST))

    print(colored('Saving Lunch menus on the db...', COLOR_LUNCH), end=" ")
    lunch_menus: List[Menu] = dict_menus.get(LUNCH)
    lunch_dates: Set[str] = {menu.date for menu in lunch_menus}
    save_menu_data(LUNCH, lunch_menus, lunch_dates)
    print(colored('done', COLOR_LUNCH))


def save_menu_data(catering: str, menus: List[Menu], dates: List[str]) -> None:
    if catering == BREAKFAST:
        collection_name = MongoCollections.MENUS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.MENUS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to save data into the database.  Possible values: {CATERINGS}")

    for date in dates:
        db.delete_many('date', date, collection_name)
    db.add_many(to_dict(menus), collection_name)


def save_register(breakfast_registers: RegistersCollection, lunch_registers: RegistersCollection) -> None:
    print(colored('Saving Breakfast registers on the db...', COLOR_BREAKFAST), end=" ")
    save_register_data(BREAKFAST, breakfast_registers.registers, breakfast_registers.dates)
    print(colored('done', COLOR_BREAKFAST))

    print(colored('Saving Lunch registers on the db...', COLOR_LUNCH), end=" ")
    save_register_data(LUNCH, lunch_registers.registers, lunch_registers.dates)
    print(colored('done', COLOR_LUNCH))


def save_register_data(catering: str, registers: List[Union[BreakfastRegister, LunchRegister]],
                       dates: List[str]) -> None:
    if catering == BREAKFAST:
        collection_name = MongoCollections.REGISTERS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.REGISTERS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to save data into the database. Possible values: {CATERINGS}")

    for date in dates:
        db.delete_many('date', date, collection_name)
    db.add_many(to_dict(registers), collection_name)
