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
        # if not(os.path.isfile(os.path.join((os.path.dirname(__file__)), 'RedDataBase.db'))):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS HostIDList (id integer primary key, DateEntryAdded text CURRENT_TIMESTAMP, Hostname TEXT type UNIQUE)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS HostDisks (id integer primary key, DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostChassis (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostBIOS (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostSystem (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostNetwork (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostFans (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostThermal (id integer primary key, DateEntryAdded)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostPower (id integer primary key, DateEntryAdded)")
        self.DBConnection.commit()
        return("Creating Database")
        # else:
        #     return("Database Already Exists")
        
    def Write_HostListDatabase(self, Hostname: str) -> str:
        try:
            with self.DBConnection:
                self.cursor.execute("INSERT INTO HostIDList(Hostname) VALUES (?)", [Hostname])
        except:
            print(f"Hostname {Hostname} could not be added as it was a duplicate entry.")
        for row in self.DBConnection.execute("SELECT * FROM HostIDList"):
                print(row)
        
            

    def Write_DiskDatabase(self, DiskData: dict, Hostname: str):
        InsertData = (Hostname, (DiskData['Id']), (DiskData['SerialNumber']), (DiskData['Model']), (DiskData['Status']['Health']), (DiskData['CapacityGB']), (DiskData['CurrentTemperatureCelsius']), (DiskData['MaximumTemperatureCelsius']), (DiskData['Description']), (''.join(str(x) for x in DiskData['DiskDriveStatusReasons'])), (DiskData['FirmwareVersion']['Current']['VersionString']), (DiskData['InterfaceSpeedMbps']), (DiskData['InterfaceType']), (DiskData['Location']), (DiskData['MediaType']), (DiskData['PowerOnHours']), (DiskData['RotationalSpeedRpm']), (DiskData['UncorrectedReadErrors']), (DiskData['UncorrectedWriteErrors']))
        self.cursor.execute("INSERT INTO HostDisks(DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
        self.DBConnection.commit()
        
    def Write_SysInfo(self):
        pass
    
    def Get_DiskDatabase(self, SearchMethod: str) -> str:
        print(type(SearchMethod))
        if(SearchMethod == 'Full'):
            for row in self.DBConnection.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
            # Query = database.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC")
        elif(SearchMethod == 'Hosts'):
            for row in self.DBConnection.execute("SELECT ID, DateEntryAdded, Hostname, HealthStatus FROM HostDisks ORDER BY DateEntryAdded DESC"):
                print(row)
        else:
            Query = self.DBConnection.execute("SELECT  FROM HostDisks")
            return(Query)
        
    def Get_DiskByID(self, DiskID: str) -> str:
        for row in self.DBConnection.execute("SELECT * FROM HostDisks WHERE DriveID=?", DiskID):
            print(row)
            
        self.cursor.execute("SELECT * FROM HostDisks WHERE DriveID=?", DiskID)
        print(self.cursor.fetchall())
        
    