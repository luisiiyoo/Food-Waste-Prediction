from typing import Dict, List
from App.DataTransformers import MenuTransformer
from App.Models.menu import Menu
from App.Util.helpers import to_dict


def transform_menu_data(full_path_file: str) -> Dict[str, Dict]:
    menu_generator = MenuTransformer(full_path_file)
    menus: Dict[str, List[Menu]] = menu_generator.build()
    menus = {catering: to_dict(menu) for catering, menu in menus.items()}
    return menus
