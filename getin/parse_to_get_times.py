from re import L
import pandas as pd
import os
import json
from bs4 import BeautifulSoup


# pierwszy przemiał był potrzebny żeby znaleźć wszystkie
# dostępne godziny o których publikowane były dane
folder = 'dane_pierwszy_przemiał_późniejsza_godzina/'


pliki = os.listdir(folder)
pliki.sort()


times_all = {}

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    data_json = json.loads(raw_data)
    soup = BeautifulSoup(data_json['table'], 'html.parser')
    options = soup.find_all("option")

    times = []
    date_string = plik.split(' ')[0]
    times_all[date_string] = []
    for option in options:
      if 'value' in option.attrs:
        if option.attrs['value']:
          times_all[date_string].append(option.attrs['value'])
    print(times_all[date_string])


with open('available_data.json','w') as f:
  data = json.dumps(times_all)
  f.write(data)