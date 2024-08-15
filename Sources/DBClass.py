import os
import sqlite3

class DBClient:
    DBConnection = None
    def __init__(self):
        SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')
        self.DBConnection = sqlite3.connect(SQLfilename)
        self.cursor = self.DBConnection.cursor()

    def __del__(self):
        self.DBConnection.close()

    def Create_Database_Tables(self):
        if not(os.path.isfile(os.path.join((os.path.dirname(__file__)), 'RedDataBase.db'))):
            self.cursor.execute("CREATE TABLE IF NOT EXISTS HostDisks (id integer primary key, DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors)")
            # cur.execute("CREATE TABLE IF NOT EXISTS HostData (id integer primary key, Date Entry Added, )")
            self.DBConnection.commit()
            return("Creating Database")
        else:
            return("Database Already Exists")

    def Write_DiskDatabase(self, DiskData: dict, Hostname: str):
        InsertData = (Hostname, (DiskData['Id']), (DiskData['SerialNumber']), (DiskData['Model']), (DiskData['Status']['Health']), (DiskData['CapacityGB']), (DiskData['CurrentTemperatureCelsius']), (DiskData['MaximumTemperatureCelsius']), (DiskData['Description']), (''.join(str(x) for x in DiskData['DiskDriveStatusReasons'])), (DiskData['FirmwareVersion']['Current']['VersionString']), (DiskData['InterfaceSpeedMbps']), (DiskData['InterfaceType']), (DiskData['Location']), (DiskData['MediaType']), (DiskData['PowerOnHours']), (DiskData['RotationalSpeedRpm']), (DiskData['UncorrectedReadErrors']), (DiskData['UncorrectedWriteErrors']))
        self.cursor.execute("INSERT INTO HostDisks(DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
        self.DBConnection.commit()
    
    def Get_DiskDatabase2(self, SearchMethod: str) -> str:
        # cursor = database.cursor()
        print(type(SearchMethod))
        if(SearchMethod == 'Full'):
            for row in self.DBConnection.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
            # Query = database.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC")
        elif(SearchMethod == 'Hosts'):
            for row in self.DBConnection.execute("SELECT ID, DateEntryAdded, Hostname, HealthStatus FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
        else:
            Query = self.DBConnection.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC")
            return(Query)
        
    