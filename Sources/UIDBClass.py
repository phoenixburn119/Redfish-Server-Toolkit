import os
import sqlite3
from dataclasses import dataclass

@dataclass
class HostDisk():
    id: int
    DateEntryAdded: str
    Hostname: str
    HostID: str
    DriveID: str
    Name: str
    HealthStatus: str
    StatusIndicator: str
    BlockSizeBytes: str
    CapableSpeedGbs: str
    NegotiatedSpeedGbs: str
    FailurePredicted: str
    HostspareType: str
    MediaType: str
    Model: str
    Location: str
    PredictedMediaLifeLeftPercent: str
    Protocol: str
    Revision: str
    SerialNumber: str
    WriteCacheEnabled: str

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
    
    def Get_DiskLogs(self, hostname: str) -> list[HostDisk]:
        hostID = self.Get_HostID(hostname)
        query_return = self.DBConnection.execute("SELECT * FROM HostDisks WHERE HostID=?", [hostID])
        hosts = []
        for host in query_return:
            h = HostDisk(host[0], host[1], host[2], host[3], host[4], host[5], host[6],
                         host[7], host[8], host[9], host[10], host[11], host[12], host[13],
                         host[14], host[15], host[16], host[17], host[18], host[19], host[20])
            hosts.append(h)
        return hosts

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