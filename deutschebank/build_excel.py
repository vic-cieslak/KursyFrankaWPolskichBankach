import pandas as pd
from datetime import datetime



with open('data.csv', 'r') as f:
  data = f.readlines()

dane = []

for line in data:
  lines = line.split(' ')
  data = lines[1]
  sprzedaz = lines[2]
  kupno = lines[3]

  plik = ' '.join(lines[4:])


  try:
    sprzedaz = float(sprzedaz)
  except:
    pass

  try:
    kupno = float(kupno)
  except:
    pass

  # dane.append([data, sprzedaz, kupno, '', plik])
  dane.append([data, sprzedaz, kupno])

df = pd.DataFrame(dane)
# df[3] = df[1] - df[2]


sorted_dane = sorted(dane, key=lambda t: datetime.strptime(t[0], '%Y-%m-%d'))
df = pd.DataFrame(sorted_dane)
df.to_excel('deutschebank.xlsx')