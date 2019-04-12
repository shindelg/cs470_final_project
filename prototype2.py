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

def get_data(companies):

  print("About " + companies + "\n")

  compList = [x.strip() for x in companies.split(",")]

  for name in compList:
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

      #need to check which exchange a company is in, retrieve id if not NASDQ
      #add check for if country code entered etc before sending request
      try:
        data = resp.json()
      except json.decoder.JSONDecodeError:
        print("Enter valid NASDQ or exchange ticker")
        return

      # data = resp.json()
      info = OrderedDict(sorted(data.items(), key=lambda t : t[0]))

      for key, val in info.items():
        info[key] = val
        print(key + "  : " +str(val))
      print("\n\n")

      # Create a csv
      # Possible issue: same company is added as a new row if run again
      with open('test2.csv', 'a+') as csvfile:
        headers = info.keys()
        # writer.writeheader()
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        with open('test2.csv', 'r') as f:
          reader = [i for i in csv.DictReader(f)]
          if len(reader) == 0:
            writer.writeheader()
          if name in reader:
            continue
          else:
            writer.writerow(info)
          

def main(argv):
  get_data(argv)

main(sys.argv[1])