import pandas as pd
import os
import json
from datetime import datetime

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

dane = {
  'date': [],
  'time': [],
  'moneySale': [],
  'moneyBuy': [],
  'foreignExchangeBuy': [],
  'foreignExchangeSale': [],
}

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    data_list = json.loads(raw_data)
    date = plik.split(' ')[0]

    chf_found = False

    for element in data_list:
      if 'items' in element:
        for another_element in element['items']:
          if another_element['country'] == 'Szwajcaria':
            # cut last 3 zeros no idea why
            # they are adding them
            # but otherwise year turns out to be 5000 something
            epoch = int(str(element['timeStamp'])[:-3])
            ts = datetime.fromtimestamp(epoch).strftime("%I:%M:%S")
            date_from_ts = datetime.fromtimestamp(epoch).strftime("%Y-%m-%d")
            if date_from_ts in dane['date']:
              continue
            print('appending', date, another_element['moneySale'], another_element['moneyBuy'])
            dane['date'].append(date)
            dane['time'].append(ts)
            dane['moneySale'].append(another_element['moneySale'])
            dane['moneyBuy'].append(another_element['moneyBuy'])
            dane['foreignExchangeBuy'].append(another_element['foreignExchangeBuy'])
            dane['foreignExchangeSale'].append(another_element['foreignExchangeSale'])
            chf_found = True

    if chf_found == False:
      # day is sunday or saturday, skip
      datetime_object = datetime.strptime(date, '%Y-%m-%d')
      if datetime_object.weekday() == 5:
        pass
      elif datetime_object.weekday() == 6:
        pass
      else:
        print('couldn\'t find CHF for ', date, '!!')


df = pd.DataFrame(dane)
df.to_excel('millenium.xlsx')