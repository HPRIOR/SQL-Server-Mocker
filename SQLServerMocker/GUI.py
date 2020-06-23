import tkinter as tk


def create_2D_dict(self, l: list):
    """argument = [(table, [columns]),...]
    returns: dict: {table} -> {column} -> {pk, fk, type}"""
    table_dict = {}
    for tup in l:
        column_dict = {}
        for col in tup[1]:
            column_dict[col] = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
            column_dict[col][0].set("False")
            column_dict[col][1].set("None")
            column_dict[col][2].set("string")
        table_dict[tup[0]] = column_dict


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
        self.string_var_dict = {}


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
        controller.app_mem.init_string = self.content_entry.get(1.0, "end")
        print(controller.app_mem.init_string)
        # this will create a frame based on input and add it to the frame dictionary
        # and also make the controller call this frame


class ColumnFrame(tk.Frame):
    column = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=self.column, sticky="nsew")
        self.column += 1


class TableFrame(tk.Frame):
    column = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=self.column, sticky="nsew")
        self.column += 1

class DbFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="nsew")



app = Controller()
app.mainloop()
