import random


def get_gen_dict():
    pass


class Generator:
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


class FKValueGenerator:
    """
    gives random values from the reference Dict
    """
