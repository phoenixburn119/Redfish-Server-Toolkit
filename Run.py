import pandas as pd
from pathlib import Path
import os
import json
# from Sources.SupportFunctions import *
from Sources.DBClass import *
from Sources.RFClass import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Sources\ILOSourceSingleTest.csv')
ILOSheet = pd.read_csv(filename)
# Create_Database_Tables()

# for i in range(ILOSheet.iloc[:,1].count()):
#     if(ILOSheet.iloc[i,2] != "IP"):
#         Response = Get_CustDisks(ILOSheet.iloc[i,3], ILOSheet.iloc[i,4], ILOSheet.iloc[i,2], ILOSheet.iloc[i,0])
#         print(Response)

# Get_DiskDatabase('Hosts')

Client = DBClient()
Client.Get_DiskDatabase2('Full')