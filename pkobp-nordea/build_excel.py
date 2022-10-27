import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

folder = 'dane/'

pliki = os.listdir(folder)
pliki.sort()

sorted_pliki = sorted(pliki, key=lambda t: datetime.strptime(t, '%d-%m-%Y %H:%M.html'))

dane = []

for plik in sorted_pliki:
  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    soup = BeautifulSoup(raw_data, 'html.parser')

    data = plik.split(' ')[0]
    godzina = plik.split(' ')[1].split('.')[0]


    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    # find where Swiss is in data table

    kraje = [ i for i in df[0]]
    swiss_index = kraje.index('SZWAJCARIA')

    kupno = float(df[4][swiss_index])
    sprzedaz = float(df[3][swiss_index])

    print(data, godzina, kupno, sprzedaz)
    dane.append([data, godzina, kupno, sprzedaz])


df = pd.DataFrame(dane)
df.to_excel('pkobp-nordea.xlsx')