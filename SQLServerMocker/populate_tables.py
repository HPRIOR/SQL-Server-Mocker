from SQLServerMocker.get_database import *
from SQLServerMocker.generators import *


class PopulateTable:
    """
    generates string to populate table
    """
    def __init__(self, db_name: str, table: Table, num_rows: int, generators: [Generator]):
        self.table = table
        self.num_rows = num_rows
        self.generators = generators
        self.db_name = db_name

    def string_builder(self):
        s = ""
        s += f"INSERT into {self.db_name}.dbo.{self.table.name} ({', '.join([col.name for col in self.table.columns])})\n"
        s += "VALUES\n"
        for i in range(self.num_rows):
            s += "("
            for generator in self.generators:
                s += generator.next()
            if i < self.num_rows:
                s += "), \n"
            else:
                s += ") \n"




class Controller:
    """
    Coordinates generation of table values
    checks table for fk/pk values, determines which generator is called by PopulateTable
    """
    def __init__(self, db: DataBase, nums_rows: [int]):
        self.db = db
        self.nums_rows = nums_rows

    def has_fk(self, table: Table) -> object:
        has_fk = False
        for col in table.columns:
            if col.foreign_key != "None":
                has_fk = True
        return has_fk
