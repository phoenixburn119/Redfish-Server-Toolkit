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
    
    # WIP The first option in if is broken
    def Gather_HostDisks(self, Hostname: str) -> str:
        if((len(((self.RFConnection.get('/redfish/v1/Systems/1/Storage/').dict)['Members']))) >= 1):
            DataBaseClient = DBClient()
            print("Storage Controller Method")
            ControllerList = (self.RFConnection.get("/redfish/v1/Systems/1/Storage/").dict)['Members']
            for Controller in ControllerList:
                ControllerData = self.RFConnection.get((Controller['@odata.id'])).dict
                DisksData = (self.RFConnection.get(ControllerData['Links']['PhysicalDrives']['@odata.id']).dict)['Members']
                for Disks in DisksData:
                    DiskData = self.RFConnection.get(Disks['@odata.id']).dict
                    DataBaseClient.Write_DiskDatabase(DiskData, Hostname)
            return("DiskData Added To Database")
        # 
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
            return("DiskData Added To Database")
    
    def Gather_Summary(self) -> str:
        DataBaseClient = DBClient()
        SystemSummary = (self.RFConnection.get("/redfish/v1/systems/1/").dict)
        SystemProc = (self.RFConnection.get("/redfish/v1/Systems/1/Processors/").dict)
        SystemBios = (self.RFConnection.get("/redfish/v1/systems/1/bios").dict)
        DataBaseClient.Write_SummaryInfo(SystemSummary, SystemProc, SystemBios)
        return("Host summary data has been written to database.")

    def Gather_BIOSData(self):
        pass