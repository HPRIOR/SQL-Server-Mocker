import json


def debug_db(file_name, get_dict):
    db = CreateDataBase(get_dict(file_name)).get_db()
    print(db)
    for table in db.tables:
        print(table)
        for column in table.columns:
            print(column)


def get_json(json_file) -> dict:
    with open(json_file) as tables:
        return json.load(tables)


class Column:
    def __init__(self, name: str, primary_key: bool, foreign_key: bool, not_null: bool, data_type: str):
        self.name = name
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.not_null = not_null
        self.data_type_original = data_type
        self.data_type = self.convert_data_type()

    def convert_data_type(self):
        if self.data_type_original in "int" or self.data_type_original in "intsmall" or self.data_type_original in "year" or self.data_type_original in "intEvenSmaller":
            return "INT"
        else:
            return "VARCHAR(100)"

    def __str__(self):
        return f"Column: {self.name} \n primary key: {self.primary_key} \n" \
               f" foreign key: {self.foreign_key} \n not null: {self.not_null} \n " \
               f"original data type: {self.data_type_original} \n db data type: {self.data_type} \n"


class Table:
    def __init__(self, table_name: str, columns: [Column]):
        self.table_name = table_name
        self.columns = columns

    def __str__(self):
        return f"Table: {self.table_name} \n" \
               f" Columns {[c.name for c in self.columns]} \n"


class DataBase:
    def __init__(self, db_name: str, tables: [Table]):
        self.db_name = db_name
        self.tables = tables

    def __str__(self):
        return f"Database name: {self.db_name} \n " \
               f"Tables: {[t.table_name for t in self.tables]} \n"


class CreateDataBase:
    def __init__(self, dictionary: dict):
        self.db_dict = dictionary
        self.db = self.get_db()

    def get_columns(self, columns: [dict]) -> [Column]:
        return [Column(c['name'], c['primary_key'], c['foreign_key'], c['not_null'],
                       c['data_type']) for c in columns]

    def get_tables(self) -> [Table]:
        return [Table(t['table_name'], self.get_columns(t['columns']))
                for t in self.db_dict["database"]]

    def get_db(self) -> DataBase:
        return DataBase(self.get_db_name(), self.get_tables())

    def get_db_name(self) -> str:
        return self.db_dict['db_name']


debug_db("..\json_tables\\test_table.json", get_json)