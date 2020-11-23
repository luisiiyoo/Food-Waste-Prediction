from typing import Dict, List, Union
from termcolor import colored
from App.Util.constants import COLOR_LUNCH, COLOR_BREAKFAST
from App.Models import Menu, BreakfastRegister, LunchRegister
from App.Util.helpers import to_dict
from App.Preproccessing.DataTransformers import MenuTransformer, RegisterTransformer
from App.Database import db
from config import MongoCollections
from App.Util.constants import BREAKFAST, LUNCH


def transform_menu_data(full_path_file: str) -> Dict[str, Dict]:
    try:
        menu_generator = MenuTransformer(full_path_file)
        dict_menus: Dict[str, List[Menu]] = menu_generator.build()
        return {catering: to_dict(menus) for catering, menus in dict_menus.items()}
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to menu data.")


def transform_register_data(full_path_file: str) -> Dict[str, Dict]:
    try:
        register_generator = RegisterTransformer(full_path_file)
        breakfast_registers, lunch_registers = register_generator.build()

        print(colored('Saving Breakfast registers on the db...', COLOR_BREAKFAST), end=" ")
        save_registers_data(BREAKFAST, breakfast_registers.registers, breakfast_registers.dates)
        print(colored('done', COLOR_BREAKFAST))

        print(colored('Saving Lunch registers on the db...', COLOR_LUNCH), end=" ")
        save_registers_data(LUNCH, lunch_registers.registers, lunch_registers.dates)
        print(colored('done', COLOR_LUNCH))

        return {
            BREAKFAST: to_dict(breakfast_registers),
            LUNCH: to_dict(lunch_registers)
        }
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to register data.")


def save_registers_data(catering: str, registers: List[Union[BreakfastRegister, LunchRegister]],
                        dates: List[str]) -> None:
    if catering == BREAKFAST:
        collection_name = MongoCollections.REGISTERS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.REGISTERS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to save data into the database.")

    for date in dates:
        db.delete_many('date', date, collection_name)
    db.add_many(to_dict(registers), collection_name)
