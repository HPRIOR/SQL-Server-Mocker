import pytest
from SQLServerMocker.get_database import *


def test_get_db_name():
    dictionary = get_json("..\json_tables\\test_table.json")
    db = CreateDataBase(dictionary).get_db()
    assert db.name == "test_db"


def test_table_name():
    dictionary = get_json("..\json_tables\\test_table.json")
    db = CreateDataBase(dictionary).get_db()
    assert [table.name for table in db.tables][0] == "test_table_1"
    assert [table.name for table in db.tables][1] == "test_table_2"


def test_columns():
    dictionary = get_json("..\json_tables\\test_table.json")
    db = CreateDataBase(dictionary).get_db()
    c_name = "column_"
    c_no = 1
    for table in db.tables:
        for column in table.columns:
            assert column.name == c_name + str(c_no)
            c_no += 1


def test_convert_data_type():
    c = Column("test", True, "None", False, "int")
    assert c.convert_data_type() == "INT"
    c = Column("test", True, "None", False, "random")
    assert c.convert_data_type() == "VARCHAR(100)"
