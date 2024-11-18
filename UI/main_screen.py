import pdb
import sys
import time
import tkinter as tk
import pandas as pd
from tkinter import HORIZONTAL
from tkinter.ttk import *
import threading
from tkinter import messagebox as msgbox

from master.node import ScraperHTML
from structure.locator_factory import CreateLocator


class FinderMainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Finder 1.0')
        self.geometry('350x320')
        self.optional_state = 'active'
        self.second_root = None
        self.resizable(False, False)
        self.start_button = tk.Button(self, text='START', command=self.start_scraping)
        self.start_button.place(x=140, y=220)

        # URL label
        self.url_label = tk.Label(self, text="URL : ")
        self.url_label.place(x=25, y=120)

        # header
        self.finder_header = tk.Label(self, text="Instantly extract all HTML locators with real-time speed "
                                                 "insights to boost your web automation efficiency", wraplength=300)
        self.finder_header.place(x=25, y=50)

        # URL Input Box
        value = tk.StringVar(self, value="https://www.mit.edu/")
        self.url_input_box = tk.Entry(self, width=25, borderwidth=2, textvariable=value)
        self.url_input_box.place(x=75, y=120)

    def display_tree(self, data_set):
        if isinstance(data_set, list) and len(data_set) != 0:
            df = pd.DataFrame(data_set).dropna(how='all')
            df = df.map(lambda x: ', '.join(x) if isinstance(x, list) else x)
            self.second_root = tk.Toplevel(self)
            self.second_root.overrideredirect(False)
            self.second_root.title("Locator Results")
            self.second_root.geometry("600x400")
            tree = Treeview(self.second_root, columns=list(df.columns), show="headings")
            for column in df.columns:
                tree.heading(column, text=column)
                tree.column(column, width=250)
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))
            tree.pack(expand=True, fill="both")
        else:
            msgbox.showerror(title="DataSetWindow", message="No Data Set Found")
            self.start_button.config(state="active")
            self.url_input_box.config(state="normal")

    def progress_window(self):
        # Create one more window for progress
        sh = ScraperHTML(url=self.url_input_box.get())
        self.start_button.config(state="disabled")
        self.url_input_box.config(state="disabled")
        first_label = tk.Label(self, text="Initiating the session")
        first_label.place(x=100, y=250)
        print("Preparing the session")
        response = sh.get_session()
        if response is not None:
            first_label.destroy()
        else:
            msgbox.showerror(title="Error", message="Unable to create session, retry after sometime.")
            sys.exit(1)
        sh.render_response(response, self)
        sh.parser_html(response, self)
        dataset = sh.find_key_value_pair(self)
        locators = CreateLocator(dataset).mapper()
        self.display_tree(locators)

    def start_scraping(self):
        thread = threading.Thread(target=self.progress_window)
        thread.start()


if __name__ == '__main__':
    obj = FinderMainScreen()
    obj.mainloop()
