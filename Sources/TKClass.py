from Sources.UIDBClass import *
import tkinter as tk
from tkinter import ttk

# from tkinter import *
from tkinter import filedialog


class TKClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Redfish-Server-Toolkit")
        self.geometry("850x600")
        self.config(background="grey")
        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.rowconfigure(1, weight=1)

        menu_bar = ttk.Frame(self)
        menu_bar.grid(row=0, column=0, sticky="ew")
        menu_bar.columnconfigure(0, weight=2)
        menu_bar.columnconfigure(1, weight=1)
        home_button = ttk.Button(
            menu_bar, text="Home", command=lambda: self.show_frame()
        )
        host_button = ttk.Button(
            menu_bar, text="Hosts", command=lambda: self.show_frame(ListHostsFrame)
        )
        first_button = ttk.Button(
            menu_bar, text="Disk Logs", command=lambda: self.show_frame(DiskSearchFrame)
        )
        options_button = ttk.Button(
            menu_bar, text="Options", command=lambda: self.show_frame(OptionsFrame)
        )
        home_button.grid(row=0, column=2)
        host_button.grid(row=0, column=3)
        first_button.grid(row=0, column=4)
        options_button.grid(row=0, column=5)

        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (ListHostsFrame, DiskSearchFrame, OptionsFrame):
            frame = F(
                container
            )
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ListHostsFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class DiskSearchFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        DBQuery = UIDBClient()
        log_frame = ttk.Frame(self)
        log_frame.grid(row=2, column=0, sticky="ew")

        host_options = DBQuery.Get_HostsList()
        host_options.insert(0, "Select Host")
        defaultoption = tk.StringVar()
        host_dropdown = ttk.OptionMenu(self, defaultoption, *host_options)
        host_dropdown.grid(row=0, column=0, sticky="ew")

        # Button used to initialize search.
        search_button = ttk.Button(
            self,
            text="Search Logs",
            command=lambda: self.GetTKDiskLogs(defaultoption.get(), log_frame)
            # command=lambda: self.DrawLogFrame(log_frame, self.Get_DiskDetails_Selection(), 'test')
        )
        search_button.grid(row=0, column=5, sticky="ew")

        # Adds the list of disk information. (Bad naming)
        self.hosts_list = tk.Listbox(self, height=20)
        self.hosts_list.grid(row=1, column=0, sticky="ew", pady=5, columnspan=2)
        self.hosts_list.insert(tk.END, "Search for hosts now")

        HeaderInfo = DBQuery.Get_TableHeaders("HostDisks")
        self.diskdetails_list = tk.Listbox(self, height=20, selectmode="multiple")
        self.diskdetails_list.grid(row=1, column=5, sticky="nsew", pady=5)
        yscrollbar = tk.Scrollbar(self)
        yscrollbar.grid(row=1, column=6, sticky="ns")
        yscrollbar.config(command=self.diskdetails_list.yview)
        for d in HeaderInfo:
            self.diskdetails_list.insert(tk.END, d)

    # WIP trying to redraw the log table depending on disk details selection.
    def DrawLogFrame(self, cont, headings):
        try:
            if 1 == (self.disk_table.winfo_exists()):
                self.disk_table.destroy()
            elif (self.disk_table.winfo_exists() == 0):
                print("No Table")
        except:
            pass
        self.disk_table = ttk.Treeview(cont, columns=headings, show='headings')
        self.disk_table.grid(row=0, column=0, sticky='ew')

        for H in headings: # Creates all the headings for the table.
            self.disk_table.heading(H, text=H)
        for D in (): # Loads table data into the treeview widget.
            pass

    def Get_DiskDetails_Selection(self):
        SelectList = []
        for index in self.diskdetails_list.curselection():
            SelectList.append(self.diskdetails_list.get(index))
        return SelectList

    def GetTKDiskLogs(self, hostname, log_frame):
        DBQuery = UIDBClient()
        # HeaderInfo = DBQuery.Get_TableHeaders("HostDisks")
        disk_data_logs = DBQuery.Get_DiskLogs(hostname)
        self.hosts_list.delete(0, tk.END)
        # self.hosts_list.insert(tk.END, HeaderInfo)
        column_selection = self.Get_DiskDetails_Selection()
        self.DrawLogFrame(log_frame, self.Get_DiskDetails_Selection())
        if disk_data_logs:
            for H in disk_data_logs:
                data = []
                for L in column_selection:
                    data.append(str(getattr(H, L)))
                self.hosts_list.insert(tk.END, ", ".join(data))
                self.disk_table.insert('', tk.END, values=data)


class OptionsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)
        path_button = ttk.Button(self, text="Select DB", command=self.file_select)
        path_button.grid(row=0, column=0, columnspan=2, sticky="ew")

        submit_button = ttk.Button(self, text="Submit", command=self.file_select)
        submit_button.grid(row=0, column=1, sticky="ew")
        # self.submit_button.columnconfigure(1)

        self.path_list = tk.Listbox(self, height=2, fg="blue", background="white")
        self.path_list.grid(row=1, column=0, columnspan=3, rowspan=1, sticky="ew")

    def file_select(self):
        my_file = filedialog.askopenfilename(
            initialdir="",
            title="Select a File",
            filetypes=(("DB files", "*.db"), ("All Files", "*.*")),
        )
        # self.my_file = "hi"
        if my_file:
            # print(self.my_file)
            self.path_list.insert(tk.END, my_file)
        else:
            pass
        


class ListHostsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)

        search_button = ttk.Button(
            self, text="Search For Hosts", command=lambda: self.GetHosts()
        )
        search_button.grid(row=0, column=0, sticky="ew")
        self.hosts_list = tk.Listbox(self, height=8)
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
