import tkinter as tk

class TKClient:
    tk_root = None
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.title("Redfish-Server-Toolkit")
        self.tk_root.frame()
        self.MainFrames()

    def __del__(self):
        pass

    def MainFrames(self):
        self.frame_main = tk.Frame(self.tk_root)
        
        self.frame_host = tk.Frame(self.tk_root)
        self.frame_host.columnconfigure(0, weight=1)
        self.frame_host.grid(row=0,column=0, sticky="ew")
        self.Host_Frame()
        
        self.frame_query = tk.Frame(self.tk_root)
        
    def test(self):
        pass
    
    def Host_Frame(self):
        submit_button = tk.Button(self.frame_host, text="Submit")
        submit_button.grid(row=0,column=0)
