import tkinter as tk

class TKClient:
    tk_root = None
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.title("Redfish-Server-Toolkit")

    def __del__(self):
        pass

