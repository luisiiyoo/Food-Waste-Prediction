import pandas
from typing import Dict, List
from App.Util.constants import CATERINGS, NUM_DAYS_SERVICE, NO_SERVICE_TAGS
from App.Models import Menu

DATE = 'date'
DAY = 'day'
IS_SERVICE_DAY = 'is_service_day'
REGULAR = 'regular'
LIGHT = 'light'
VEGAN = 'vegan'
VEGETARIAN = 'vegetarian'


class MenuTransformer:
    def __init__(self, full_path_file: str, catering_col_idx: int = 0, diet_col_idx: int = 1):
        self.full_path_file = full_path_file
        self.catering_col_idx = catering_col_idx
        self.diet_col_idx = diet_col_idx

    def build(self, separator: str = "\t") -> Dict[str, List[Menu]]:
        df = pandas.read_csv(self.full_path_file, sep=separator)
        menus: Dict[str, List[Menu]] = {catering: self.__get_menus_by_catering(df, catering) for catering in CATERINGS}
        return menus

    def __get_menus_by_catering(self, df: pandas.DataFrame, catering: str) -> List[Menu]:
        days_columns = df.columns[-NUM_DAYS_SERVICE:].tolist()
        same_catering_diet_indexes = df.index[df.iloc[:, self.catering_col_idx].str.lower() == catering].tolist()

        records_catering: List[Menu] = []
        for day_column in days_columns:
            record: Dict[str, str] = dict()
            record[DATE] = df.loc[0, day_column]
            record[DAY] = day_column.lower()

            for row_idx in same_catering_diet_indexes:
                diet: str = df.iloc[row_idx, self.diet_col_idx].strip().lower()
                dish: str = df.loc[row_idx, day_column].strip().lower()

                dish = dish.replace('*', '').replace('+', 'and')

                record[IS_SERVICE_DAY] = dish not in NO_SERVICE_TAGS
                record[diet] = dish if record[IS_SERVICE_DAY] else None

            menu_catering = Menu(date=record[DATE], day=record[DAY], is_service_day=record[IS_SERVICE_DAY],
                                 regular=record[REGULAR], light=record[LIGHT], vegan=record[VEGAN],
                                 vegetarian=record[VEGETARIAN])
            records_catering.append(menu_catering)
        return records_catering
