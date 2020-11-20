from typing import Dict, List
from App.Models import Menu, AbstractRegister
from App.Util.helpers import to_dict
from App.DataTransformers import MenuTransformer, RegisterTransformer


def transform_menu_data(full_path_file: str) -> Dict[str, Dict]:
    menu_generator = MenuTransformer(full_path_file)
    dict_menus: Dict[str, List[Menu]] = menu_generator.build()
    return {catering: to_dict(menus) for catering, menus in dict_menus.items()}


def transform_register_data(full_path_file: str) -> Dict[str, Dict]:
    register_generator = RegisterTransformer(full_path_file)
    dict_registers: Dict[str, List[AbstractRegister]] = register_generator.build()

    return {catering: to_dict(registers) for catering, registers in dict_registers.items()}
