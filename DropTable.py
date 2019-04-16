# importing module
import sqlite3

#This file it used to drop the PublicCompany file from the
#Temp_ForestTrends database

# connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# cursor
crsr = connection.cursor()

# SQL command to Drop Tables
crsr.execute(" Drop table if exists FTData; ")
crsr.execute(" Drop table if exists NewData; ")
crsr.execute(" Drop table if exists Tickers; ")

print("Successfully Dropped all tables from Database")

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# close the connection
connection.close()
