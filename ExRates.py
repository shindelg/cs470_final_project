# importing module
import sqlite3, csv

# Connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# Function to create the table for exchange rates
CreateExchangeRate = """CREATE TABLE ExchangeRates (
Currency VARCHAR(5) PRIMARY KEY,
ExRate INTEGER,
CurrentDate Date
);"""

# Cursor object
crsr = connection.cursor()

# Create the ExchangeRate table
crsr.execute(CreateExchangeRate)

# This loads the data in from the Scraper csv into the CapitalCubeData Table
with open('exchangeRate.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Currency'], i['ExRate']) for i in dr]

# Insert values into exchangeRate table
connection.executemany("INSERT INTO ExchangeRates VALUES (?,?, date('now'));", to_db)


# crsr.execute("INSERT INTO ExchangeRates (Currency,ExRate,CurrentDate) VALUES ('USD', 1, date('now'));")


# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# close the connection
connection.close()
