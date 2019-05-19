# Importing module
import sqlite3, csv

# Connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

################################################################################
# Table Creation
################################################################################

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
latestAnnualRevenue REAL,
latestQuarterlyAnnualFilingDate DATETIME,
latestQuarterlyRevenue REAL,
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
latestAnnualFilingDate DATETIME,
FinancesCurrentAsOf DATETIME,
Peers VARCHAR(200)
);"""

################################################################################
# Calling the queries above to create tables in database
################################################################################

# Cursor object
crsr = connection.cursor()

# Create the CapitalCube data table
crsr.execute(CreateCCData)

# Create the NewData table, where we will filter CapitalCube's data
crsr.execute(CreateNewData)

################################################################################
# Reading in SuccessTickers.csv and inserting data into CapitalCubeData Table
################################################################################

# This loads the data in from the Scraper csv into the CapitalCubeData Table
with open('SuccessTickers.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['_links'], i['asOfDate'], i['closingPrice'], i['country'], i['currency'], i['dividendQualityScore'], i['exchange'], i['fiftyTwoWeekHigh'], i['fiftyTwoWeekLow'], i['fundamentalAnalysisScore'], i['latestAnnualFilingDate'],i['latestAnnualRevenue'],i['latestQuarterlyAnnualFilingDate'],i['latestQuarterlyRevenue'],i['latestSemiAnnualFilingDate'], i['marketCap'], i['name'], i['oneMonthSharePricePerformance'], i['oneYearSharePricePerformance'], i['peers'], i['profile'], i['symbol']) for i in dr]

# Insert values from the Scraper csv into the CapitalCubeData Table
connection.executemany("INSERT INTO CapitalCubeData (_links, asOfDate, closingPrice, country, currency, dividendQualityScore, exchange, fiftyTwoWeekHigh, fiftyTwoWeekLow, fundamentalAnalysisScore, latestAnnualFilingDate, latestAnnualRevenue,latestQuarterlyAnnualFilingDate,  latestQuarterlyRevenue, latestSemiAnnualFilingDate ,marketCap, name, oneMonthSharePricePerformance, oneYearSharePricePerformance, peers, profile, symbol) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)

################################################################################
# Querying CapitalCubeData for the data that needs to go into NewData table
# and inserting it into NewData.
################################################################################

# Filter out relevant data from CapitalCube into our NewData table
crsr.execute("SELECT name, symbol, currency, marketCap, latestAnnualRevenue, latestAnnualFilingDate, asOfDate, peers FROM CapitalCubeData;")

# Set up the relevant info to be inserted
other_info= crsr.fetchall()

# Insert the relevant data into NewData
connection.executemany("INSERT INTO NewData (CompanyName, TickerSymbol, FinancesCurrency, MarketCapitalizationInUsd, AnnualRevenueInUsd, latestAnnualFilingDate,FinancesCurrentAsOf, Peers) VALUES (?,?,?,?,?,?,?,?)", other_info)

################################################################################
# Altering NewData Table to have NativeCurrency column
################################################################################

#This alters the table to create a new column
crsr.execute("ALTER TABLE NewData ADD COLUMN NaviteCurrency INTEGER;")

crsr.execute("UPDATE NewData SET NaviteCurrency = (SELECT ExchangeRates.ExRate from ExchangeRates WHERE ExchangeRates.Currency = NewData.FinancesCurrency) * MarketCapitalizationInUsd")

################################################################################
# The query below retrieves the data that will go into UpdatedCompanyInformation
################################################################################

# Function is to compare two tables within sqlite database
QueryOne = """SELECT DISTINCT FTData.CompanyId, FTData.CompanyName ,NewData.TickerSymbol,
NewData.FinancesCurrency, (SELECT round ((NewData.MarketCapitalizationInUsd * 1000000),2)),
(SELECT round ((NewData.NaviteCurrency * 1000000),2)), NewData.AnnualRevenueInUsd,
NewData.latestAnnualFilingDate, NewData.FinancesCurrentAsOf, NewData.Peers,
FTData.MarketCapitalizationInUsd, FTData.AnnualRevenueInUsd
FROM NewData JOIN FTData
WHERE NewData.TickerSymbol = FTData.TickerSymbol
AND (NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd)
;"""

################################################################################
# The creation of UpdatedCompanyInformation
################################################################################
# Output to a csv
fields = ['CompanyId', 'CompanyName', 'TickerSymbol', 'FinancesCurrency', 'Updated MarketCapitalizationInUsd','MarketCapitalization in Native Currency','AnnualRevenueInUsd', 'LatestAnnualFilingDate','Upaded FinancesCurrentAsOf', 'Peers', 'Original MarketCapitalizationInUsd', 'Original AnnualRevenueInUsd']
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
