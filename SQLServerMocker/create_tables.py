from SQLServerMocker.get_database import CreateDataBase, DataBase, Table, get_json


class CreateTable:
    def __init__(self, db: DataBase):
        self.db = db
        self.table_string: str = ""

    def initial_string(self, table: Table) -> str:
        return f"CREATE TABLE {self.db.name}.dbo.{table.name} (\n"

    def column_string(self, table: Table) -> str:
        cols = ""
        for col in table.columns:
            if col.not_null:
                cols += f"{col.name} {col.data_type} NOT NULL,\n"
            else:
                cols += f"{col.name} {col.data_type},\n"
        return cols

    def constraint_string(self, table: Table) -> str:
        cols = ""
        for col in table.columns:
            if col.foreign_key != "None":
                cols += f"FOREIGN KEY ({col.name}) REFERENCES {self.db.name}.dbo.{col.foreign_key} ({col.name}), \n"
        return cols

    def primary_key_string(self, table: Table) -> str:
        s = ""
        pk_list = [col.name for col in table.columns if col.primary_key]
        for enum, key in enumerate(pk_list):
            if enum < len(pk_list) - 1:
                s += key + ", "
            else:
                s += key
        return f"PRIMARY KEY ({s}) \n \n"

    def string_builder(self, table: Table) -> str:
        s = ""
        s += self.initial_string(table)
        s += self.column_string(table)
        s += self.constraint_string(table)
        s += self.primary_key_string(table)
        return s

    def table_loop(self):
        for table in self.db.tables:
            self.table_string += self.string_builder(table)


c = CreateTable(CreateDataBase(get_json("..\json_tables\\test_table.json")).get_db())

c.table_loop()

print(c.table_string)
