import pytest
from SQLServerMocker.get_database import *


def test_convert_data_type():
    c = Column("test", True, False, False, "int")
    assert c.convert_data_type() == "INT"
    c = Column("test", True, False, False, "random")
    assert c.convert_data_type() == "VARCHAR(100)"
