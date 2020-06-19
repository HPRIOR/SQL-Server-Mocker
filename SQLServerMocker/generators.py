import random
from abc import ABC, abstractmethod
from collections import defaultdict


def get_gen_dict() -> dict:
    return {
        "date": GenerateDate(),
        "int": GenerateRandomInt(100),
        "string": GenerateRandomStringCollection("a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, "
                                                 "w, x, y, z", 5)
    }


class Generator(ABC):
    @abstractmethod
    def next(self) -> str:
        pass


class GenerateID(Generator):
    def __init__(self, col_name):
        self.col_name = col_name
        self.iter = 0

    def next(self) -> str:
        r_val = f"'{self.col_name}_{self.iter}'"
        self.iter += 1
        return r_val


class GenerateDate(ABC):
    def __init__(self):
        self.current = 1

    def next(self) -> str:
        val_return = "\'" + self.get_year() + "-" + str(self.current) + "-" + self.get_day() + "\'"
        self.current += 1
        return val_return

    def get_year(self):
        return str(random.randint(1950, 2020))

    def get_day(self):
        return str(random.randint(1, 30))


class GenerateRandomInt(ABC):
    def __init__(self, rng):
        self.range = rng

    def next(self) -> str:
        return random.randint(1, self.rng)


class GenerateRandomStringCollection(ABC):
    """
    range specifies length of string, string should be a comma seperated list of items
    """

    def __init__(self, string, range):
        self.letters = string.split(', ')
        self.range = range

    def next(self) -> str:
        s = ""
        for i in range(self.range):
            r = random.randint(0, self.range)
            s += self.letters[r]
        return "\'" + s + "\'"


class ReferenceDict:
    """
    contains dictionary:
    key = column reference which has already been created
    value = values which have been created for that column reference
    this is used to create FKValueGenerators
    """

    def __init__(self):
        self.dict = defaultdict(list)

    def populate_dict(self, column_key, value):
        self.dict[column_key].append(value)


class FKValueGenerator(ABC):
    """
    gives random values from the reference Dict
    """
    def __init__(self, values: list):
        self.values = values
        self.rand_seq = random.sample(range(0, len(values)), len(values))
        self.index = 0

    def next(self) -> str:
        if self.index < len(self.values) - 1:
            _ = self.values[self.rand_seq[self.index]]
            self.index += 1
            return "\'" + _ + "\'"
        else:
            self.index = 0
            self.rand_seq = random.sample(range(0, len(self.values)), len(self.values))
            _ = self.values[self.rand_seq[self.index]]
            self.index += 1
            return "\'" + _ + "\'"







