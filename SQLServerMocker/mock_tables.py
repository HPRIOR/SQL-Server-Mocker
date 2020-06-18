import json


def get_json(json_file) -> dict:
    with open(json_file) as tables:
        return json.load(tables)


d = get_json("..\json_tables\\test_table.json")
print(d)


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

class Table:
    def __init__(self, table_name: str, columns : [Column]):
        self.table_name = table_name
        self.columns = columns

class DataBase:
    def __init__(self, db_name: str, tables: [Table]):


class ConvertJson:
    def __init__(self, json_dict: dict):
        self.json_dict = json_dict
        self.tables = None
        self.db_name = None

    def table_name

