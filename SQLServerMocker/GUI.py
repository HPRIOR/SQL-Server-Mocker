import tkinter as tk
from SQLServerMocker.str_to_db_info import DKMString
from SQLServerMocker.generators import get_gen_dict


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


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("SQL server mocker")
        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.app_mem = ApplicationMemory()

        self.frames = {StartPage.__name__: StartPage(main_frame, self), DbFrame.__name__: DbFrame(main_frame, self)}

        self.show_frame("StartPage")

    def show_frame(self, key):
        frame = self.frames[key]
        frame.tkraise()


class ApplicationMemory:
    def __init__(self):
        self.init_string = None
        self.string_var_dict = None
        self.table_rows = None
        self.gen_dict = get_gen_dict()
        self.dict_key_list = [key for key, value in self.gen_dict.items()]


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")
        label = tk.Label(self,
                         text="Enter a database schema. "
                              "For example:\n \n"
                              "LOCATION (LOC_ID, LOC_NAME, LOC_CITY)\n"
                              "CAR (CAR_ID, CAR_CATEGORY, CAR_MAKE, CAR_MODEL, LOC_ID)\n"
                              "CUSTOMER (CUST_ID, CUST_NAME, CUST_CONTACT_NO)")
        label.pack(pady=10, padx=10)
        self.content_entry = tk.Text(self, textvariable=controller.app_mem.init_string)
        self.content_entry.pack(expand=True, fill="both")
        enter_str_button = tk.Button(self, text="Enter", command=lambda: self.process_content(controller))
        enter_str_button.pack()

    def process_content(self, controller):
        try:
            table_tup_list = DKMString(self.content_entry.get(1.0, "end").strip('\n')).table_list()
            controller.app_mem.string_var_dict = get_str_var_dict(table_tup_list)
            self.create_table_frames(table_tup_list, controller)
            controller.show_frame("DbFrame")
        except(IndexError):
            pass
            # show error message

    def create_table_frames(self, tables, controller):
        for table, columns in tables:
            controller.frames[table] = TableFrame(controller.frames["DbFrame"], controller)
            for col in columns:
                controller.frames[col] = ColumnFrame(controller.frames[table], controller, col)


class ColumnFrame(tk.Frame):
    row = 0

    def __init__(self, parent, controller, label):
        tk.Frame.__init__(self, parent)
        self.grid(row=self.row, column=0, sticky="nsew")
        ColumnFrame.row += 1
        self.label = label


class TableFrame(tk.Frame):
    row = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=self.row, column=0, sticky="nsew")
        TableFrame.row += 1


class DbFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")


app = Controller()
app.mainloop()
