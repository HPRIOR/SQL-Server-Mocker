import pytest
import SQLServerMocker.mock_tables as mock_tables

def test_convert_data_type():
    c = mock_tables.Column("test", True, False, False, "int")
    assert c.convert_data_type() == "INT"
    c = mock_tables.Column("test", True, False, False, "random")
    assert c.convert_data_type() == "VARCHAR(100)"
