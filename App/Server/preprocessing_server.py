from typing import Dict, List
import pandas
from App.Database import query_data


def build_menus_bow_model(catering: str) -> List[Dict]:
    menus: List[Dict] = [document for document in query_data.get_menus(catering)]
    df = pandas.DataFrame(data=menus).set_index('_id').sort_index()
    print(df.head())
    return menus
