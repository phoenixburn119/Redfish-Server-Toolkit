from Sources.UIDBClass import *
import tkinter as tk
from tkinter import ttk
# from tkinter import *
from tkinter import filedialog


class TKClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Redfish-Server-Toolkit")
        self.geometry('750x600')
        self.config(background = "grey")
        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.rowconfigure(1, weight=1)
        
        menu_bar = ttk.Frame(self)
        menu_bar.grid(row=0, column=0, sticky="ew")
        menu_bar.columnconfigure(0, weight=2)
        menu_bar.columnconfigure(1, weight=1)
        home_button = ttk.Button(menu_bar, text="Home", command=lambda : self.show_frame())
        host_button = ttk.Button(menu_bar, text="Hosts", command=lambda : self.show_frame(ListHostsFrame))
        first_button = ttk.Button(menu_bar, text="Input Form", command=lambda : self.show_frame(InputForm))
        options_button = ttk.Button(menu_bar, text="Options", command=lambda : self.show_frame(OptionsFrame))
        home_button.grid(row=0, column=2)
        host_button.grid(row=0, column=3)
        first_button.grid(row=0, column=4)
        options_button.grid(row=0, column=5)
        
        
        container = ttk.Frame(self)  
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}
  
        for F in (ListHostsFrame, InputForm, OptionsFrame):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(ListHostsFrame)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() 
        
class InputForm(ttk.Frame):
    def __init__(self, parent, controller):
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

class OptionsFrame(ttk.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.columnconfigure(0, weight=1)
            # self.rowconfigure(0, weight=1)
            path_button = ttk.Button(self, text="Select DB", command=self.file_select)
            path_button.grid(row=0, column=0, columnspan=2, sticky="ew")
            
            submit_button = ttk.Button(self, text="Submit", command=self.file_select)
            submit_button.grid(row=0, column=1, sticky="ew")
            # self.submit_button.columnconfigure(1)
            
            self.path_list = tk.Listbox(self, height= 2, fg="blue", background="white")
            self.path_list.grid(row=1, column=0, columnspan=3, rowspan=1, sticky="ew")
            
    
        def file_select(self):
            my_file = filedialog.askopenfilename(initialdir="",
                title="Select a File",
                filetypes=(("DB files", "*.db"),("All Files", "*.*")))
            # self.my_file = "hi"
            if my_file:
                # print(self.my_file)
                self.path_list.insert(tk.END, my_file)
            else:
                pass
            
class ListHostsFrame(ttk.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.columnconfigure(0, weight=1)
            
            search_button = ttk.Button(self, text="Search For Hosts", command=lambda : self.GetHosts())
            search_button.grid(row=0, column=0, sticky="ew")
            self.hosts_list = tk.Listbox(self, height=2)
            self.hosts_list.grid(row=1, column=0, sticky="ew")
            self.hosts_list.insert(tk.END, "Search for hosts now")

            
            
        def GetHosts(self):
            DBQuery = UIDBClient()
            Hosts = DBQuery.Get_HostsList()
            self.hosts_list.delete(0, tk.END)
            print(Hosts)
            if Hosts:
                for H in Hosts:
                    self.hosts_list.insert(tk.END, H)
                    pass
            
            