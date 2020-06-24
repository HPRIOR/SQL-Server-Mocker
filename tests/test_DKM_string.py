import pytest
from SQLServerMocker.str_to_db_info import *

s = "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)" \
    "\nCAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)" \
    "\nCUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)" \
    "\nCAR_HIRE (HIRE_ID, CAR_ID, CUST_ID, START_DATE, START_MILEAGE, END_DATE, END_MILEAGE)"

dkm_str = DKMString(s)


def test_table_strings():
    assert dkm_str.table_strings(s) == \
           [
               "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)",
               "CAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)",
               "CUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)",
               "CAR_HIRE (HIRE_ID, CAR_ID, CUST_ID, START_DATE, START_MILEAGE, END_DATE, END_MILEAGE)"
           ]


def test_table_dict():
    assert dkm_str.table_dict(dkm_str.table_strings(s)[0]) == ("LOCATION", ["LOC_ID", "LOC_NAME", "LOC_CITY"])


def test_table_list():
    assert dkm_str.table_list() == [("LOCATION", ["LOC_ID", "LOC_NAME", "LOC_CITY"]),
                                    ("CAR", ["CAR_ID", "CAR_CATEGORY", "CAR_MAKE", "CAR_MODEL", "LOC_ID"]),
                                    ("CUSTOMER", ["CUST_ID", "CUST_NAME", "CUST_CONTACT_NO"]),
                                    ("CAR_HIRE",
                                     ["HIRE_ID", "CAR_ID", "CUST_ID", "START_DATE", "START_MILEAGE", "END_DATE",
                                      "END_MILEAGE"])]


def test_main():
    test_table_dict()
    test_table_strings()
    test_table_list()
