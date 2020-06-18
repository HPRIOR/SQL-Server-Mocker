from SQLServerMocker.get_database import *
from SQLServerMocker.create_tables import *

db = CreateDataBase(get_json("..\json_tables\\test_table.json")).get_db()
db_reverse = CreateDataBase(get_json("..\json_tables\\test_table_reverse.json")).get_db()


def test_initial_string():
    assert CreateTable(db).initial_string(db.tables[0]) == "CREATE TABLE test_db.dbo.test_table_1 (\n"
    assert CreateTable(db).initial_string(db.tables[1]) == "CREATE TABLE test_db.dbo.test_table_2 (\n"


def test_column_string():
    assert CreateTable(db).column_string(db.tables[0]) \
           == "column_1 VARCHAR(100),\ncolumn_2 INT,\ncolumn_3 VARCHAR(100) NOT NULL,\n"
    assert CreateTable(db).column_string(db.tables[1]) \
           == "column_4 VARCHAR(100),\ncolumn_5 VARCHAR(100),\ncolumn_6 VARCHAR(100),\n"


def test_constraint_string():
    assert CreateTable(db).constraint_string(db.tables[1]) \
           == "FOREIGN KEY (column_4) REFERENCES test_db.dbo.test_table_1 (column_4),\n"

def test_primary_key_string():
    assert CreateTable(db).primary_key_string(db.tables[0]) \
           == "PRIMARY KEY (column_1)"
    assert CreateTable(db).primary_key_string(db.tables[1]) \
           == "PRIMARY KEY (column_4, column_5)"


def test_string_builder():
    assert CreateTable(db).string_builder() \
           == "CREATE TABLE test_db.dbo.test_table_1 (\ncolumn_1 VARCHAR(100),\ncolumn_2 INT," \
              "\ncolumn_3 VARCHAR(100) NOT NULL,\nPRIMARY KEY (column_1)\n);\n \nCREATE TABLE " \
              "test_db.dbo.test_table_2 (\ncolumn_4 VARCHAR(100),\ncolumn_5 VARCHAR(100),\ncolumn_6 " \
              "VARCHAR(100),\nFOREIGN KEY (column_4) REFERENCES test_db.dbo.test_table_1 (column_4)," \
              "\nPRIMARY KEY (column_4, column_5)\n);\n"














