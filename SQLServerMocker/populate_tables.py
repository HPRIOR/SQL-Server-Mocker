from SQLServerMocker.get_database import *
from SQLServerMocker.generators import *


class PopulateTable:
    """
    generates string to populate table
    """

    def __init__(self, db: DataBase, nums_rows: [int]):
        self.db = db
        self.nums_rows = nums_rows
        self.ref_dict = ReferenceDict()
        self.gen_dict = get_gen_dict()

    def db_string_builder(self):
        """does foreign keys first, then loop until each table has a foreign key match in ref dict """
        _ = ""
        _ += self.build_no_fk([table for table in self.db.tables if not self.has_fk(table)])
        _ += self.build_fk([table for table in self.db.tables if self.has_fk(table)])
        return _

    def build_no_fk(self, tables: [Table]) -> str:
        _ = " "
        for enum, table in enumerate(tables):
            _ += self.table_string_builder(table, self.get_generator_array(table, self.ref_dict), self.nums_rows[enum])
            return _

    def build_fk(self, tables: [Table]) -> str:
        _ = ""
        while len(tables) > 0:
            for enum, table in enumerate(tables):
                if self.has_col_in_ref_dict(table):
                    _ += self.table_string_builder(table, self.get_generator_array(table, self.ref_dict), self.nums_rows[enum])
                    tables.remove(table)
        return _

    def table_string_builder(self, table: Table, generators: [Generator], num_rows: int) -> str:
        col_names = [col.name for col in table.columns]
        s = ""
        s += f"INSERT into {self.db.name}.dbo.{table.name} ({', '.join([col.name for col in table.columns])})\n"
        s += "VALUES\n"
        for i in range(num_rows):
            s += "("
            for j in range(len(generators)):
                _ = generators[j].next()
                if j < len(generators) - 1:
                    s += str(_) + ", "
                else:
                    s += _
                self.ref_dict.populate_dict(col_names[j], _)
            if i < num_rows - 1:
                s += "), \n"
            else:
                s += ") \n \n"
        return s

    def get_generator_array(self, table: Table, ref_dict: ReferenceDict) -> [Generator]:
        """returns an array of appropriate generators"""
        return [self.get_generator(col, self.gen_dict, ref_dict) for col in table.columns]

    def get_generator(self, col: Column, gen_dict: dict, ref_dict: ReferenceDict) -> Generator:
        """contains logic which returns the correct generator (fk -> ref_gen, id -> id gen, else -> gen_dict)"""
        if col.foreign_key != "None":
            return FKValueGenerator(ref_dict.dict[col.name])
        else:
            if col.data_type == "id":
                return GenerateID(col.name)
            else:
                return gen_dict[col.data_type_og]

    def has_col_in_ref_dict(self, table: Table) -> bool:
        """returns true if every foreign key the table has a match in the reference dictionary"""
        _ = [True if col.name in self.ref_dict.dict
             else False for col in [col for col in table.columns if col.foreign_key != "None"]]
        return not False in _

    def has_fk(self, table: Table) -> bool:
        """returns true if a table has a foreign key"""
        has_fk = False
        for col in table.columns:
            if col.foreign_key != "None":
                has_fk = True
        return has_fk


d = CreateDataBase(get_json("..\json_tables\\test_foreign_key.json")).get_db()

rows = [10, 5]

p = PopulateTable(d, rows)

print(p.db_string_builder())
