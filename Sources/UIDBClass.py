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
        self.cursor.execute("SELECT Hostname FROM HostIDList")
        return(self.cursor.fetchall())
    
    def Get_DiskLogs(self, hostname: str, QueryList: tuple) -> str:
        hostID = self.Get_HostID(hostname)
        # QueryReturn = self.DBConnection.execute("SELECT * FROM HostDisks WHERE HostID=?", [hostID])
        print(type(QueryList))
        print(QueryList)
        # data = [QueryList, hostID]
        # print(data)
        # QueryReturn2 = self.DBConnection.execute("SELECT ? FROM HostDisks WHERE HostID=1", [QueryList])
        # for f in QueryReturn2:
        #     print(f)
            
        # sql = 'SELECT (%s) FROM HostDisks' % ', '.join('?' for a in QueryList)
        # self.cursor.execute(sql, QueryList)
        
        str1 = "SELECT "
        for fieldname in QueryList:
            str1 = str1 + fieldname + ", "

        select_query_string = str1[0:-2] + " from " +'HostDisk'
        query=(select_query_string)
        
        
        # return(QueryReturn.fetchall())
    
    def Get_TableHeaders(self, TableName):
        # test = self.cursor.execute("SELECT sql FROM sqlite_master WHERE name=?", [TableName])
        test = self.cursor.execute(f"SELECT * FROM {TableName}")
        # return(test.fetchall())
        HeaderList = []
        for row in test.description:
            HeaderList.append(row[0])
        return(HeaderList)
            
        
        
        
def main():
    Client = UIDBClient()
    test = ['Hostname', 'HostID', 'DriveID', 'Name', 'HealthStatus']
    test = (tuple(test))
    Client.Get_DiskLogs("sanesx01", test)
    


if __name__ == "__main__":
    main()