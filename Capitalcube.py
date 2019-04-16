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
  # df = pd.read_csv(tickerCSV, index_col=False) # na_values=['NA']
  df = pd.read_csv(tickerCSV) # na_values=['NA']
  totalRow = df.shape[0] #49
  print("Total ", totalRow, "company information requested")
  
  columns = ['TickerSymbol', 'Name', 'HeadquarterCountry', 'PublicOrPrivate', 'Sector', 
  'Industry', 'MarketCapitalization', 'AnnualRevenue', 'FinancesCurrency', 'Exchange', 
  'MarketCapitalizationInUsd', 'AnnualRevenueInUsd', 'FinancesCurrentAsOf', 'Profile', 'LastUpdated']
  
  successDataset = pd.DataFrame(columns=columns)
  failedDataset = pd.DataFrame()
  success = []
  failed = []

  for index, name in df.itertuples():  
    if "-" not in name:
      print("Incorrect format")
      print("Needs form: <ticker symbol>-<country code>")
      return

    # Get url response
    urls = ["https://api.capitalcube.com/companies/" +name, "https://api.capitalcube.com/companies/" +name +"/peers"]
    # url = "https://api.capitalcube.com/companies/" +name
    # resp = requests.get(url)

    for url in urls:
      
      resp = requests.get(url)
      
      if resp.ok:
        print(resp)

        try:
          data = resp.json()
        except json.decoder.JSONDecodeError:
          print("Invalid ticker symbol: " +name)
          print("Enter valid NASDQ or exchange ticker")
          failed.append({'FailedTicker':name})
          continue

        peersList = []
        if "peers" in url:
          holder = data['_links']['cn:peer']
          for peerTicker in holder:
            for k, v in peerTicker.items():
              if k == "symbol":
                peersList.append(v)
        print(peersList)

        # if not peersList:
        #   data['peers'] = None
        # else:
        data['peers'] = peersList
        success.append(data)
        peersList.clear()
        # print("dinedoen: ", peersList)
        
  failedDataset = pd.DataFrame.from_dict(failed, orient='columns')
  failedDataset.to_csv("FailedTicker.csv", index=False)
  successDataset = pd.DataFrame.from_dict(success, orient='columns')
  successDataset.to_csv("Success.csv", index=False)

def main():
  retrieve_data("inputCSV.csv")

main()
