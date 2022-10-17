import pandas as pd
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

folder = 'dane_pierwszy_przemiał_późniejsza_godzina/'

pliki = os.listdir('dane_pierwszy_przemiał_późniejsza_godzina/')

pliki.sort()

dane = []

for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    data_json = json.loads(raw_data)
    date = plik.split(' ')[0]
    soup = BeautifulSoup(data_json['table'], 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    # find where Swiss is in data table
    swiss_index = list(df[0]).index('Szwajcaria')
    kupno = df[2][swiss_index]
    sprzedaz = df[3][swiss_index]
    print(date, kupno, sprzedaz)
    dane.append([date, kupno, sprzedaz])


df = pd.DataFrame(dane)

df.to_excel('getin.xlsx')