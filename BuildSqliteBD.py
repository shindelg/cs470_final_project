# importing module
import sqlite3, csv
#import "./publicComp.csv"

# connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# cursor
crsr = connection.cursor()

# SQL command to create a table in the database This will be used to Creat
# ForestTrends skimmed csv csv in sqlite
sql_command = """CREATE TABLE PublicCompany (
CompanyId INTEGER PRIMARY KEY,
CompanyName VARCHAR(100),
TickerSymbol VARCHAR(20),
FinancesCurrency VARCHAR(20),
MarketCapitalizationInUsd INTEGER,
AnnualRevenueInUsd INTEGER,
FinancesCurrentAsOf VARCHAR(20)
);"""

# execute the statement
crsr.execute(sql_command)

sql_command = """CREATE TABLE UpdatedPublicCompany (
CompanyId INTEGER PRIMARY KEY,
CompanyName VARCHAR(100),
TickerSymbol VARCHAR(20),
FinancesCurrency VARCHAR(20),
MarketCapitalizationInUsd INTEGER,
AnnualRevenueInUsd INTEGER,
FinancesCurrentAsOf INTEGER
);"""

# execute the statement
crsr.execute(sql_command)

#This loads the data in from the csv into the PublicCompany Table
with open('publicComp.csv', 'rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['CompanyId'], i['CompanyName'], i['TickerSymbol'], i['FinancesCurrency'], i['MarketCapitalizationInUsd'], i['AnnualRevenueInUsd'], i['FinancesCurrentAsOf']) for i in dr]

connection.executemany("INSERT INTO PublicCompany (CompanyId, CompanyName, TickerSymbol, FinancesCurrency,MarketCapitalizationInUsd,AnnualRevenueInUsd, FinancesCurrentAsOf ) VALUES (?,?,?,?,?,?,?);", to_db)

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# close the connection
connection.close()
