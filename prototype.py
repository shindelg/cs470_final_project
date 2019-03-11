import urllib
import json
import sys
import requests
import csv
from collections import OrderedDict

# Auth
s = requests.Session()
s.auth = ('user', 'pw')

def get_data(name):
  print("About " + name + "\n")

# <http|s>://[<email>:<password>@]
# api.capitalcube.com/<resource>[/subresource...][?<parameters>]
  # print(requests.__version__)

  # get url response
  url = "https://api.capitalcube.com/companies/" +name
  resp = requests.get(url)

  if(resp.ok):
  
    data = resp.json() 

    # test column order
    # data = {"col0":0, "col1":1,"col2":2, "col3":3,"col4":4, "col5":5}
    
    info = OrderedDict(sorted(data.items(), key=lambda t : t[0]))

    # print whole data of a company
    for key, val in info.items():
      info[key] = val
      print(key + "  : " +str(val))
    print("\n\n")

    # write in csv
    with open('test.csv', 'w+') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(info.keys())
      writer.writerow(info.values())
  
def main(argv):
  get_data(argv)

main(sys.argv[1])
