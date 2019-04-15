# Python code to demonstrate SQL to fetch data.

# importing the module
import sqlite3

# connect withe the myTable database
connection = sqlite3.connect("Temp_ForestTrends.db")

# cursor object
crsr = connection.cursor()

# execute the command to fetch all the data from the table emp
#crsr.execute("SELECT * FROM PublicCompany")
crsr.execute("SELECT * FROM NewData")


# Function is to compare two tables within sqlite database
#crsr.execute("SELECT * FROM NewData EXCEPT SELECT * FROM FTData")
#crsr.execute("SELECT * FROM NewData INNER JOIN FTData WHERE NewData.CompanyId = FTData.CompanyId")
#crsr.execute("SELECT * FROM NewData LEFT OUTER JOIN FTData WHERE NewData.CompanyId = FTData.CompanyId")

QueryOne = """SELECT * FROM NewData
JOIN FTData
WHERE NewData.CompanyId = FTData.CompanyId
AND (NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd
OR NewData.AnnualRevenueInUsd != FTData.AnnualRevenueInUsd)
;"""



#OR NewData.AnnualRevenueInUsd != FTData.AnnualRevenueInUsd
#crsr.execute("SELECT * FROM NewData JOIN FTData WHERE NewData.CompanyId = FTData.CompanyId AND NewData.MarketCapitalizationInUsd != FTData.MarketCapitalizationInUsd")

crsr.execute(QueryOne)
# crsr.execute(QueryTwo)


# store all the fetched data in the ans variable
ans= crsr.fetchall()

# loop to print all the data
for i in ans:
    print(i)
