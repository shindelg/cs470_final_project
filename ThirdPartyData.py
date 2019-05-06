# Importing module
import sqlite3, csv

# Connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# Function to create the table based on new data
CreateCCData = """CREATE TABLE CapitalCubeData (
_links VARCHAR(200),
asOfDate DATETIME,
closingPrice REAL,
country VARCHAR(50),
currency VARCHAR(10),
dividendQualityScore VARCHAR(10),
exchange VARCHAR(10),
fiftyTwoWeekHigh REAL,
fiftyTwoWeekLow REAL,
fundamentalAnalysisScore INTEGER,
latestAnnualFilingDate DATETIME,
latestQuarterlyAnnualFilingDate DATETIME,
latestSemiAnnualFilingDate DATETIME,
marketCap REAL,
name VARCHAR(100),
oneMonthSharePricePerformance REAL,
oneYearSharePricePerformance REAL,
peers VARCHAR(100),
profile VARCHAR(1000),
symbol VARCHAR(25)
);"""

# Function to create the table based on new data
CreateNewData = """CREATE TABLE NewData (
CompanyId INTEGER PRIMARY KEY,
CompanyName VARCHAR(100),
TickerSymbol VARCHAR(20),
FinancesCurrency VARCHAR(20),
MarketCapitalizationInUsd REAL,
AnnualRevenueInUsd REAL,
FinancesCurrentAsOf DATETIME,
Peers VARCHAR(200)
);"""

# Function to create the table for exchange rates
CreateExchangeRate = """CREATE TABLE ExchangeRates (
Currency VARCHAR(5) PRIMARY KEY,
ExRate INTEGER,
CurrentDate Date
);"""


# Cursor object
crsr = connection.cursor()

# Create the CapitalCube data table
crsr.execute(CreateCCData)

# This loads the data in from the Scraper csv into the CapitalCubeData Table
with open('SuccessTickers.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['_links'], i['asOfDate'], i['closingPrice'], i['country'], i['currency'], i['dividendQualityScore'], i['exchange'], i['fiftyTwoWeekHigh'], i['fiftyTwoWeekLow'], i['fundamentalAnalysisScore'], i['latestAnnualFilingDate'], i['latestQuarterlyAnnualFilingDate'], i['latestSemiAnnualFilingDate'], i['marketCap'], i['name'], i['oneMonthSharePricePerformance'], i['oneYearSharePricePerformance'], i['peers'], i['profile'], i['symbol']) for i in dr]

# Insert values from the Scraper csv into the CapitalCubeData Table
connection.executemany("INSERT INTO CapitalCubeData (_links, asOfDate, closingPrice, country, currency, dividendQualityScore, exchange, fiftyTwoWeekHigh, fiftyTwoWeekLow, fundamentalAnalysisScore, latestAnnualFilingDate, latestQuarterlyAnnualFilingDate, latestSemiAnnualFilingDate, marketCap, name, oneMonthSharePricePerformance, oneYearSharePricePerformance, peers, profile, symbol) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)

# Create the NewData table, where we will filter CapitalCube's data
crsr.execute(CreateNewData)

# Create the ExchangeRate table
crsr.execute(CreateExchangeRate)

# This loads the data in from the Scraper csv into the CapitalCubeData Table
with open('exchangeRate.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Currency'], i['ExRate']) for i in dr]

# Insert values into exchangeRate table
connection.executemany("INSERT INTO ExchangeRates VALUES (?,?, date('now'));", to_db)

# Get the company IDs from FTData separately
crsr.execute("SELECT CompanyId FROM FTData;")

# Set up company IDs to be inserted
comp_ids= crsr.fetchall()

# Filter out relevant data from CapitalCube into our NewData table
# fiftyTwoWeekLow is a placeholder for when we can actually get the annual revenue of a company
crsr.execute("SELECT name, symbol, currency, marketCap, fiftyTwoWeekLow, asOfDate, peers FROM CapitalCubeData;")

# Set up the relevant info to be inserted
other_info= crsr.fetchall()

# Insert the relevant data into NewData
connection.executemany("INSERT INTO NewData (CompanyName, TickerSymbol, FinancesCurrency, MarketCapitalizationInUsd, AnnualRevenueInUsd, FinancesCurrentAsOf, Peers) VALUES (?,?,?,?,?,?,?)", other_info)

#This alters the table to create a new column
crsr.execute("ALTER TABLE NewData ADD COLUMN NaviteCurrency INTEGER;")

crsr.execute("UPDATE NewData SET NaviteCurrency = (SELECT ExchangeRates.ExRate from ExchangeRates WHERE ExchangeRates.Currency = NewData.FinancesCurrency) * MarketCapitalizationInUsd")

# Function is to compare two tables within sqlite database
QueryOne = """SELECT DISTINCT FTData.CompanyId, FTData.CompanyName ,NewData.TickerSymbol, NewData.FinancesCurrency, NewData.MarketCapitalizationInUsd, NewData.NaviteCurrency, NewData.AnnualRevenueInUsd, NewData.FinancesCurrentAsOf, NewData.Peers, FTData.MarketCapitalizationInUsd, FTData.AnnualRevenueInUsd
FROM NewData JOIN FTData
WHERE NewData.TickerSymbol = FTData.TickerSymbol
AND (NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd
OR NewData.AnnualRevenueInUsd != FTData.AnnualRevenueInUsd)
;"""

#crsr.execute(QueryOne)

# Output to a csv
fields = ['CompanyId', 'CompanyName', 'TickerSymbol', 'FinancesCurrency', 'Updated MarketCapitalizationInUsd','MarketCapitalization in Native Currency','Updated AnnualRevenueInUsd', 'Upaded FinancesCurrentAsOf', 'Peers', 'Original MarketCapitalizationInUsd', 'Original AnnualRevenueInUsd']
toExport = crsr.execute(QueryOne)

with open('UpdatedCompanyInformation.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerows([(fields)])
    writer.writerows(toExport)

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# close the connection
connection.close()
