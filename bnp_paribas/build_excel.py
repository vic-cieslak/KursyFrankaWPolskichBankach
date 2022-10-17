# 2. parse html to get ratesTable

# <option value="27400">401 08:45</option>
# <option selected="selected" value="27404">402 16:15</option>


import pandas as pd
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

# pierwszy przemiał był potrzebny żeby znaleźć wszystkie
# dostępne godziny/numery tabel kursowych o których publikowane były dane
folder = 'dane/'

pliki = os.listdir(folder)
pliki.sort()

# 1. extract
# data-configuration='{"defaultDate": "2004-01-06","showCalculator": "false"}'

# 2. extract datetime
# <option selected="selected" value="1584">2 12:40</option>

# 3. import html table as dataframe

def extract_date(soup_object):
  div = soup_object.find_all("div", {"class": "configuration"})[0]
  config_string = div.attrs["data-configuration"]
  config_dict = json.loads(config_string)
  date_string = config_dict['defaultDate']

  return date_string

dane = []

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    soup = BeautifulSoup(raw_data, 'html.parser')

    options = soup.find_all("option", selected=True)

    time_published = None
    for option in options:
      if 'BGŻ' in option.contents:
        continue
      else:
        time_published = option.contents[0].split(' ')[1]

    if not time_published:
      raise Exception('timestamp not found!')

    date_string = extract_date(soup)

    table = soup.find('table')

    df = pd.read_html(str(table))[0]

    frank_index = list(df['Kraj']).index('Szwajcaria')

    kupno = str(df['Kupno'][frank_index])
    sprzedaz = str(df['Sprzedaż'][frank_index])

    # values are missing dots
    # look like this -> 33213
    # we want them to look like this -> 3.3213
    kupno = kupno[:1] + '.' + kupno[1:]
    sprzedaz = sprzedaz[:1] + '.' + sprzedaz[1:]

    ts = date_string + ' ' + time_published
    print(ts, kupno, sprzedaz)
    dane.append([ts, kupno, sprzedaz])


sorted_dane = sorted(dane, key=lambda t: datetime.strptime(t[0], '%Y-%m-%d %H:%M'))
df = pd.DataFrame(sorted_dane)
df.to_excel('bnp_paribas.xlsx')