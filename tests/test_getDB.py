import pytest

from SQLServerMocker.get_database import *


def test_get_db_name():
    dictionary = get_json("..\json_tables\\test_table.json")
    print(dictionary)
    db = CreateDataBase(dictionary)
    assert db.get_db_name() == "db_name"
