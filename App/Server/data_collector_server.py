from typing import Dict, List, Set, Union
from App.Models import Menu, AbstractRegister, BreakfastRegister, LunchRegister
from App.Server.DataCollector import MenuTransformer, RegisterTransformer
from App.Util.constants import MenuFields, RegisterFields
from App.Util.constants import BREAKFAST
from App.Database.db_server import save_menus_db, save_registers_db


def transform_menu_data(full_path_file: str) -> Dict[str, List[Menu]]:
    """
    Transform a raw file to a valid dictionary of menus data grouped by catering

    Args:
        full_path_file (string): Raw menu file path

    Returns:
        Dict[str, List[Menu]]: Dictionary of menus data grouped by catering

    Raises:
        Exception: If the file has not a valid structure
    """
    try:
        menu_transformer = MenuTransformer(full_path_file)
        dict_menus: Dict[str, List[Menu]] = menu_transformer.build()
        return dict_menus
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to menu sample_data.")


def transform_register_data(full_path_file: str) -> Dict[str, List[AbstractRegister]]:
    """
    Transform a raw file to a valid dictionary of registers data grouped by catering

    Args:
        full_path_file (string): Raw menu file path

    Returns:
        Dict[str, List[Menu]]: Dictionary of registers data grouped by catering

    Raises:
        Exception: If the file has not a valid structure
    """
    try:
        register_transformer = RegisterTransformer(full_path_file)
        dict_registers: Dict[str, List[AbstractRegister]] = register_transformer.build()
        return dict_registers
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to register sample_data.")


def insert_menus(catering: str, list_dict_menus: List[Dict]) -> None:
    """
    Insert a list of menus to the given catering collection

    Args:
        catering (string): A valid catering
        list_dict_menus (List[Dict]): List of menu dictionaries to insert into the db

    Returns:
        None

    Raises:
        Exception: If there is a missing menu attribute
    """
    try:
        menus: List[Menu] = []
        for dict_menu in list_dict_menus:
            date = dict_menu[MenuFields.DATE]
            day = dict_menu[MenuFields.DAY]
            is_service_day = dict_menu[MenuFields.IS_SERVICE_DAY]
            regular = dict_menu[MenuFields.REGULAR]
            light = dict_menu[MenuFields.LIGHT]
            vegan = dict_menu[MenuFields.VEGAN]
            vegetarian = dict_menu[MenuFields.VEGETARIAN]
            menu = Menu(date=date, day=day, is_service_day=is_service_day, regular=regular, light=light, vegan=vegan,
                        vegetarian=vegetarian)
            menus.append(menu)
        unique_dates: Set[str] = {menu.date for menu in menus}
        save_menus_db(catering, menus, unique_dates)
    except KeyError as e:
        raise Exception(f"Missing key {e} on one or many menus.")


def insert_registers(catering: str, list_dict_registers: List[Dict]) -> None:
    """
    Insert a list of registers to the given catering collection

    Args:
        catering (string): A valid catering
        list_dict_registers (List[Dict]): List of register dictionaries to insert into the db

    Returns:
        None

    Raises:
        Exception: If there is a missing register attribute
    """
    try:
        registers: List[Union[BreakfastRegister, LunchRegister]] = []
        for dict_registers in list_dict_registers:
            date = dict_registers[RegisterFields.DATE]
            person = dict_registers[RegisterFields.PERSON]
            diet = dict_registers[RegisterFields.DIET]
            request = dict_registers[RegisterFields.REQUEST]
            attend = dict_registers[RegisterFields.ATTEND]
            if catering == BREAKFAST:
                register = BreakfastRegister(date=date, person=person, request=request, attend=attend, diet=diet)
            else:
                register = LunchRegister(date=date, person=person, request=request, attend=attend, diet=diet,
                                         extra=RegisterFields.EXTRA)
            registers.append(register)
        unique_dates: Set[str] = {register.date for register in registers}
        save_registers_db(catering, registers, unique_dates)
    except KeyError as e:
        raise Exception(f"Missing key {e} on one or many registers for {catering}.")
