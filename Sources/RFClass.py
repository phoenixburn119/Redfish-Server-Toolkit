import redfish
from Sources.DBClass import *

class RFClient:
    RFConnection = None
    def __init__(self, Username: str, Password: str, MangIP: str) -> str:
        base_url = "https://" + (MangIP)
        self.RFConnection = REDFISH_OBJ = redfish.redfish_client(base_url=base_url, username=(Username), password=(Password), default_prefix='/redfish/v1/')
        self.RFConnection.login(auth="session")
        
    def __del__(self):
        self.RFConnection.logout()
    
    def Gather_HostDisks(self, Hostname: str) -> str:
        # if((len(((self.RFConnection.get('/redfish/v1/Systems/1/Storage/').dict)['Members']))) >= 1):
        if((len(((self.RFConnection.get('/redfish/v1/Systems/1/Storage/').dict)['Members']))) >= 1):
            print("Drive Method: Drive storage not empty")
            return("Drive Method")
        elif(1 == 1):
            DataBaseClient = DBClient()
            print("Storage Controller Method")
            ControllerList = (self.RFConnection.get("/redfish/v1/Systems/1/SmartStorage/ArrayControllers").dict)['Members']
            for Controller in ControllerList:
                ControllerData = self.RFConnection.get((Controller['@odata.id'])).dict
                DisksData = (self.RFConnection.get(ControllerData['Links']['PhysicalDrives']['@odata.id']).dict)['Members']
                for Disks in DisksData:
                    DiskData = self.RFConnection.get(Disks['@odata.id']).dict
                    DataBaseClient.Write_DiskDatabase(DiskData, Hostname)
                    # Write_DiskDatabase(Hostname, (DiskData['Id']), (DiskData['SerialNumber']), (DiskData['Model']), (DiskData['Status']['Health']), (DiskData['CapacityGB']), (DiskData['CurrentTemperatureCelsius']), (DiskData['MaximumTemperatureCelsius']), (DiskData['Description']), (''.join(str(x) for x in DiskData['DiskDriveStatusReasons'])), (DiskData['FirmwareVersion']['Current']['VersionString']), (DiskData['InterfaceSpeedMbps']), (DiskData['InterfaceType']), (DiskData['Location']), (DiskData['MediaType']), (DiskData['PowerOnHours']), (DiskData['RotationalSpeedRpm']), (DiskData['UncorrectedReadErrors']), (DiskData['UncorrectedWriteErrors']))
        return("DiskData Added To Database")