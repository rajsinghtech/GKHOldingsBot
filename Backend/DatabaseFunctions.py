import sqlite3
from os.path import exists
import pandas as pd
import os
def createTable(databaseFile):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("""CREATE TABLE HoldingData(
            Date INT,
            StockTicker text,
            SecurityDescription text,
            Shares real,
            Price real,
            TradedMarketValue real,
            PortfolioWeight real,
            AssetGroup text
    )
    """)
    conn.commit()
    conn.close()

def addRow(databaseFile,row):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("INSERT INTO HoldingData VALUES (?,?,?,?,?,?,?,?)", (row['Date'],row['Stock Ticker'],row['Security Description'],row['Shares/Par (Full)'],row['Price (Base)'],row['Traded Market Value (Base)'],row['Portfolio Weight %'],row['Asset Group']))
    conn.commit()
    conn.close()

def addToTableFromFile(databaseFile, file):
    current = pd.read_csv(file)
    for i, row in current.iterrows():
            addRow(databaseFile, row)

def getTickerTime(databaseFile, name, limit):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("SELECT * FROM HoldingData WHERE StockTicker ='" + name + "' ORDER BY Date DESC LIMIT '" + str(limit) + "'")
    x = c.fetchall()
    conn.commit()
    conn.close() 
    return x

def getTicker(databaseFile, name):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("SELECT * FROM HoldingData WHERE StockTicker ='" + name + "' ORDER BY Date DESC")
    x = c.fetchall()
    conn.commit()
    conn.close() 
    return x


def dropTable(databaseFile):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS HoldingData")
    conn.commit()
    conn.close()

def getLatestDate(databaseFile):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("select Date from HoldingData ORDER BY Date DESC Limit 1;")
    x = c.fetchall()
    conn.commit()
    conn.close()
    return x[0][0]

def getDateData(databaseFile, date):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("SELECT * FROM HoldingData WHERE Date ='" + date + "' ORDER BY Date DESC")
    x = c.fetchall()
    conn.commit()
    conn.close()
    return x

def getLatestData(databaseFile):
    x = getLatestDate(databaseFile)
    x = getDateData(databaseFile, x)
    return x

def removeDuplicates(databaseFile):
    conn = sqlite3.connect(databaseFile)
    c = conn.cursor()
    c.execute("""DELETE FROM HoldingData
    WHERE EXISTS (
    SELECT 1 FROM HoldingData p2 
    WHERE HoldingData.Date = p2.Date
    AND HoldingData.StockTicker = p2.StockTicker
    AND HoldingData.rowid > p2.rowid
    );
    """)
    conn.commit()
    conn.close()

def reloadDatabase(databaseFile, directory):
    dropTable(databaseFile)
    print("Dropped Table: " + databaseFile)
    createTable(databaseFile)
    print("Created Table: " + databaseFile)
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            addToTableFromFile(databaseFile, f)
            print("Added: " + f)
    removeDuplicates(databaseFile)
    print("Removed Duplicates: " + databaseFile)





