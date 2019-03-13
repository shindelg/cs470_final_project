import csv
import sys
import pandas as pd


def get_public_company(filename):
  companies = pd.read_csv(filename)
  publicComp = companies[(companies.PublicOrPrivate == "Publicly traded") | (companies.PublicOrPrivate == "Public")]

  # Publicly traded companies : all information
  publicComp.to_csv("publicComp.csv")

  # Publicly traded companies : selected information
  selectedHeader = ["PublicOrPrivate", "CompanyName", "HeadquarterCountry", "TickerSymbol", "FinancesCurrency"]
  publicComp[selectedHeader].to_csv("simpleVersion.csv",index = False)
  # tmp = publicComp.reindex(columns = selectedHeader)

  

def main(argv):
  get_public_company(argv)

main(sys.argv[1])
