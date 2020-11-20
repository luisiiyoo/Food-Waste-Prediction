from App.Util import DIETS
from App.Util.helpers import str_to_timestamp


class AbstractRegister:
    def __init__(self, date: str, person: str, request: bool, attend: bool, diet: str):
        timestamp = int(str_to_timestamp(date))
        self._id = f"{timestamp}-{person.strip().replace(' ','_')}"
        self.person = person
        self.date = date
        self.request = request
        self.attend = attend
        if diet == '':
            self.diet = None
        elif diet not in DIETS:
            raise Exception(f"'{diet}' is an invalid diet. Please use a valid diet: {DIETS}.")
        else:
            self.diet = diet


class BreakfastRegister(AbstractRegister):
    def __init__(self, date: str, person: str, request: bool, attend: bool, diet: str):
        super().__init__(date, person, request, attend, diet)


class LunchRegister(AbstractRegister):
    def __init__(self, date: str, person: str, request: bool, attend: bool, diet: str, extra: bool):
        super().__init__(date, person, request, attend, diet)
        self.extra = extra
