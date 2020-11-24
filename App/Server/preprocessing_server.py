from typing import Dict, List
from App.Models import Menu
from App.Util.helpers import to_dict
from App.Preproccessing.DataTransformers import MenuTransformer, RegisterTransformer
from App.Util.constants import BREAKFAST, LUNCH
from App.Database import save_transformed_data


def transform_menu_data(full_path_file: str) -> Dict[str, Dict]:
    try:
        menu_generator = MenuTransformer(full_path_file)
        dict_menus: Dict[str, List[Menu]] = menu_generator.build()

        save_transformed_data.save_menus(dict_menus)

        return {catering: to_dict(menus) for catering, menus in dict_menus.items()}
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to menu data.")


def transform_register_data(full_path_file: str) -> Dict[str, Dict]:
    try:
        register_generator = RegisterTransformer(full_path_file)
        breakfast_registers, lunch_registers = register_generator.build()

        save_transformed_data.save_register(breakfast_registers, lunch_registers)

        return {
            BREAKFAST: to_dict(breakfast_registers),
            LUNCH: to_dict(lunch_registers)
        }
    except IndexError as e:
        raise Exception("The file has not a valid structure for transforming to register data.")
