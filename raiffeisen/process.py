import pandas as pd
import os
import json

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

l = []
for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    data_dict = json.loads(raw_data)
    dd = data_dict['rates'].keys()
    dd_list = list(dd)
    date = plik.split(' ')[0]
    try:
      last_ts = dd_list[-1]
      rates = data_dict['rates'][last_ts]
      for rate in rates:
        if rate['code'] == 'CHF':
          print(plik, '------  FOUND', rate['buy'], rate['sell'])
          l.append([date, last_ts, rate['buy'], rate['sell']])
    except IndexError:
      # l.append([date, '', 'brak danych', 'brak danych'])
      print(plik, ' ---- MISSING')


df = pd.DataFrame(l)
df.to_excel('raiffeisen.xlsx')