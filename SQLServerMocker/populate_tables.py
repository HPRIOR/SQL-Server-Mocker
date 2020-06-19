from SQLServerMocker.get_database import *
from SQLServerMocker.generators import *


class PopulateTable:
    """
    generates string to populate table
    """

    def __init__(self, db: DataBase, nums_rows: [int]):
        self.db = db
        self.num_rows = nums_rows
        self.ref_dict = ReferenceDict()
        self.gen_dict = get_gen_dict()

    def db_string_builder(self):
        pass


    def table_string_builder(self, table: Table, generators: [Generator], num_rows: int) -> str:
        s = ""
        s += f"INSERT into {self.db.name}.dbo.{table.name} ({', '.join([col.name for col in table.columns])})\n"
        s += "VALUES\n"
        for i in range(num_rows):
            s += "("
            s += ", ".join([generator.next() for generator in generators])
            # add values to fk dict here
            if i < self.num_rows:
                s += "), \n"
            else:
                s += ") \n"
        return s

    def get_generator_array(self, table: Table, gen_dict: dict, ref_dict: dict) -> [Generator]:
        """returns an array of appropriate generators"""
        return [self.get_generator(col, gen_dict, ref_dict) for col in table.columns]

    def get_generator(self, col: Column, gen_dict: dict, ref_dict: ReferenceDict) -> Generator:
        """contains logic which returns the correct generator (fk -> ref_gen, id -> id gen, else -> gen_dict)"""
        if col.foreign_key != "None":
            return ref_dict.dict[col.data_type_og]
        else:
            if col.data_type == "id":
                return GenerateID(col.name)
            else:
                return gen_dict[col.data_type_og]

    def check_ref_dict(self, table: Table) -> bool:
        """returns true if every foregeign key the table has a match in the reference dictionary"""
        _ = [True if col.foreign_key != "None" and col.name in self.ref_dict else False for col in table.columns]
        return not False in _

    def has_fk(self, table: Table) -> bool:
        """returns true if a table has a foreign key"""
        has_fk = False
        for col in table.columns:
            if col.foreign_key != "None":
                has_fk = True
        return has_fk
