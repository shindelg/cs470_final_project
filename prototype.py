import urllib
import json
import sys
import requests
# from bs4 import BeautifulSoup as bs

# Auth
s = requests.Session()
s.auth = ('user', 'pw')

def get_data(name):
  print("About " + name + "\n")

  if "-" not in name:
    print("Incorrect format")
    print("Needs form: <ticker symbol>-<country code>")
    return(False)

# <http|s>://[<email>:<password>@]
# api.capitalcube.com/<resource>[/subresource...][?<parameters>]
  url = "https://api.capitalcube.com/companies/" +name
  resp = requests.get(url)

  info = dict()

  if(resp.ok):
    print(resp)

    #Try to open data, if not a json - failed query

    #need to check which exchange a company is in, retrieve id if not NASDQ
    #add check for if country code entered etc before sending request
    try:
      data = resp.json()
    except json.decoder.JSONDecodeError:
      print("Enter valid NASDQ or exchange ticker")
      return(False)

    # Print market cap
    print(data["marketCap"])

    # Print whole data of a company
    for key, val in data.items():
      info[key] = val
      print(key + "  : " +str(val))

    print("\n\n")
    return(True)

  # Get peers?
  # url2 = "https://api.capitalcube.com/companies/" +name +"/peers"
  # resp2 = requests.get(url2)

  # peers = dict()
  #
  # if(resp2.ok):
  #   print(resp2)
  #   data = resp2.json()

    # for key, val in data.items():
    #   peers[key] = val
    #   print(key)

#def main(argv):
#  get_data(argv)

#main(sys.argv[1])
