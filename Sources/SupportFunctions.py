import redfish
import json
import sqlite3
import os
from pathlib import Path

def Get_CustDisks(Username, Password, HostIP, Hostname):
    base_url = "https://" + (HostIP)
    REDFISH_OBJ = redfish.redfish_client(base_url=base_url, username=(Username), password=(Password), default_prefix='/redfish/v1/')
    REDFISH_OBJ.login(auth="session")
    
    if((len(((REDFISH_OBJ.get('/redfish/v1/Systems/1/Storage/').dict)['Members']))) >= 1):
        print("Drive Method: Drive storage not empty")
        return("Drive Method")
    elif(1 == 1):
        print("Storage Controller Method")
        ControllerList = (REDFISH_OBJ.get("/redfish/v1/Systems/1/SmartStorage/ArrayControllers").dict)['Members']
        for Controller in ControllerList:
            ControllerData = REDFISH_OBJ.get((Controller['@odata.id'])).dict
            DisksData = (REDFISH_OBJ.get(ControllerData['Links']['PhysicalDrives']['@odata.id']).dict)['Members']
            for Disks in DisksData:
                DiskData = REDFISH_OBJ.get(Disks['@odata.id']).dict
                Write_DiskDatabase(Hostname, (DiskData['Id']), (DiskData['SerialNumber']), (DiskData['Model']), (DiskData['Status']['Health']), (DiskData['CapacityGB']), (DiskData['CurrentTemperatureCelsius']), (DiskData['MaximumTemperatureCelsius']), (DiskData['Description']), (''.join(str(x) for x in DiskData['DiskDriveStatusReasons'])), (DiskData['FirmwareVersion']['Current']['VersionString']), (DiskData['InterfaceSpeedMbps']), (DiskData['InterfaceType']), (DiskData['Location']), (DiskData['MediaType']), (DiskData['PowerOnHours']), (DiskData['RotationalSpeedRpm']), (DiskData['UncorrectedReadErrors']), (DiskData['UncorrectedWriteErrors']))
    REDFISH_OBJ.logout()
    return("DiskData Added To Database")

def Write_DiskDatabase(Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors):
    SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')

    database = sqlite3.connect(SQLfilename)
    cursor = database.cursor()

    InsertData = (Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors)
    cursor.execute("INSERT INTO HostDisks(DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", InsertData)
    database.commit()

    # for row in database.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC"):
    #     print(row)

    database.close()

def Create_Database_Tables():
    SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')
    if not(os.path.isfile(SQLfilename)):
        database = sqlite3.connect(SQLfilename)
        cursor = database.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS HostDisks (id integer primary key, DateEntryAdded, Hostname, DriveID, SerialNumber, Model, HealthStatus, CapacityGB, CurrentTemperatureCelsius, MaximumTemperatureCelsius, Description, DiskDriveStatusReasons, FirmwareVersion, InterfaceSpeedMbps, InterfaceType, Location, MediaType, PowerOnHours, RotationalSpeedRpm, UncorrectedReadErrors, UncorrectedWriteErrors)")
        # cur.execute("CREATE TABLE IF NOT EXISTS HostData (id integer primary key, Date Entry Added, )")
        database.commit()
        database.close()
        return("Creating Database")
    else:
        return("Database Already Exists")

def Get_DiskDatabase():
    SQLfilename = os.path.join((os.path.dirname(__file__)), 'RedDataBase.db')
    database = sqlite3.connect(SQLfilename)
    # cursor = database.cursor()
    for row in database.execute("SELECT * FROM HostDisks ORDER BY DateEntryAdded DESC"):
        print(row)
        
    # for row in database.execute("SELECT ID, Hostname, DriveID, Healthstatus FROM HostDisks ORDER BY DateEntryAdded DESC"):
    #     print(row)
    # for row in database.execute("SELECT ID, Hostname, DriveID, Healthstatus FROM HostDisks WHERE DriveID='5' AND ID='6'"):
    #     print(row)
    database.close()