import pandas as pd
import os
import json
from bs4 import BeautifulSoup


# pierwszy przemiał był potrzebny żeby znaleźć wszystkie
# dostępne godziny o których publikowane były dane
folder = 'html/'


pliki = os.listdir(folder)
pliki.sort()


times_all = {}

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    soup = BeautifulSoup(raw_data, 'html.parser')

    options = soup.find_all("option")
    options_strings = []
    for option in options:
      options_strings.append(option.attrs['value'])

    file_datetime = soup.find_all("h3")[0].contents[3].contents[0]
    print(file_datetime, options_strings)
    times_all[file_datetime] = options_strings



with open('available_data.json', 'w') as f:
  data = json.dumps(times_all)
  f.write(data)