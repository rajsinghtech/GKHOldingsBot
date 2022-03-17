from os import path
from parso import parse
import requests
from datetime import datetime
from dateutil.parser import parse as parsedate
def getPreviousDate(file):
    with open(file) as f:
        lines = f.readlines()
        print(type(lines))
        return datetime.fromisoformat(lines[0])

def writeNewDate(file, date):
    with open(file, 'w') as f:
        f.write(str(date))

def downloadCSV(url):
    head = requests.head(url)
    url_date = parsedate(requests.head(url).headers['Last-Modified']).astimezone()
    file_date = getPreviousDate("Backend/date.txt")
    print("Previous File date: " + str(file_date))
    print("New URL date:  " + str(url_date))
    if(url_date > file_date):
        writeNewDate("Backend/date.txt", url_date)
        user_agent = {"User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
        data = requests.get(url, headers=user_agent)
        with open("AdvisorShares_GK_Holdings_File.csv", 'wb')as file:
            file.write(data.content)
        print("Updated to: " + (str(url_date)))
        return 1
    else:
        print("No change: " + (str(file_date)))
        return 0

def cleanupCSV(file, url):
    local_file = 'CurrentHoldings.csv'
    data = requests.get(url)
    with open(local_file, 'wb')as file:
        file.write(data.content)
    dictionary = csv.DictReader(open(local_file))
    Holdings = list(dictionary)
    newDate = Holdings[0]['Date'].replace("/", "-")
    shutil.copyfile(local_file, "Holdings/" + newDate + ".csv")
    current = pd.read_csv("Holdings/" + newDate + ".csv")
    current.pop('Account Symbol')
    current.pop('Security Number')
    split = newDate.split("-")
    formatDate = split[2] + "-" + split[0] + "-" + split[1]
    current['Date'] = formatDate
    EmptyStockTicker = pd.isna(current['Stock Ticker'])
    i = 0
    for x in EmptyStockTicker:  
        if x == True:
            current['Stock Ticker'][i] = current['Security Description'][i].replace(" ", "")
        i = i + 1
    for rowIndex, row in current.iterrows():
        for columnIndex, value in row.items():
            x = str(current.at[rowIndex,columnIndex])
            x = x.replace(',','')
            x = x.replace('%','')
            current.at[rowIndex,columnIndex] = x
    current.to_csv("Holdings/" + newDate + ".csv", index=False)