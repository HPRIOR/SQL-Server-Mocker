from abc import ABC, abstractmethod

"""
This file defines a group of classes that handle input into the GUI. e.g. DKMString takes a specific format of string
and converts is into a list of dictionaries containing: {table} -> {rows}. This is returned through the table list 
method
"""

class StrToDbInfo(ABC):
    @abstractmethod
    def table_list(self) -> [dict]:
        pass


class DKMString(StrToDbInfo):
    def __init__(self, db_string):
        self.db_string = db_string

    def table_strings(self, inp: str) -> [str]:
        return [s for s in inp.split("\n")]

    def table_dict(self, t_str: str) -> tuple:
        return (
            t_str.split(" ")[0].strip(), [s.strip() for s in t_str[t_str.find("(") + 1: t_str[1].find(")")].split(", ")]
        )

    def table_list(self) -> [dict]:
        return [self.table_dict(t_str) for t_str in self.table_strings(self.db_string)]


