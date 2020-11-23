from typing import List, Union
from App.Models.register import BreakfastRegister, LunchRegister


class RegistersCollection:
    def __init__(self, registers: List[Union[BreakfastRegister, LunchRegister]], dates: List[str]):
        self.registers = registers
        self.dates = dates
