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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS HostIDList (id integer primary key, DateEntryAdded text default CURRENT_TIMESTAMP, Hostname TEXT type UNIQUE)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostDisks (id integer primary key, DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS HostDisks (id integer primary key, DateEntryAdded, Hostname, HostID, DriveID, Name, HealthStatus, StatusIndicator, BlockSizeBytes, CapableSpeedGbs, NegotiatedSpeedGbs, FailurePredicted, HostspareType, MediaType, Model, Location, PredictedMediaLifeLeftPercent, Protocol, Revision, SerialNumber, WriteCacheEnabled)")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS HostSummary (id integer primary key, DateEntryAdded text default CURRENT_TIMESTAMP, Hostname TEXT type UNIQUE, Model, SerialNumber, HPE Gen, CPU_Model, Management_IP, Management_Version, Number_Of_Proc, Number_of_Cores_per_proc, MultiThreading, RAM_in_GB, HostOS, HostOS_version)")
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
                
    # WIP not usable currently. 
    def Cleanup_Database_Tables(self, Hostlist: list):
        try:
            with self.DBConnection:
                CleanupList = self.cursor.execute("SELECT ID,Hostname FROM HostIDList").fetchall()
        except:
            pass
        print(Hostlist)
        print(CleanupList)
        # if():
        #     try:
        #         with self.DBConnection:
        #             self.cursor.execute("SELECT ID FROM HostIDList WHERE Hostname=?", [Hostname])
        #     except:
        #         pass
        # elif():
        #     pass
    
    # Returns the foreign key ID for the hostname from the HostIDList table.
    def Get_HostID(self, Hostname: str) -> str:
        self.cursor.execute("SELECT ID FROM HostIDList WHERE Hostname=?", [Hostname])
        HostIDReturn = self.cursor.fetchone()
        return(HostIDReturn[0])

    def Write_DiskDatabase(self, DiskData: dict, Hostname: str):
        HostID = self.Get_HostID(Hostname)
        # InsertData = (Hostname, (HostID), (DiskData['SerialNumber']), (DiskData['Model']), (DiskData['Status']['Health']), (DiskData['CapacityGB']), (DiskData['CurrentTemperatureCelsius']), (DiskData['MaximumTemperatureCelsius']), (DiskData['Description']), (''.join(str(x) for x in DiskData['DiskDriveStatusReasons'])), (DiskData['FirmwareVersion']['Current']['VersionString']), (DiskData['InterfaceSpeedMbps']), (DiskData['InterfaceType']), (DiskData['Location']), (DiskData['MediaType']), (DiskData['PowerOnHours']), (DiskData['RotationalSpeedRpm']), (DiskData['UncorrectedReadErrors']), (DiskData['UncorrectedWriteErrors']))
        InsertData = (Hostname, (HostID), (DiskData['Id']), (DiskData['Name']), (DiskData['Status']['Health']),(DiskData['StatusIndicator']), (DiskData['BlockSizeBytes']), (DiskData['CapableSpeedGbs']), (DiskData['NegotiatedSpeedGbs']), (DiskData['FailurePredicted']), (DiskData['HotspareType']), (DiskData['MediaType']), (DiskData['Model']), (DiskData['PhysicalLocation']['PartLocation']['ServiceLabel']), (DiskData['PredictedMediaLifeLeftPercent']), (DiskData['Protocol']), (DiskData['Revision']), (DiskData['SerialNumber']), (DiskData['WriteCacheEnabled'])) 
        # self.cursor.execute("INSERT INTO HostDisks(DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
        self.cursor.execute("INSERT INTO HostDisks(DateEntryAdded, Hostname, HostID, DriveID, Name, HealthStatus, StatusIndicator, BlockSizeBytes, CapableSpeedGbs, NegotiatedSpeedGbs, FailurePredicted, HostspareType, MediaType, Model, Location, PredictedMediaLifeLeftPercent, Protocol, Revision, SerialNumber, WriteCacheEnabled) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
        self.DBConnection.commit()
        
    def Write_SysInfo(self):
        pass
    
    def Write_SummaryInfo(self, SystemSummary:dict, SystemProc:dict, SystemBios:dict):
        InsertData = ((SystemSummary['HostName']), (SystemSummary['Model']), (SystemSummary['SerialNumber']), (SystemSummary['ProcessorSummary']['Model']), (SystemSummary['ProcessorSummary']['Count']), (SystemBios['Attributes']['ProcHyperthreading']), (SystemSummary['MemorySummary']['TotalSystemMemoryGiB']), (SystemSummary['Oem']['Hpe']['HostOS']['OsName']), (SystemSummary['Oem']['Hpe']['HostOS']['OsVersion']))
        try:
            with self.DBConnection:
                if(self.cursor.execute("SELECT")):
                    self.cursor.execute("INSERT INTO HostSummary(DateEntryAdded, Hostname, Model, SerialNumber, CPU_Model, Number_Of_Proc, MultiThreading, RAM_in_GB, HostOS, HostOS_version) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
                else:
                    pass
        except:
            print(f"Hostname {(SystemSummary['HostName'])} failed to write data.")
        
        print((self.cursor.execute("SELECT * FROM HostSummary").fetchall()))
            
    
    def Get_DiskDatabase(self, SearchMethod: str) -> str:
        print(type(SearchMethod))
        if(SearchMethod == 'Full'):
            for row in self.DBConnection.execute("SELECT * FROM HostDisks ORDER BY ID DESC"):
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
        return(self.cursor.fetchall())
