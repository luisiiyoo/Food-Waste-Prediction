from App.Util.helpers import str_to_timestamp


class Menu:
    def __init__(self, date: str, day: str, is_service_day: str, regular: str, light: str, vegan: str, vegetarian: str):
        self._id = int(str_to_timestamp(date))
        self.date = date
        self.day = day
        self.is_service_day = is_service_day
        self.regular = regular
        self.light = light
        self.vegan = vegan
        self.vegetarian = vegetarian
