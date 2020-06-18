import json


def get_json(json_file) -> dict:
    with open(json_file) as tables:
        return json.load(tables)


d = get_json("..\json_tables\\test_table.json")


# print(d)

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
    def __init__(self, table_name: str, columns: [Column]):
        self.table_name = table_name
        self.columns = columns


class DataBase:
    def __init__(self, db_name: str, tables: [Table]):
        self.db_name = db_name
        self.tables = tables


class GetDataBase:
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary
        self.db = self.get_db()

    def get_columns(self, columns: [dict]) -> [Column]:
        return [Column(column['name'], column['primary_key'], column['foreign_key'], column['not_null'],
                       column['data_type']) for column in columns]

    def get_tables(self) -> [Table]:
        return [Table([val for val in table][0], self.get_columns(table['columns']))
                for table in self.dictionary[self.get_db_name()]]

    def get_db(self) -> DataBase:
        return DataBase(self.get_db_name(), self.get_tables())

    def get_db_name(self) -> str:
        return [(key, value) for key, value in self.dictionary.items()][0][0]


db = GetDataBase(d)

print(db)
