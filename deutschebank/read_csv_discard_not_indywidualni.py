import pandas as pd
from datetime import datetime

with open('data.csv', 'r') as f:
    lines = f.readlines()

dane = []
for line in lines:
  _, date, sprzedaz, kupno, *plik = line.split(' ')
  plik = " ".join(plik).strip()
  if 'ndywidual' in plik:
    dane.append([date, sprzedaz, kupno, plik])

new_dane = []
sorted_dane = sorted(dane, key=lambda dane: datetime.strptime(dane[0], '%Y-%m-%d'))
# sort by date
