# importing module
import sqlite3, csv, pandas
#import "./publicComp.csv"

# connecting to the database
connection = sqlite3.connect("Temp_ForestTrends.db")

# cursor
crsr = connection.cursor()

# SQL command to create a table in the database This will be used to Creat
# ForestTrends original csv in sqlite
# sql_command = """CREATE TABLE PublicCompany (
# CompanyId INTEGER PRIMARY KEY,
# CompanySiteID INTEGER,
# CompanyName VARCHAR(50),
# PostToWebsite VARCHAR(50),
# Visible VARCHAR(10),
# Researcher VARCHAR(50),
# Cohort INTEGER,
# DateLastUpdated VARCHAR(50),
# RefreshSchedule VARCHAR(50),
# NextRefresh VARCHAR(50),
# RelevantParentCompany VARCHAR(50),
# RelevantSubsidiaryCompanies VARCHAR(50),
# AllAliases VARCHAR(50),
# FirstEightAliases VARCHAR(50),
# AllOtherAliases VARCHAR(50),
# CompanyWebsite VARCHAR(50),
# Majorcompanybrands VARCHAR(50),
# HeadquarterCountry VARCHAR(50),
# PublicOrPrivate VARCHAR(50),
# TickerSymbol VARCHAR(20),
# Sector VARCHAR(50),
# Industry VARCHAR(50),
# MarketCapitalizationDisclosed VARCHAR(50),
# MarketCapitalization INTEGER,
# AnnualRevenueDisclosed VARCHAR(50),
# AnnualRevenue INTEGER,
# FinancesCurrency VARCHAR(50),
# MarketCapitalizationInUsd INTEGER,
# AnnualRevenueInUsd INTEGER,
# FinancesCurrentAsOf VARCHAR(50),
# TwitterHandle VARCHAR(50),
# SustainabilityReporting VARCHAR(50),
# SustainabilityCommodityReporting VARCHAR(50),
# CommodityReportedon VARCHAR(50),
# SustainabilityReportingYear VARCHAR(50),
# AcknowledgeDeforestationIssue VARCHAR(50),
# AcknowlDeforestationwithCommod VARCHAR(50),
# CDP2015_voluntaryoffsetbuyer VARCHAR(50),
# PromiseFuturDeforestationCommit VARCHAR(50),
# CommodityTypeofFutureCommit VARCHAR(50),
# GeneralCommitment VARCHAR(50),
# SoyCommitment VARCHAR(50),
# PalmCommitment VARCHAR(50),
# TimberPulpCommitment VARCHAR(50),
# CattleCommitment VARCHAR(50),
# TotalCommitments INTEGER,
# DormantCommPresent VARCHAR(50),
# NumberOfAssessments INTEGER,
# NumberOfRelatedActivities INTEGER,
# CreatedAt VARCHAR(50),
# ModifiedAt VARCHAR(50),
# VoluntaryOffsets VARCHAR(50),
# Researcher_Other VARCHAR(50),
# UpdatedNotes VARCHAR(50));"""


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
