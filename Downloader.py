import sys
sys.path.insert(0, 'Backend')
from Backend import BackendFunctions
url = 'https://advisorshares.com/wp-content/uploads/csv/holdings/AdvisorShares_GK_Holdings_File.csv'
dStatus = BackendFunctions.downloadCSV(url)
if dStatus == 0:
    print("No Change to Database")
elif dStatus == 1:
    print("Database Updated")


