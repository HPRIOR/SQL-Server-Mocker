import random
from abc import ABC, abstractmethod


def get_gen_dict():
    pass


class Generator(ABC):
    @abstractmethod
    def next(self):
        pass


class GenerateID(Generator):
    def __init__(self, col_name):
        self.col_name = col_name
        self.iter = 0

    def next(self):
        r_val = f"'{self.col_name}_{self.iter}'"
        self.iter += 1
        return r_val


class ReferenceDict:
    """
    contains dictionary of reference generators:
    key = column reference which has already been created
    value = values which have been created for that column reference
    """
    def __init__(self):
        self.dict = {}

    def populate_dict(self, column_key, value):
        if column_key in self.dict:
            self.dict[column_key] += str(value) + ", "
        else:
            self.dict[column_key] = str(value) + ", "

class FKValueGenerator:
    """
    gives random values from the reference Dict
    """
