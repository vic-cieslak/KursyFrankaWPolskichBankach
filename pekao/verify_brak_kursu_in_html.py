import os
from bs4 import BeautifulSoup
import pandas as pd
folder = 'html/'

pliki = os.listdir('html/')
pliki.sort()

dane = []
for plik in pliki:
  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    # print('checking ', plik)
    # soup = BeautifulSoup(raw_data, 'html.parser')
    date = plik.split(' ')[0]
    if 'Brak kursu' in raw_data:
      dane.append([date, False, 'BRAK'])
      print('brak kursu!', plik)
    else:
      dane.append([date, True, 'Exists'])
      print('mam kurs')

df = pd.DataFrame(dane)
df.to_excel('pekao_missing.xlsx')