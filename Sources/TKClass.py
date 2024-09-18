import tkinter as tk
from tkinter import ttk

class TKClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Redfish-Server-Toolkit")
        self.geometry('750x600')
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        frame = InputForm(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        frame2 = InputForm(self)
        frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
class InputForm(ttk.Frame):
    def __init__(self, parent):
            super().__init__(parent)
            self.entry_field = ttk.Entry(self)
            self.entry_field.grid(row=0, column=0, sticky="ew")
            self.entry_field.bind("<Return>", self.add_to_list)
            
            self.entry_button = ttk.Button(self, text="Add", command=self.add_to_list)
            self.entry_button.grid(row=0,column=1)
            
            self.text_list = tk.Listbox(self)
            self.text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
            
    def add_to_list(self, event=None):
        text = self.entry_field.get()
        if text:
            self.text_list.insert(tk.END, text)
            self.entry_field.delete(0, tk.END)
            
class ListHosts(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            
            