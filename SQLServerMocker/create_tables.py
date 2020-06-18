from SQLServerMocker.get_database import *


class CreateTable:
    def __init__(self, db: DataBase):
        self.db = db
        self.table_string: str = ""

    def initial_string(self, table: Table) -> str:
        return f"CREATE TABLE {self.db.name}.dbo.{table.name} (\n"

    def column_string(self, table: Table) -> str:
        return "".join([f"{col.name} {col.data_type} NOT NULL,\n" if col.not_null
                        else f"{col.name} {col.data_type}\n" for col in table.columns])

    def constraint_string(self, table: Table) -> str:
        return "".join([f"FOREIGN KEY ({col.name}) REFERENCES {self.db.name}.dbo.{col.foreign_key} ({col.name}), \n"
                        for col in table.columns if col.foreign_key != "None"])

    def primary_key_string(self, table: Table) -> str:
        return f"PRIMARY KEY ({', '.join([col.name for col in table.columns if col.primary_key])}) \n \n"

    def string_builder(self) -> str:
        s = ""
        for table in self.db.tables:
            s += self.initial_string(table)
            s += self.column_string(table)
            s += self.constraint_string(table)
            s += self.primary_key_string(table)
        return s

    # add logic to govern the order of create tables (e.g. those with foreign keys are made last)


c = CreateTable(CreateDataBase(get_json("..\json_tables\\test_table.json")).get_db())

print(c.string_builder())
