import pytest
from SQLServerMocker.str_to_db_info import *

s = "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)" \
    "\nCAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)" \
    "\nCUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)" \
    "\nCAR_HIRE (HIRE_ID, CAR_ID, CUST_ID, START_DATE, START_MILEAGE, END_DATE, END_MILEAGE)"


def test_table_strings():
    assert table_strings(s) == \
           [
               "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)",
               "CAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)",
               "CUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)",
               "CAR_HIRE (HIRE_ID, CAR_ID, CUST_ID, START_DATE, START_MILEAGE, END_DATE, END_MILEAGE)"
           ]


def test_table_dict():
    assert table_dict(table_strings(s)[0]) == {"LOCATION": ["LOC_ID", "LOC_NAME", "LOC_CITY"]}


def test_table_list():
    assert table_list(s) == [{"LOCATION": ["LOC_ID", "LOC_NAME", "LOC_CITY"]},
                             {"CAR": ["CAR_ID", "CAR_CATEGORY", "CAR_MAKE", "CAR_MODEL", "LOC_ID"]},
                             {"CUSTOMER": ["CUST_ID", "CUST_NAME", "CUST_CONTACT_NO"]},
                             {"CAR_HIRE": ["HIRE_ID", "CAR_ID", "CUST_ID", "START_DATE", "START_MILEAGE", "END_DATE",
                                           "END_MILEAGE"]}]
