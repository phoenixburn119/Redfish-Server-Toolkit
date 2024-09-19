import os
import sqlite3

class UIDBClient:
    DBConnection = None
    def __init__(self):
        SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')
        self.DBConnection = sqlite3.connect(SQLfilename)
        self.cursor = self.DBConnection.cursor()

    def __del__(self):
        self.DBConnection.close()
        
    # Returns the foreign key ID for the hostname from the HostIDList table.
    def Get_HostID(self, Hostname: str) -> str:
        self.cursor.execute("SELECT ID FROM HostIDList WHERE Hostname=?", [Hostname])
        HostIDReturn = self.cursor.fetchone()
        return(HostIDReturn[0])
    
    def Get_HostsList(self) -> str:
        # for row in self.DBConnection.execute("SELECT * FROM HostIDList"):
        #     print(row)
            
        self.cursor.execute("SELECT Hostname FROM HostIDList")
        return(self.cursor.fetchall())