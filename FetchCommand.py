# Python code to demonstrate SQL to fetch data.

# importing the module
import sqlite3, csv

# connect withe the myTable database
connection = sqlite3.connect("Temp_ForestTrends.db")

# cursor object
crsr = connection.cursor()

# execute the command to fetch all the data from the table emp
#crsr.execute("SELECT * FROM PublicCompany")
#crsr.execute("SELECT * FROM NewData")


# Function is to compare two tables within sqlite database
QueryOne = """SELECT NewData.CompanyId, NewData.CompanyName, NewData.TickerSymbol, NewData.FinancesCurrency, NewData.MarketCapitalizationInUsd, NewData.AnnualRevenueInUsd, NewData.FinancesCurrentAsOf, FTData.MarketCapitalizationInUsd, FTData.AnnualRevenueInUsd
FROM NewData JOIN FTData
WHERE NewData.CompanyId = FTData.CompanyId
AND (NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd
OR NewData.AnnualRevenueInUsd != FTData.AnnualRevenueInUsd)
;"""

crsr.execute(QueryOne)

# Output to a csv
fields = ['CompanyId', 'CompanyName', 'TickerSymbol', 'FinancesCurrency', 'Updated MarketCapitalizationInUsd', 'Updated AnnualRevenueInUsd', 'FinancesCurrentAsOf', 'Original MarketCapitalizationInUsd', 'Original AnnualRevenueInUsd',]
toExport = crsr.execute(QueryOne)

with open('UpdatedCompanyInformation.csv', 'w+') as f:
    writer = csv.writer(f)
    writer.writerows([(fields)])
    writer.writerows(toExport)



# store all the fetched data in the ans variable
ans= crsr.fetchall()

# loop to print all the data
for i in ans:
    print(i)
