from SQLServerMocker.get_database import *
from SQLServerMocker.generators import *


class PopulateTables:
    """
    generates strings to populate tables
    """
    def __init__(self, db: DataBase):
        self.db = db
        self.ref_dict = ReferenceDict()
        self.gen_dict = get_gen_dict()

    def db_string_builder(self):
        """Builds string of tables without foreign keys first, then those with foreign keys -
        ensures foreign key references in ref_dict"""
        _ = ""
        _ += str(self.build_no_fk([table for table in self.db.tables if not self.has_fk(table)]))
        _ += str(self.build_fk([table for table in self.db.tables if self.has_fk(table)]))
        return _

    def build_no_fk(self, tables: [Table]) -> str:
        _ = ""
        for table in tables:
            _ += self.table_string_builder(table, self.get_generator_array(table, self.ref_dict), table.rows)
            return _

    def build_fk(self, tables: [Table]) -> str:
        _ = ""
        while len(tables) > 0:
            for table in tables:
                if self.has_col_in_ref_dict(table):
                    _ += self.table_string_builder(table, self.get_generator_array(table, self.ref_dict), table.rows)
                    tables.remove(table)
        return _

    def table_string_builder(self, table: Table, generators: [Generator], num_rows: int) -> str:
        col_names = [col.name for col in table.columns]
        s = f"INSERT into {self.db.name}.dbo.{table.name} ({', '.join([col.name for col in table.columns])})\n"
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


p = PopulateTables(d)

print(p.db_string_builder())
