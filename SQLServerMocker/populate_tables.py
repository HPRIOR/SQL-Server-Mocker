from SQLServerMocker.get_database import *
from SQLServerMocker.generators import *


class PopulateTables:
    """
    generates string to populate tables
    """

    def __init__(self, db: DataBase):
        self.db = db
        self.tables = db.tables
        self.gen_dict = get_gen_dict()
        self.ref_dict = self.populate_ref_dict(self.tables, self.fk_references(self.tables, self.has_fk),
                                               self.get_generator)

    def db_string_builder(self) -> str:
        """applies table_string_builder to each table and concatenates the resulting string"""
        return "\n".join([self.table_string_builder(table, self.get_gen_array(table, self.ref_dict, self.get_generator),
                                                    self.db.name)
                          for table in self.tables])

    def table_string_builder(self, table: Table, generators: [Generator], db_name: str) -> str:
        """Gets values from the supplied generators for each column within a table"""
        s = f"INSERT into {db_name}.dbo.{table.name} ({', '.join([col.name for col in table.columns])})\n"
        s += "VALUES\n"
        for i in range(table.rows):
            s += "(" + ", ".join([str(gen.next()) for gen in generators])
            s += "),\n" if i < table.rows - 1 else ")\n"
        return s

    def get_gen_array(self, table: Table, ref_dict: ReferenceDict, get_gen) -> [Generator]:
        """
        Contains the logic for getting array of generators: namely, getting generators for
        foreign keys (both referring and referenced)
        """
        gens = []
        for col in table.columns:
            if col.foreign_key != "None":
                gens.append(FKValueGenerator(ref_dict.dict[col.foreign_key][col.name]))
            elif table.name in ref_dict.dict and col.name in ref_dict.dict[table.name]:
                gens.append(ValueGenerator(ref_dict.dict[table.name][col.name]))
            else:
                gens.append(get_gen(col, get_gen_dict()))
        return gens

    def get_generator(self, col: Column, gen_dict: dict):
        """ will return appropriate generator based on the data_type of column"""
        return GenerateID(col.name) if col.data_type_og == "id" else gen_dict[col.data_type_og]

    def fk_references(self, tables: [Table], has_fk) -> [str, str]:
        """returns col_names and table references for foreign key columns"""
        fk_ref = []
        for table in [table for table in tables if has_fk(table)]:
            for col in table.columns:
                if col.foreign_key != "None":
                    fk_ref.append((col.name, col.foreign_key))
        return fk_ref

    def populate_ref_dict(self, tables: [Table], fk_refs: [str, str], get_generator):
        """populates the reference dictionary with: table -> col_name -> values"""
        r_dict = ReferenceDict()
        for table in tables:
            for col in table.columns:
                for col_name, table_ref in fk_refs:
                    if table_ref == table.name and col_name == col.name:
                        gen = get_generator(col, get_gen_dict())
                        for i in range(table.rows):
                            r_dict.populate_table_refs(table.name, col.name, gen.next())
        return r_dict

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
