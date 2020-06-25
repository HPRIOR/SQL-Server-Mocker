import tkinter as tk
from SQLServerMocker.str_to_db_info import DKMString
from SQLServerMocker.generators import get_gen_dict
from SQLServerMocker.get_database import CreateDataBase
from SQLServerMocker.create_tables import CreateTable
from SQLServerMocker.populate_tables import PopulateTables


def get_str_var_dict(tuple_list: list):
    """argument = [(table, [columns]),...]
    returns: dict: {table} -> {column} -> {pk, fk, type}"""
    table_dict = {}
    for tup in tuple_list:
        column_dict = {}
        for col in tup[1]:
            column_dict[col] = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
            column_dict[col][0].set("False")
            column_dict[col][1].set("None")
            column_dict[col][2].set("string")
        table_dict[tup[0]] = column_dict
    return table_dict


class ApplicationMemory:
    app_mem: dict = {
        "init_string": None,
        "db_name": None,
        "string_var_dict": None,
        "table_rows": None,
        "gen_dict": get_gen_dict(),
        "table_names": None,

    }


class MainController(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("SQL server mocker")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.app_mem = ApplicationMemory.app_mem
        self.app_mem["gen_dict_keys"] = [key for key, value in self.app_mem["gen_dict"].items()]
        self.app_mem["db_name"] = tk.StringVar()

        self.frames = {
            StartFrame.__name__: StartFrame(
                parent=self.main_frame,
                main_controller=self,
                start_p_controller=StartPageController(),
            ),
            DualScreenFrame.__name__: DualScreenFrame(
                parent=self.main_frame,
                controller=self
            ),
        }

        self.frames[DbFrame.__name__] = DbFrame(
            parent=self.frames["DualScreenFrame"],
            controller=self
        )
        self.frames[DisplayFrame.__name__] = DisplayFrame(
            parent=self.frames["DualScreenFrame"],
            controller=self,
            text="Text will be displayed here"
        )
        self.frames[EnterBackButtonFrame.__name__] = EnterBackButtonFrame(
            parent=self.frames["DualScreenFrame"],
            controller=DisplayController(self.app_mem, self)
        )

        self.show_frame("StartFrame")

    def show_frame(self, key):
        frame = self.frames[key]
        frame.tkraise()


class StartPageController:
    def process_start_frame_input(self, main_controller, content_entry):
        try:
            table_tup_list = DKMString(content_entry.get(1.0, "end").strip('\n')).table_list()
            main_controller.app_mem["string_var_dict"] = get_str_var_dict(table_tup_list)
            main_controller.app_mem["table_names"] = [key for key, value in
                                                      main_controller.app_mem["string_var_dict"].items()]
            main_controller.app_mem["table_names"].append("None")
            main_controller.app_mem["table_rows"] = [tk.StringVar() for table in main_controller.app_mem["table_names"] if table != "None"]
            for string_var in main_controller.app_mem["table_rows"]:
                string_var.set("10")
            self.create_table_frames(table_tup_list, main_controller)
            main_controller.show_frame("DualScreenFrame")

        except IndexError:
            pass
            # show error message

    def create_table_frames(self, tables, controller):
        row = 1
        pad = 5
        for table, columns in tables:
            controller.frames[table] = TableFrame(controller.frames["DbFrame"], controller, table)

            pk_label = tk.Label(controller.frames[table], text="Primary Key")
            fk_label = tk.Label(controller.frames[table], text="Foreign Key Table")
            type_label = tk.Label(controller.frames[table], text="Data Type")

            pk_label.grid(row=row, column=2, pady=pad)
            fk_label.grid(row=row, column=3, pady=pad)
            type_label.grid(row=row, column=4, pady=pad)

            row = self.create_column_frames(columns, controller, row, table)

    def create_column_frames(self, columns, controller, row, table):
        for col in columns:
            controller.frames[col] = [
                ColumnLabelFrame(
                    parent=controller.frames[table],
                    controller=controller,
                    row=row,
                    column=1,
                    label=col
                ),
                ColumnPkOptionFrame(
                    parent=controller.frames[table],
                    controller=controller,
                    row=row,
                    column=2,
                    string_var=controller.app_mem["string_var_dict"][table][col][0]
                ),
                ColumnFkOptionFrame(
                    parent=controller.frames[table],
                    controller=controller,
                    row=row,
                    column=3,
                    string_var=controller.app_mem["string_var_dict"][table][col][1]
                ),
                ColumnTypeOptionFrame(
                    parent=controller.frames[table],
                    controller=controller,
                    row=row,
                    column=4,
                    string_var=controller.app_mem["string_var_dict"][table][col][2]
                )
            ]
            row += 1
        return row


class CreateDBDict:
    def __init__(self, app_mem: dict):
        self.app_mem = app_mem

    def create_db_dict(self):
        main_dict = {
            "db_name": self.app_mem["db_name"].get(),
            "tables": self.create_table_dicts(),
        }
        return main_dict

    def create_table_dicts(self) -> [dict]:
        d = []
        for enum, (key_table, column_dict) in enumerate(self.app_mem["string_var_dict"].items()):
            d.append({
                "table_name": key_table,
                "columns": self.create_column_dicts(column_dict),
                "rows": int(self.app_mem["table_rows"][enum].get())
            })
        return d

    def create_column_dicts(self, columns: dict) -> [dict]:
        d = []
        for col_name, string_vars in columns.items():
            d.append({
                "name": col_name,
                "primary_key": string_vars[0].get() == "True",
                "foreign_key": string_vars[1].get(),
                "data_type": string_vars[2].get(),
                "not_null" : True
            })
            print(bool(string_vars[0].get()))
        return d




class DisplayController:
    def __init__(self, app_mem: dict, main_controller):
        self.app_mem = app_mem
        self.main_controller = main_controller

    def display_text(self):
        db_dict = CreateDBDict(self.app_mem).create_db_dict()
        db = CreateDataBase(db_dict).get_db()
        display_text = CreateTable(db).string_builder() + PopulateTables(db).string_builder()
        DisplayFrame(self.main_controller.frames["DualScreenFrame"], MainController, display_text)


class DualScreenFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=0, sticky="nsew")


class StartFrame(tk.Frame):
    def __init__(self, parent, main_controller, start_p_controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")

        label = tk.Label(self,
                         text="Enter a database schema. "
                              "For example:\n \n"
                              "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)\n"
                              "CAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)\n"
                              "CUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)")
        content_entry = tk.Text(self, textvariable=main_controller.app_mem["init_string"])
        enter_str_button = tk.Button(self, text="Enter",
                                     command=lambda: start_p_controller.process_start_frame_input(main_controller,
                                                                                                  content_entry))

        label.pack(pady=10, padx=10)
        content_entry.pack(expand=True, fill="both")
        enter_str_button.pack()


class ColumnFrame(tk.Frame):
    """Column frames inherit from this: use to change grid parameters"""

    def __init__(self, parent, controller, row, column):
        tk.Frame.__init__(self, parent)
        self.grid(row=row + 2, column=column, sticky='nesw')


class ColumnLabelFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, label):
        ColumnFrame.__init__(self, parent, controller, row, column)
        self.column_label = tk.Label(self, text=label + ": ")
        self.column_label.pack()


class ColumnPkOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        pk_option = tk.OptionMenu(self, string_var, "False", "True")
        pk_option.pack()


class ColumnFkOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        fk_option = tk.OptionMenu(self, string_var, *controller.app_mem["table_names"])
        fk_option.pack()


class ColumnTypeOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        fk_option = tk.OptionMenu(self, string_var, *controller.app_mem["gen_dict_keys"])
        fk_option.pack()


class TableFrame(tk.Frame):
    row = 1

    def __init__(self, parent, controller, label):
        tk.Frame.__init__(self, parent)
        self.grid(row=self.row, column=0, sticky="nsew", pady=10, padx=20)

        row_num_imp = tk.Entry(self, textvariable=controller.app_mem["table_rows"][TableFrame.row-1])
        num_row_label = tk.Label(self, text="number of rows: ")
        table_label = tk.Label(self, text=label)

        row_num_imp.grid(column=4, row=0, sticky='e')
        num_row_label.grid(column=3, row=0)
        table_label.grid(column=0, row=0)

        TableFrame.row += 1


class DbFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=0, sticky="nsew")

        input_frame = tk.Frame(self)
        db_name_inp = tk.Entry(input_frame, textvariable=controller.app_mem["db_name"])
        db_name_label = tk.Label(input_frame, text="Database name: ")

        input_frame.grid(row=0, column=0)
        db_name_inp.grid(column=1, row=0)
        db_name_label.grid(column=0, row=0)



class DisplayFrame(tk.Frame):
    def __init__(self, parent, controller, text):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=1, sticky="nsew")
        label = tk.Label(self, text=text)
        label.grid(row=5)


class EnterBackButtonFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=1, column=0)

        self.enter = tk.Button(self, text="Enter", command=lambda: controller.display_text())
        self.enter.grid(row=0, column=2)


app = MainController()
app.mainloop()
