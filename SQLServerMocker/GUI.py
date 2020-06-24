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

        self.frames = {
            StartPage.__name__: StartPage(main_frame, self),
            DualScreenFrame.__name__: DualScreenFrame(main_frame, self),
        }
        self.frames[DbFrame.__name__] = DbFrame(self.frames["DualScreenFrame"], self)
        self.frames[DisplayFrame.__name__] = DisplayFrame(self.frames["DualScreenFrame"], self),

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
        self.table_names = None
        self.gen_dict_key_list = [key for key, value in self.gen_dict.items()]


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
            controller.app_mem.table_names = [key for key, value in controller.app_mem.string_var_dict.items()]
            self.create_table_frames(table_tup_list, controller)
            controller.show_frame("DualScreenFrame")
        except(IndexError):
            pass
            # show error message

    def create_table_frames(self, tables, controller):
        row = 1
        for table, columns in tables:
            controller.frames[table] = TableFrame(controller.frames["DbFrame"], controller, table)
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
                        string_var=controller.app_mem.string_var_dict[table][col][0]
                    ),
                    ColumnFkOptionFrame(
                        parent=controller.frames[table],
                        controller=controller,
                        row=row,
                        column=3,
                        string_var=controller.app_mem.string_var_dict[table][col][1]
                    ),
                    ColumnTypeOptionFrame(
                        parent=controller.frames[table],
                        controller=controller,
                        row=row,
                        column=4,
                        string_var=controller.app_mem.string_var_dict[table][col][2]
                    )
                ]
                row += 1


class ColumnFrame(tk.Frame):
    """Column frames inherit from this: use to change grid parameters"""

    def __init__(self, parent, controller, row, column):
        tk.Frame.__init__(self, parent)
        self.grid(row=row, column=column, sticky='nesw')


class ColumnLabelFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, label):
        ColumnFrame.__init__(self, parent, controller, row, column)
        self.column_label = tk.Label(self, text=label + ": ")
        self.column_label.pack()


class ColumnPkOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        pk_option = tk.OptionMenu(self, string_var, "True", "False")
        pk_option.pack()


class ColumnFkOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        fk_option = tk.OptionMenu(self, string_var, *controller.app_mem.table_names)
        fk_option.pack()


class ColumnTypeOptionFrame(ColumnFrame):
    def __init__(self, parent, controller, row, column, string_var):
        ColumnFrame.__init__(self, parent, controller, row, column)
        fk_option = tk.OptionMenu(self, string_var, *controller.app_mem.gen_dict_key_list)
        fk_option.pack()


class TableFrame(tk.Frame):
    row = 0

    def __init__(self, parent, controller, label):
        tk.Frame.__init__(self, parent)
        self.grid(row=self.row, column=0, sticky="nsew", pady=10, padx=20)
        TableFrame.row += 1
        lb = tk.Label(self, text=label)
        lb.grid(column=0, row=0)


class DbFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=0, sticky="nsew")


class DisplayFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=1, sticky="nsew")


class DualScreenFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="grey")
        self.grid(row=0, column=0, sticky="nsew")

    def display_text(self, text):
        label = tk.Label(self, text=text)
        label.pack()


app = Controller()
app.mainloop()
