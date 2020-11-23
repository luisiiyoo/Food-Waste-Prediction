import pandas
from termcolor import cprint
from typing import Dict, List, Tuple
from App.Util.constants import NO_SERVICE_TAGS, EXTRA_TAG, COLOR_BREAKFAST, COLOR_LUNCH, DIETS
from App.Models import BreakfastRegister, LunchRegister
from App.Util.helpers import datetime_to_str
from App.Models.registers_collection import RegistersCollection

INDEX_START = 1
DATE = 'date'
PERSON = 'person'
DIET = 'diet'
ATTEND = 'attend'
REQUEST = 'request'
EXTRA = 'extra'


def df_to_breakfast_register(df: pandas.DataFrame) -> List[BreakfastRegister]:
    return [
        BreakfastRegister(date=row[DATE], person=row[PERSON], request=row[REQUEST], attend=row[ATTEND], diet=row[DIET])
        for _, row in df.iterrows()]


def df_to_lunch_register(df: pandas.DataFrame) -> List[LunchRegister]:
    return [
        LunchRegister(date=row[DATE], person=row[PERSON], request=row[REQUEST], attend=row[ATTEND], diet=row[DIET],
                      extra=row[EXTRA]) for _, row in df.iterrows()]


class RegisterTransformer:
    def __init__(self, full_path_file: str, breakfast_cols_idx: List[int] = [0, 1, 2],
                 lunch_cols_idx: List[int] = [0, 4, 5]):
        self.full_path_file = full_path_file
        self.breakfast_cols_idx = breakfast_cols_idx
        self.lunch_cols_idx = lunch_cols_idx

    def build(self) -> Tuple[RegistersCollection, RegistersCollection]:
        cprint('Extracting Breakfast data.', COLOR_BREAKFAST)
        df_breakfast = self.__extract_data(self.breakfast_cols_idx, False)
        cprint('Extracting Lunch data.', COLOR_LUNCH)
        df_lunch = self.__extract_data(self.lunch_cols_idx, True)
        breakfast_registers = RegistersCollection(df_to_breakfast_register(df_breakfast),
                                                  list(df_breakfast[DATE].unique()))
        lunch_registers = RegistersCollection(df_to_breakfast_register(df_lunch), list(df_lunch[DATE].unique()))
        return breakfast_registers, lunch_registers

    def __extract_data(self, cols_idx: List[int], check_extra_meals: bool) -> pandas.DataFrame:
        xls_file = pandas.ExcelFile(self.full_path_file)
        sheets = xls_file.sheet_names
        frames: List[pandas.DataFrame] = []
        for sheet in sheets:
            df = pandas.read_excel(self.full_path_file, sheet_name=sheet)

            # is_service_day = (df.iloc[0:5, 0].str.lower() == 'holiday').sum() == 0
            first_rows = list(df.iloc[0:5, 0].str.lower().values)
            is_service_day = all(record not in NO_SERVICE_TAGS for record in first_rows)
            if not is_service_day:
                print(f'Skip {sheet} because it has one NO_SERVICE_TAGS: {NO_SERVICE_TAGS}')
                continue
            df = df.iloc[INDEX_START:, cols_idx]

            # Rename the columns
            col_names_old = df.columns
            date_record = col_names_old[0]
            col_names_new = [PERSON, DIET, ATTEND]
            col_names_dict = dict(zip(col_names_old, col_names_new))
            df = df.rename(columns=col_names_dict)

            # Converting to the correct data type
            df[REQUEST] = df.loc[:, DIET].notnull().tolist()
            df[DATE] = datetime_to_str(date_record)
            df[ATTEND] = df[ATTEND].astype('bool')

            # Keep data that is not empty on PERSON column
            df = df[df[PERSON].notna()]

            # Reset index
            df.reset_index(drop=True, inplace=True)
            df = df[[PERSON, DATE, REQUEST, ATTEND, DIET]]

            df[DIET] = df[DIET].fillna('').str.lower().str.strip()
            if check_extra_meals:
                df[EXTRA] = df[DIET].str.contains(EXTRA_TAG, regex=False)
                df[DIET] = df[DIET].map(lambda diet: str(diet).replace(EXTRA_TAG, ''))
            df[DIET] = df[DIET].map(remove_extra_tag)

            # Removing not valid diets records
            valid_diets = ['', *DIETS]
            df = df[df[DIET].isin(valid_diets)]
            # Removing duplicated records and keeping the last
            df = df.drop_duplicates(subset=PERSON, keep="last")
            frames.append(df)

        df_breakfast = pandas.concat(frames, ignore_index=True, axis=0)
        df_breakfast.sort_values(by=[DATE], ascending=True, inplace=True)
        return df_breakfast.reset_index(drop=True)


def remove_extra_tag(diet: str):
    diet_extra = diet.split()
    return diet if len(diet_extra) == 0 else diet_extra[0]
