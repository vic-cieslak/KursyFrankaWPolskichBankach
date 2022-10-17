# 2. parse html to get ratesTable

# <option value="27400">401 08:45</option>
# <option selected="selected" value="27404">402 16:15</option>

# ratesTable:
# build a list / json with all availalbe valeues ['27400', '27404',  'etc']

# 3. send additional requests to get the rest of the data using ratesTable

# 4. send request to with param

# this thing needs form data

import pandas as pd
import os
import json
from bs4 import BeautifulSoup


# pierwszy przemiał był potrzebny żeby znaleźć wszystkie
# dostępne godziny/numery tabel kursowych o których publikowane były dane
folder = 'html/'

pliki = os.listdir(folder)
pliki.sort()


tabele_kursowe_idki = []

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    soup = BeautifulSoup(raw_data, 'html.parser')

    options = soup.find_all("option")
    options_strings = []
    for option in options:
      options_strings.append(option.attrs['value'])

    try:
      options_strings.remove('bnp')
    except ValueError:
      pass
    print(options_strings)
    tabele_kursowe_idki.extend(options_strings)


with open('available_data.json', 'w') as f:
  tabele_kursowe_idki = list(set(tabele_kursowe_idki))
  try:
    options_strings.remove('bnp')
  except ValueError:
    pass
  try:
    options_strings.remove('bgz')
  except ValueError:
    pass

  tabele_kursowe_idki.sort()
  data = json.dumps(tabele_kursowe_idki)
  f.write(data)