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
        r_val = f"'{self.col_name[:3]}_{self.iter}'"
        self.iter += 1
        return r_val


class GenerateDate(Generator):
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


class GenerateRandomInt(Generator):
    def __init__(self, rng):
        self.rng = rng

    def next(self) -> str:
        return random.randint(1, self.rng)


class GenerateRandomStringCollection(Generator):
    """
    range specifies length of string, string should be a comma separated list of items
    """

    def __init__(self, string, rng):
        self.letters = string.split(', ')
        self.range = rng

    def next(self) -> str:
        s = ""
        for i in range(self.range):
            r = random.randint(0, self.range)
            s += self.letters[r]
        return "\'" + s + "\'"


class ReferenceDict:
    """
    contains dictionary:
    {referenced table} -> {column name} -> {list of values}
    this is used to create value generators for fk and referenced columns
    """

    def __init__(self):
        self.dict = {}

    def populate_table_refs(self, table_name: str, column_key: str, value):
        if table_name not in self.dict:
            self.dict[table_name] = defaultdict(list)
        self.dict[table_name][column_key].append(value)


class ValueGenerator(Generator):
    def __init__(self, values: list):
        self.values = values
        self.index = 0

    def next(self) -> str:
        _ = self.values[self.index]
        self.index += 1
        return _


class FKValueGenerator(Generator):
    """
    gives random values from the reference Dict
    """

    def __init__(self, values: list):
        self.values = values
        self.rand_seq = random.sample(range(0, len(values)), len(values))
        self.index = 0

    def next(self) -> str:
        try:
            _ = self.values[self.rand_seq[self.index]]
            self.index += 1
            return _
        except IndexError:
            self.index = 0
            self.rand_seq = random.sample(range(0, len(self.values)), len(self.values))
            _ = self.values[self.rand_seq[self.index]]
            self.index += 1
            return _
