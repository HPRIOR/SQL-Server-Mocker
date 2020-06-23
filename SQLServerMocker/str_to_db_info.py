def table_strings(inp: str) -> [str]:
    return [s for s in inp.split("\n")]


def table_dict(t_str: str) -> dict:
    return {t_str.split(" ")[0].strip(): [s.strip() for s in t_str[t_str.find("(") + 1: t_str[1].find(")")].split(", ")]}

def table_list(dicts: [dict]) -> list:



t_str = table_strings("LOCATION (LOC_ID, LOC_NAME, LOC_CITY)"
                      "\nCAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)"
                      "\nCUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)"
                      "\nCAR_HIRE (HIRE_ID, CAR_ID, CUST_ID, START_DATE, START_MILEAGE, END_DATE, END_MILEAGE)")

print(table_dict(t_str[0]))
