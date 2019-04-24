# Importing module
import sqlite3, csv

# Connecting to the database

connection = sqlite3.connect("Temp_ForestTrends.db")
print("Connected to Temp_ForestTrends Database")

# Cursor
crsr = connection.cursor()

# Define a function that we will be using often for debugging purposes
getTickers = "SELECT TickerSymbol FROM Tickers"

# Function to create the FT Table; this is the data we get from ForestTrends
CreateFT = """CREATE TABLE FTData (
CompanyId INTEGER PRIMARY KEY,
CompanyName VARCHAR(100),
TickerSymbol VARCHAR(20),
FinancesCurrency VARCHAR(20),
MarketCapitalizationInUsd INTEGER,
AnnualRevenueInUsd INTEGER,
FinancesCurrentAsOf DATE
);"""


# Create the FTData Table for loading in unfiltered data
crsr.execute(CreateFT)


# This loads the data in from the ForestTrends csv into the FTData Table publicComp.csv
with open('publicComp.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['CompanyId'], i['CompanyName'], i['TickerSymbol'], i['FinancesCurrency'], i['MarketCapitalizationInUsd'], i['AnnualRevenueInUsd'], i['FinancesCurrentAsOf']) for i in dr]

# Insert values from the ForestTrends csv into the FTData Table
connection.executemany("INSERT INTO FTData (CompanyId, CompanyName, TickerSymbol, FinancesCurrency,MarketCapitalizationInUsd,AnnualRevenueInUsd, FinancesCurrentAsOf ) VALUES (?,?,?,?,?,?,?);", to_db)


# Output to a csv
toExport = crsr.execute("SELECT TickerSymbol FROM FTData WHERE TickerSymbol NOT LIKE '';")

with open('output.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(['Tickers'])
    writer.writerows(toExport)

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# Close the connection
connection.close()
