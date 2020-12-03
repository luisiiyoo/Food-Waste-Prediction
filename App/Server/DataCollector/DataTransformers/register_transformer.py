import pandas
from termcolor import cprint
from typing import Dict, List
from App.Util.constants import NO_SERVICE_TAGS, EXTRA_TAG, COLOR_BREAKFAST, COLOR_LUNCH, DIETS, BREAKFAST, LUNCH, \
    RegisterFields
from App.Models import BreakfastRegister, LunchRegister, AbstractRegister
from App.Util.helpers import datetime_to_str

INDEX_START = 1


def df_to_breakfast_register(df: pandas.DataFrame) -> List[BreakfastRegister]:
    """
    Transforms a dataframe to a list of breakfast registers

    Args:
        df (pandas.DataFrame): Registers dataframe to transform to a list of breakfast registers

    Returns:
        List[BreakfastRegister]: List of registers
    """
    return [
        BreakfastRegister(date=row[RegisterFields.DATE], person=row[RegisterFields.PERSON],
                          request=row[RegisterFields.REQUEST], attend=row[RegisterFields.ATTEND],
                          diet=row[RegisterFields.DIET])
        for _, row in df.iterrows()]


def df_to_lunch_register(df: pandas.DataFrame) -> List[LunchRegister]:
    """
    Transforms a dataframe to a list of lunch registers

    Args:
        df (pandas.DataFrame): Registers dataframe to transform to a list of lunch registers

    Returns:
        List[LunchRegister]: List of registers
    """
    return [
        LunchRegister(date=row[RegisterFields.DATE], person=row[RegisterFields.PERSON],
                      request=row[RegisterFields.REQUEST], attend=row[RegisterFields.ATTEND],
                      diet=row[RegisterFields.DIET], extra=row[RegisterFields.EXTRA]) for _, row in df.iterrows()]


def remove_extra_tag(diet: str) -> str:
    """
    Keeps the fist word given a text, i.e. "regular + extras" -> "regular"

    Args:
        diet (str): Text to keep the first word

    Returns:
        str: First word
    """
    diet_extra = diet.split()
    return diet if len(diet_extra) == 0 else diet_extra[0]


class RegisterTransformer:
    """
    RegisterTransformer class to extract people registers from raw text

    Args:
        full_path_file (str): Full path of the file to extract the sample_data
        breakfast_cols_idx (List[int]): Column indexes of breakfast registers
        lunch_cols_idx (List[int]): Column indexes of lunch registers

    Attributes:
        full_path_file (str): Full path of the file to extract the sample_data
        breakfast_cols_idx (List[int]): Column indexes of breakfast registers
        lunch_cols_idx (List[int]): Column indexes of lunch registers
    """

    def __init__(self, full_path_file: str, breakfast_cols_idx: List[int] = [0, 1, 2],
                 lunch_cols_idx: List[int] = [0, 4, 5]):
        self.full_path_file = full_path_file
        self.breakfast_cols_idx = breakfast_cols_idx
        self.lunch_cols_idx = lunch_cols_idx

    def build(self) -> Dict[str, List[AbstractRegister]]:
        """
        Extracts the sample_data from the file provided on the constructor

        Args:
            None

        Returns:
            Dict[str, List[AbstractRegister]]: Registers by catering
        """
        cprint('Extracting Breakfast sample_data.', COLOR_BREAKFAST)
        df_breakfast = self.__extract_data(self.breakfast_cols_idx, False)
        cprint('Extracting Lunch sample_data.', COLOR_LUNCH)
        df_lunch = self.__extract_data(self.lunch_cols_idx, True)

        registers: Dict[str, List[AbstractRegister]] = {
            BREAKFAST: df_to_breakfast_register(df_breakfast),
            LUNCH: df_to_breakfast_register(df_lunch)
        }
        return registers

    def __extract_data(self, cols_idx: List[int], check_extra_meals: bool) -> pandas.DataFrame:
        """
        Extracts the sample_data bny catering (breakfast or lunch)

        Args:
            cols_idx (List[int]): Column indexes to get the sample_data
            check_extra_meals (bool): Validate if the register wants extra meals

        Returns:
            pandas.DataFrame: Registers extracted
        """
        cprint(f"Reading '{self.full_path_file}' as ExcelFile", 'cyan')
        xls_file = pandas.ExcelFile(self.full_path_file)
        sheets = xls_file.sheet_names
        frames: List[pandas.DataFrame] = []
        for sheet in sheets:
            df = pandas.read_excel(self.full_path_file, sheet_name=sheet)

            # is_service_day = (df.iloc[0:5, 0].str.lower() == 'holiday').sum() == 0
            first_rows = list(df.iloc[0:5, 0].str.lower().values)
            is_service_day = all(record not in NO_SERVICE_TAGS for record in first_rows)

            count_attendance = df.iloc[INDEX_START:, cols_idx[-1]].fillna(False).astype('bool').sum()
            if count_attendance == 0:
                cprint(f"Warning: '{sheet}' sheet does not contain records of attendance", 'yellow')
            if not is_service_day:
                cprint(f"Skip '{sheet}' sheet because it has one NO_SERVICE_TAGS: {NO_SERVICE_TAGS}", 'red')
                continue
            df = df.iloc[INDEX_START:, cols_idx]

            # Rename the columns
            col_names_old = df.columns
            date_record = col_names_old[0]
            col_names_new = [RegisterFields.PERSON, RegisterFields.DIET, RegisterFields.ATTEND]
            col_names_dict = dict(zip(col_names_old, col_names_new))
            df = df.rename(columns=col_names_dict)

            # Converting to the correct sample_data type
            df[RegisterFields.REQUEST] = df.loc[:, RegisterFields.DIET].notnull().tolist()
            df[RegisterFields.DATE] = datetime_to_str(date_record)
            df[RegisterFields.ATTEND] = df[RegisterFields.ATTEND].fillna(False).astype('bool')

            # Keep sample_data that is not empty on PERSON column
            df = df[df[RegisterFields.PERSON].notna()]

            # Reset index
            df.reset_index(drop=True, inplace=True)
            df = df[[RegisterFields.PERSON, RegisterFields.DATE, RegisterFields.REQUEST, RegisterFields.ATTEND,
                     RegisterFields.DIET]]

            df[RegisterFields.DIET] = df[RegisterFields.DIET].fillna('').str.lower().str.strip()
            if check_extra_meals:
                df[RegisterFields.EXTRA] = df[RegisterFields.DIET].str.contains(EXTRA_TAG, regex=False)
                df[RegisterFields.DIET] = df[RegisterFields.DIET].map(lambda diet: str(diet).replace(EXTRA_TAG, ''))
            df[RegisterFields.DIET] = df[RegisterFields.DIET].map(remove_extra_tag)

            # Removing not valid diets records
            valid_diets = ['', *DIETS]
            df = df[df[RegisterFields.DIET].isin(valid_diets)]
            # Removing duplicated records and keeping the last
            df = df.drop_duplicates(subset=RegisterFields.PERSON, keep="last")
            frames.append(df)

        df_breakfast = pandas.concat(frames, ignore_index=True, axis=0)
        df_breakfast.sort_values(by=[RegisterFields.DATE], ascending=True, inplace=True)
        return df_breakfast.reset_index(drop=True)
