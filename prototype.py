import urllib
import json
import sys
import requests
import csv
import os
from collections import OrderedDict

# Auth
s = requests.Session()
s.auth = ('user', 'pw')

def get_data(companiesCSV):
  
  companies = []
  with open(companiesCSV, 'r') as rd:
    companies = [str(s) for line in rd.readlines() for s in line[:-1].split(',')]

#   print(companies)
  
  # Delete files from previous API call
  failedExists = os.path.isfile("./FailedTicker.csv")
  successExists = os.path.isfile("./Success.csv")

  if failedExists:
    os.remove("FailedTicker.csv")
  if successExists:
    os.remove("Success.csv")
  
  # Create FailedTicker.csv for failed tickers 
  wrongTickerFile = csv.writer(open('FailedTicker.csv', 'a+'))
  wrongTickerFile.writerow([str("WrongTickers")])
  
  # Iterate through each company
  for name in companies:
    if name == "Tickers":
      continue
      
    if "-" not in name:
      print("Incorrect format")
      print("Needs form: <ticker symbol>-<country code>")
      return

    # Get url response
    url = "https://api.capitalcube.com/companies/" +name
    resp = requests.get(url)

    if(resp.ok):
      print(resp)

      #Try to open data, if not a json - failed query
      try:
        data = resp.json()
      except json.decoder.JSONDecodeError:
        print("Enter valid NASDQ or exchange ticker")
    
        wrongTickerFile.writerow([str(name)])
        continue

      info = OrderedDict(sorted(data.items(), key=lambda t : t[0]))

    #   for key, val in info.items():
    #     info[key] = val
    #     print(key + "  : " +str(val))
    #   print("\n\n")

      headers = info.keys()

      with open('Success.csv', 'a+') as ff1:
        writer = csv.DictWriter(ff1, fieldnames=headers)
        with open('Success.csv', 'r') as ff2:
          reader = [i for i in csv.DictReader(ff2)]
          if len(reader) == 0:
            writer.writeheader()
            writer.writerow(info)
          else:
            writer.writerow(info)

def main():
  get_data("inputCSV.csv")

main()

"""
Example "inputCSV.csv" format:

Tickers
MMM-US
AMC-AU
WRONG-22
BARN-CH
BAS-DE

"""
