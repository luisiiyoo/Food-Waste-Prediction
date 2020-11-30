import pandas
from typing import Dict, List
from App.Util.constants import CATERINGS, NUM_DAYS_SERVICE, NO_SERVICE_TAGS, MenuFields
from App.Models import Menu


class MenuTransformer:
    """
    MenuTransformer class to extract menus from raw text

    Args:
        full_path_file (str): Full path of the file to extract the sample_data
        catering_col_idx (int): Catering index column
        diet_col_idx (int): Diet index column

    Attributes:
        full_path_file (str): Full path of the file to extract the sample_data
        catering_col_idx (int): Catering index column
        diet_col_idx (int): Diet index column
    """

    def __init__(self, full_path_file: str, catering_col_idx: int = 0, diet_col_idx: int = 1):
        self.full_path_file = full_path_file
        self.catering_col_idx = catering_col_idx
        self.diet_col_idx = diet_col_idx

    def build(self, separator: str = "\t") -> Dict[str, List[Menu]]:
        """
        Extracts the sample_data from the file provided on the constructor

        Args:
            separator (str): Raw text separator to delimiter a new entry

        Returns:
            Dict[str, List[Menu]]: Dictionary containing the sample_data extracted by catering
        """
        df = pandas.read_csv(self.full_path_file, sep=separator)
        menus: Dict[str, List[Menu]] = {catering: self.__get_menus_by_catering(df, catering) for catering in CATERINGS}
        return menus

    def __get_menus_by_catering(self, df: pandas.DataFrame, catering: str) -> List[Menu]:
        """
        Transforms the raw sample_data to a list of Menus

        Args:
            df (pandas.DataFrame): Raw sample_data
            catering (str): Catering to extract the sample_data

        Returns:
            List[Menu]: List of menus
        """
        days_columns = df.columns[-NUM_DAYS_SERVICE:].tolist()
        same_catering_diet_indexes = df.index[df.iloc[:, self.catering_col_idx].str.lower() == catering].tolist()

        records_catering: List[Menu] = []
        for day_column in days_columns:
            record: Dict[str, str] = dict()
            record[MenuFields.DATE] = df.loc[0, day_column]
            record[MenuFields.DAY] = day_column.lower()

            for row_idx in same_catering_diet_indexes:
                diet: str = df.iloc[row_idx, self.diet_col_idx].strip().lower()
                dish: str = df.loc[row_idx, day_column].strip().lower()

                record[MenuFields.IS_SERVICE_DAY] = dish not in NO_SERVICE_TAGS
                record[diet] = dish if record[MenuFields.IS_SERVICE_DAY] else None

            menu_catering = Menu(date=record[MenuFields.DATE], day=record[MenuFields.DAY],
                                 is_service_day=record[MenuFields.IS_SERVICE_DAY],
                                 regular=record[MenuFields.REGULAR], light=record[MenuFields.LIGHT],
                                 vegan=record[MenuFields.VEGAN],
                                 vegetarian=record[MenuFields.VEGETARIAN])
            records_catering.append(menu_catering)
        return records_catering
