import os
import sqlite3

class DBClient:
    
    def __init__(self):
        SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')
        self.DBConnect = sqlite3.connect(SQLfilename)
        
    def __del__(self):
        self.DBConnect.close()
        
    def Get_DiskDatabase2(self, SearchMethod: str):
        # cursor = database.cursor()
        print(type(SearchMethod))
        if(SearchMethod == 'Full'):
            for row in self.DBConnect.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
            # Query = database.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC")
        elif(SearchMethod == 'Hosts'):
            for row in self.DBConnect.execute("SELECT ID, DateEntryAdded, Hostname, HealthStatus FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
        else:
            Query = self.DBConnect.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC")
            return(Query)
        
    