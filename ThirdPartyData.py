# Importing module
import sqlite3, csv

# Connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# Function to create the table based on new data
CreateNewData = """CREATE TABLE NewData (
CompanyId INTEGER PRIMARY KEY,
CompanyName VARCHAR(100),
TickerSymbol VARCHAR(20),
FinancesCurrency VARCHAR(20),
MarketCapitalizationInUsd INTEGER,
AnnualRevenueInUsd INTEGER,
FinancesCurrentAsOf DATETIME
);"""

# Cursor object
crsr = connection.cursor()

# Create the NewData table
crsr.execute(CreateNewData)

# This loads the data in from the Scraper csv into the NewData Table
with open('SuccessTickers.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['CompanyId'], i['CompanyName'], i['TickerSymbol'], i['FinancesCurrency'], i['MarketCapitalizationInUsd'], i['AnnualRevenueInUsd'], i['FinancesCurrentAsOf']) for i in dr]

# Insert values from the Scraper csv into the NewData Table
connection.executemany("INSERT INTO NewData (CompanyId, CompanyName, TickerSymbol, FinancesCurrency,MarketCapitalizationInUsd,AnnualRevenueInUsd, FinancesCurrentAsOf ) VALUES (?,?,?,?,?,?,?);", to_db)

# Execute the command to fetch all the data from NewData
#crsr.execute("SELECT * FROM PublicCompany")
#crsr.execute("SELECT * FROM NewData")

# Function is to compare two tables within sqlite database
QueryOne = """SELECT NewData.CompanyId, NewData.CompanyName, NewData.TickerSymbol, NewData.FinancesCurrency, NewData.MarketCapitalizationInUsd, NewData.AnnualRevenueInUsd, NewData.FinancesCurrentAsOf, FTData.MarketCapitalizationInUsd, FTData.AnnualRevenueInUsd
FROM NewData JOIN FTData
WHERE NewData.CompanyId = FTData.CompanyId
AND (NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd
OR NewData.AnnualRevenueInUsd != FTData.AnnualRevenueInUsd)
;"""

#crsr.execute(QueryOne)

# Output to a csv
fields = ['CompanyId', 'CompanyName', 'TickerSymbol', 'FinancesCurrency', 'Updated MarketCapitalizationInUsd', 'Updated AnnualRevenueInUsd', 'Upaded FinancesCurrentAsOf', 'Original MarketCapitalizationInUsd', 'Original AnnualRevenueInUsd',]
toExport = crsr.execute(QueryOne)

with open('UpdatedCompanyInformation.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerows([(fields)])
    writer.writerows(toExport)
