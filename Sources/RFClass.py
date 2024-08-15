import redfish
class RFClient:
    RF_Client = None
    def __init__(self, Username: str, Password: str, MangIP: str):
        base_url = "https://" + (MangIP)
        self.RF_Client = REDFISH_OBJ = redfish.redfish_client(base_url=base_url, username=(Username), password=(Password), default_prefix='/redfish/v1/')
        self.RF_Client = REDFISH_OBJ.login(auth="session")
        
    def __del__(self):
        self.RF_Client.logout()
    
    def Get_HostDisks():
        pass