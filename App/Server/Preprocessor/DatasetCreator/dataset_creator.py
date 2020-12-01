import pandas
from termcolor import cprint
from typing import List, Dict, Set, Tuple, Union
from App.Util.constants import DIETS, MenuFields, RegisterFields, DatasetFields
from App.Server.Preprocessor.BagOfWords import BagOfWords


def get_data_satisfy_condition(df: pandas.DataFrame, col_name: str, value: Union[str, bool]) -> pandas.DataFrame:
    """
    Gets records with a specific value in a column

    Args:
        df (pandas.DataFrame): Data
        col_name (str): Column name to filter data
        value (Union[str, bool]): Value to match into the data frame and get the records

    Returns:
        df_value (pandas.DataFrame): Data frame that contains the filtered records
    """
    return df.loc[df[col_name] == value, :]


class DatasetCreator:
    """
    GroupData class to create a new data set that merge the information about Registers, Menus and BagOfWords instance
    previously obtained

    Args:
        df_registers (pandas.DataFrame): DataFrame that contains the data about registers
        df_menus (pandas.DataFrame): DataFrame that contains the data about menus
        menu_bow (BagOfWords): BagOfWords instance that contains the instance of BagOfWords

    Attributes:
        df_registers (pandas.DataFrame): Data frame that contains the records about registers
        df_menu (pandas.DataFrame): Data frame that contains the records about menus
        menu_bow (BagOfWords): BagOfWords instance previously obtained
        common_dates (): Dates that match between df_registers and df_menu
        different_dates (): Dates that don't match between df_registers and df_menu
    """

    def __init__(self, df_registers: pandas.DataFrame, df_menus: pandas.DataFrame, menu_bow: BagOfWords):
        filter_col_name_menu = MenuFields.IS_SERVICE_DAY
        self.df_menu = df_menus.loc[df_menus[filter_col_name_menu], :].reset_index(drop=True)
        self.df_registers = df_registers.fillna('')
        self.menu_bow = menu_bow
        self.common_dates: List[str] = []
        self.different_dates: List[str] = []

    def __get_common_dates(self, date_col_name: str) -> Tuple[List[str], List[str]]:
        """
        Gets the common dates between Registers and Menu data frames

        Args:
            date_col_name (str): Column name that refers to dates in both data frames

        Returns:
            common_dates (List[str]): List of strings in common between Registers and Menu data frames
            different_dates (List[str]): List of different strings between Registers and Menu data frames
        """
        registers_unique_dates: Set = set(self.df_registers[date_col_name].unique())
        menu_unique_dates: Set = set(self.df_menu[date_col_name].unique())

        common_dates: Set = registers_unique_dates.intersection(menu_unique_dates)
        all_dates: Set = registers_unique_dates.union(menu_unique_dates)
        different_dates: Set = all_dates - common_dates
        return list(common_dates), list(different_dates)

    def build(self) -> List[Dict[str, Union[str, int]]]:
        """
        Groups the data to generate a new frame

        Args:
            None

        Returns:
            List[Dict[str, Union[str, int]]]: Merged dataset
        """
        self.common_dates, self.different_dates = self.__get_common_dates(DatasetFields.DATE)
        bow_features: List[str] = self.menu_bow.get_features()
        cprint(f'Common dates: {len(self.common_dates)}. Dates not included: {len(self.different_dates)}', 'yellow')

        grouped_data: List[Dict[str, Union[str, int]]] = []
        for idx, date in enumerate(self.common_dates):
            menu: pandas.DataFrame = get_data_satisfy_condition(self.df_menu, MenuFields.DATE, date)
            registers: pandas.DataFrame = get_data_satisfy_condition(self.df_registers, RegisterFields.DATE, date)

            no_request = get_data_satisfy_condition(registers, RegisterFields.REQUEST, False)
            request = get_data_satisfy_condition(registers, RegisterFields.REQUEST, True)

            attend_request = get_data_satisfy_condition(request, RegisterFields.ATTEND, True)
            no_attend_request = get_data_satisfy_condition(request, RegisterFields.ATTEND, False)

            for diet in DIETS:
                diet_request = len(get_data_satisfy_condition(request, RegisterFields.DIET, diet))
                diet_attend_request = len(get_data_satisfy_condition(attend_request, RegisterFields.DIET, diet))

                raw_text: List[str] = menu[diet].values
                bow_vector: List[int] = self.menu_bow.vectorize_raw_data(raw_text)[0].tolist()
                bow_dict = dict(zip(bow_features, bow_vector))

                group_record: Dict[str, Union[str, int]] = dict()
                group_record['_id'] = f"{date}_{diet}"
                group_record[DatasetFields.DATE] = date
                group_record[DatasetFields.DAY] = menu[MenuFields.DAY].values[0]
                group_record[DatasetFields.DIET] = diet
                group_record[DatasetFields.TOTAL_PEOPLE] = len(registers)
                group_record[DatasetFields.TOTAL_REQUESTS] = len(request)
                group_record[DatasetFields.REQUEST] = diet_request
                group_record[DatasetFields.ATTEND] = diet_attend_request
                grouped_data.append({**bow_dict, **group_record})
        return grouped_data
