import json
import requests
import sys
import csv
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from collections import OrderedDict
from datetime import datetime, timedelta

# Auth
s = requests.Session()
s.auth = ('user', 'pw')

def retrieve_data(tickerCSV):

  df = pd.read_csv(tickerCSV)
  totalRow = df.shape[0]

  print("Total ", totalRow, "company information requested")

  successDataset = pd.DataFrame()
  failedDataset = pd.DataFrame()
  success = []
  failed = []

  ###########################################################
  #                                                         #
  #                     Tickers Iteration                   #
  #                                                         #
  ###########################################################
  for index, name in df.itertuples():
    print(name)

    if "-" not in name:
      print("Incorrect format")
      print("Needs form: <ticker symbol>-<country code>")

      failed.append({'FailedTicker':name})
      continue

    # If ticker contains empty space in it, sort it to FailedTicker
    if " " in name:
      failed.append({'FailedTicker': name})
      continue

    ###########################################################
    #          Request for company general information        #
    ###########################################################
    url_generalCompanyInfo = "https://api.capitalcube.com/companies/" +name
    resp_generalCompanyInfo = requests.get(url_generalCompanyInfo)

    if resp_generalCompanyInfo.status_code == 200:
      try:
        data = resp_generalCompanyInfo.json()
      except json.decoder.JSONDecodeError:
        print(name, ": failed to retrieve data from CapitalCube")
        failed.append({'FailedTicker':name})
        continue

      # Save lastet annual filing date to get annual revenue
      # (url request 3 below)
      lfd = data['latestAnnualFilingDate'][:10]
      latestAnnualFilingDate = str(datetime.strptime(lfd, '%Y-%m-%d') - timedelta(days=1))[:10]

      ###########################################################
      #              Nested request for company peers           #
      ###########################################################
      url_peers = "https://api.capitalcube.com/companies/" +name +"/peers"
      resp_peers = requests.get(url_peers)

      if resp_peers.status_code == 200:
        try:
          peersData = resp_peers.json()
        except json.decoder.JSONDecodeError:
          print("Error occured while retrieving peers list")
          continue

        peersList = []
        holder = peersData['_links']['cn:peer']

        for peerTicker in holder:
          for k, v in peerTicker.items():
            if k == "symbol":
              peersList.append(v)

        data['peers'] = peersList
        success.append(data)

      ###########################################################
      #    Nested request for annual/latest quarterly revenue   #
      ###########################################################
      url_annualrevenue = "https://api.capitalcube.com/companies/" +name +"/reports/financials/income-statement"
      resp_annualrevenue = requests.get(url_annualrevenue)

      if resp_annualrevenue.status_code == 200:
        try:
          revenueData = resp_annualrevenue.json()
        except json.decoder.JSONDecodeError:
          print("Error occured while retrieving annual revenue")
          continue

        # annual revenue
        ttmIndex = revenueData['rows'][1]['values'].index(latestAnnualFilingDate)
        ttm = float(revenueData['rows'][2]['values'][ttmIndex]) * 1000000

        # latest quarterly revenue if exists
        lqrIndex = revenueData['rows'][0]['values'].index('TTM')
        lqr = float(revenueData['rows'][2]['values'][lqrIndex]) * 1000000

        data['latestAnnualRevenue'] = ttm
        data['latestQuarterlyRevenue'] = lqr
        success.append(data)

      ###########################################################
      #           Further nested request comes here             #
      ###########################################################
      '''
      url_example_format = "https://api.capitalcube.com/companies/" +name +"/[subresource...]"
      resp_example_format = requests.get(url_example_format)

      if resp_example_format.status_code == 200:
        try:
          exampleData = resp_example_format.json()
        except json.decoder.JSONDecodeError:
          print("Error occured while (FILL_IN_HERE)")
          continue

        # OBTAIN DATA
        ...

        # append data
        data['COLUMN NAME'] = COLUMN VALUE
        success.append(data)
      '''

  failedDataset = pd.DataFrame.from_dict(failed, orient='columns')
  failedDataset.to_csv("FailedTickers.csv", index=False)
  successDataset = pd.DataFrame.from_dict(success, orient='columns')
  successDataset.to_csv("SuccessTickers.csv", index=False)

def main():
  retrieve_data("output.csv")

main()
