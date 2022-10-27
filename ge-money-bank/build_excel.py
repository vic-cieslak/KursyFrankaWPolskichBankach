import pandas as pd
import os
import json

folder = 'dane/'

pliki = os.listdir(folder)
pliki.sort()

dane = []

for plik in pliki:
  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    current_date = plik.split('.')[0]

    data = json.loads(raw_data)


    for pair in data:
      if pair['currency'] == 'CHF':
        wiersz = [current_date, pair['buying'], pair['selling']]
        print(wiersz)
        dane.append(wiersz)


df = pd.DataFrame(dane)
df.to_excel('ge-money-bank.xlsx')