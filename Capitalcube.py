
import json
import requests
import sys
import csv
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from collections import OrderedDict
# Auth
s = requests.Session()
s.auth = ('user', 'pw')

def retrieve_data(tickerCSV):

  df = pd.read_csv(tickerCSV)
  totalRow = df.shape[0]
  print("Total ", totalRow, "company information requested")

  # TODO Reformat columns and information when retrieving data from Capitalcube?
  # columns = ['TickerSymbol', 'Name', 'HeadquarterCountry', 'PublicOrPrivate', 'Sector',
  # 'Industry', 'MarketCapitalization', 'AnnualRevenue', 'FinancesCurrency', 'Exchange',
  # 'MarketCapitalizationInUsd', 'AnnualRevenueInUsd', 'FinancesCurrentAsOf', 'Profile', 'LastUpdated']

  successDataset = pd.DataFrame()
  failedDataset = pd.DataFrame()
  success = []
  failed = []

  for index, name in df.itertuples():

    # TODO Throws error when ticker includes spaces (ex. HM B-SE)
    if "-" not in name:
      print("Incorrect format")
      print("Needs form: <ticker symbol>-<country code>")

      if name == 'Subsidiary':
        continue
      else:
        failed.append({'FailedTicker':name})
        continue

    # Request for company information
    url1 = "https://api.capitalcube.com/companies/" +name
    resp1 = requests.get(url1)

    if resp1.ok:
      print(resp1)

      try:
        data = resp1.json()
      except json.decoder.JSONDecodeError:
        print("Invalid ticker symbol: " +name)
        print("Enter valid NASDQ or exchange ticker")
        failed.append({'FailedTicker':name})
        continue

      # Request for company peers
      url2 = "https://api.capitalcube.com/companies/" +name +"/peers"
      resp2 = requests.get(url2)

      if resp2.ok:
        print("peers:", resp2)

        try:
          peersData = resp2.json()
        except json.decoder.JSONDecodeError:
          print("Error happened while pulling peers list")
          continue

        peersList = []
        holder = peersData['_links']['cn:peer']

        for peerTicker in holder:
          for k, v in peerTicker.items():
            if k == "symbol":
              peersList.append(v)

        data['peers'] = peersList
        success.append(data)

  failedDataset = pd.DataFrame.from_dict(failed, orient='columns')
  failedDataset.to_csv("FailedTickers.csv", index=False) # Failed tickers csv
  successDataset = pd.DataFrame.from_dict(success, orient='columns')
  successDataset.to_csv("SuccessTickers.csv", index=False) # Successful tickers with information csv

def main():
  # input file (list of Tickers with the header "Tickers")
  retrieve_data("output.csv")

main()

'''
Input file should start with the header "Tickers"
output.csv file example:
Tickers
MMM-US
DSY-FR
AAA-SE
'''
