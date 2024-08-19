import pandas as pd
from pathlib import Path
import os
from Sources.DBClass import *
from Sources.RFClass import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Sources\ILOSourceSingleTest.csv')
ILOSheet = pd.read_csv(filename)
DClient = DBClient()
DClient.Create_Database_Tables()
for host in range(ILOSheet.iloc[:,1].count()):
    if(ILOSheet.iloc[host,0] != "Hostname"):
        DClient.Write_HostListDatabase(ILOSheet.iloc[host,0])

for i in range(ILOSheet.iloc[:,1].count()):
    if(ILOSheet.iloc[i,2] != "IP"):
        FClient = RFClient(ILOSheet.iloc[i,3], ILOSheet.iloc[i,4], ILOSheet.iloc[i,2])
        FClient.Gather_HostDisks(ILOSheet.iloc[i,0])
        pass

# Get_DiskDatabase('Hosts')

DClient.Get_DiskDatabase('Full')
# DClient.Get_DiskByID('3')

