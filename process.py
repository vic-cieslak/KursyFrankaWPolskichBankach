import pandas as pd
import os

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

def extract_kupno_sprzedaz_CHF(dataframe):
    kupno = df[df.columns[0]][2].split(';')[5]
    sprzedaz = df[df.columns[0]][2].split(';')[4]

    return kupno, sprzedaz

l = []
to_run_again = []
for plik in pliki:
  data = plik.split('.')[0]
  df = pd.read_csv('dane/' + plik)
  try:
    kupno, sprzedaz = extract_kupno_sprzedaz_CHF(df)
  except KeyError:
    sprzedaz = 'BRAK'
    kupno = 'BRAK'
    print('brak', data)
    to_run_again.append(data)
  print('appending', data)
  l.append((data, kupno, sprzedaz))


df = pd.DataFrame(l)
df.to_excel('mbank.xlsx')
