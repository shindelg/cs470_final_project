import json
import sys
import csv
import pandas as pd
from forex_python.converter import CurrencyRates
from datetime import datetime


def main():
  now= datetime.now()
  print(now.strftime('%Y-%m-%d %H:%M:%S'))

  c = CurrencyRates()
  currencyData = c.get_rates('USD')
  df = pd.DataFrame.from_dict(currencyData, orient='index')
  df.columns = ['ExRate']
  df.to_csv('CurrencyConverter.csv', index_label='Currency')

  print("Currency csv created")

main()
