# Importing module
import sqlite3, csv
# Import "./publicComp.csv"

# Connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

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

# Function to create a table of just the ticker symbols, to be standardized
CreateTickers = """CREATE TABLE Tickers (
TickerSymbol VARCHAR(20)
);"""

# Function to create the table based on new data
CreateNewData = """CREATE TABLE NewData (
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


# Create the New Data table to insert new data from Capital Cube
crsr.execute(CreateNewData)

# This loads the data in from the Updated csv into the NewData Table
with open('newdata.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['CompanyId'], i['CompanyName'], i['TickerSymbol'], i['FinancesCurrency'], i['MarketCapitalizationInUsd'], i['AnnualRevenueInUsd'], i['FinancesCurrentAsOf']) for i in dr]

# Insert values from the newdata csv into the NewData Table
connection.executemany("INSERT INTO NewData (CompanyId, CompanyName, TickerSymbol, FinancesCurrency,MarketCapitalizationInUsd,AnnualRevenueInUsd, FinancesCurrentAsOf ) VALUES (?,?,?,?,?,?,?);", to_db)


# Create the Tickers table for standardizing ticker symbols
crsr.execute(CreateTickers)

# Filter the ticker symbols to not include blank tickers
crsr.execute("SELECT TickerSymbol FROM FTData WHERE TickerSymbol NOT LIKE '';")

# Set up the filtered tickers to be added into a new table named Tickers (one column that is just tickers)
newTickers= crsr.fetchall()

# Insert the filtered tickers into the Tickers table
for i in newTickers:
	crsr.execute("INSERT INTO Tickers (TickerSymbol) VALUES (?);", i)

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# Close the connection
connection.close()