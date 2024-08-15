import pandas as pd
from pathlib import Path
import os
# from Sources.SupportFunctions import *
from Sources.DBClass import *
from Sources.RFClass import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Sources\ILOSourceSingleTest.csv')
ILOSheet = pd.read_csv(filename)
Client = DBClient()
Client.Create_Database_Tables()

for i in range(ILOSheet.iloc[:,1].count()):
    if(ILOSheet.iloc[i,2] != "IP"):
        # Response = Get_CustDisks(ILOSheet.iloc[i,3], ILOSheet.iloc[i,4], ILOSheet.iloc[i,2], ILOSheet.iloc[i,0])
        # print(Response)
        FClient = RFClient(ILOSheet.iloc[i,3], ILOSheet.iloc[i,4], ILOSheet.iloc[i,2])
        FClient.Gather_HostDisks(ILOSheet.iloc[i,0])
        # pass

# Get_DiskDatabase('Hosts')

DClient = DBClient()
DClient.Get_DiskDatabase2('Full')

