import pandas as pd
import os
from bs4 import BeautifulSoup
from datetime import datetime

# pierwszy przemiał był potrzebny żeby znaleźć wszystkie
# dostępne godziny o których publikowane były dane
folder = 'dane/'


pliki = os.listdir(folder)

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
    list_of_currencies = [ i for i in df['Nazwa']['Nazwa']]
    frank_index = list_of_currencies.index('Frank szwajcarski')

    kupno = df['Dewizy']['Kupno'][frank_index]
    sprzedaz = df['Dewizy']['Sprzedaż'][frank_index]
    print(data, godzina, kupno, sprzedaz)
    dane.append([data, godzina, kupno, sprzedaz])


df = pd.DataFrame(dane)
df.to_excel('kredytbank_santander.xlsx')