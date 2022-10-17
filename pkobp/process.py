import pandas as pd

import os

# for xcel in dane
# load excel
# grab dewizy kupno, dewizy sprzedaz
# put to dataframe with date and time

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

dane = []
to_run_again = []

# CHF_INDEX = 8

for plik in pliki:

  # wczytaj pojedyńczy plik excel
  df = pd.read_excel('dane/' + plik)

  # złap date i godzine z pliku
  dt = df.columns[0][52:].split(',')[0]

  # wybierz kolumne z symbolami walut i sprawdź
  # w którym wierszu jest frank szwajcarski
  CHF_INDEX = list(df['Unnamed: 2']).index('CHF')

  data, godzina = dt.split(' ')

  # potwierdz że kolumna/format nie zmienia sie
  # na przestrzeni lat/plików
  assert 'Dewizy - kupno' == df['Unnamed: 3'][0]
  assert 'Dewizy - sprzedaż' == df['Unnamed: 5'][0]

  dewizy_kupno = df['Unnamed: 3'][CHF_INDEX]
  dewizy_sprzedaz = df['Unnamed: 5'][CHF_INDEX]

  print('dodaje' , df['Unnamed: 3'][CHF_INDEX], df['Unnamed: 5'][CHF_INDEX])
  dane.append((data, godzina, dewizy_kupno, dewizy_sprzedaz))

df = pd.DataFrame(dane)
df.to_excel('pkobp.xlsx')

