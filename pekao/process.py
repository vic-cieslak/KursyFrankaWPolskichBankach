import xml.etree.ElementTree as ET
import os
import xmltodict
import pandas as pd

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()


dane = []

for plik in pliki:
  # print('loading, ', plik)
  tree = ET.parse(folder + plik)
  root = tree.getroot()
  to_string  = ET.tostring(root, encoding='UTF-8', method='xml')
  data_dict = xmltodict.parse(to_string)
  data_publikacji = data_dict['tabela_kursow']['data_publikacji'] # format -> '17.03.2014 07:00'
  found_swiss = False
  for position in data_dict['tabela_kursow']['pozycja']:
    if position['kraj'] == 'Szwajcaria':
      print('appending',data_publikacji, position['kupno'], position['sprzedaz'])
      dane.append([data_publikacji, position['kupno'], position['sprzedaz']])
      found_swiss = True


  if not found_swiss:
    print('!! not found for date: ', data_publikacji)

df = pd.DataFrame(dane)
df.to_excel('pekao.xlsx')

# normalize format
# existing_in_html_new_format = []
# for date in existing_in_html:
#   date = plik.split(' ')[0]
#   date = datetime.strptime(date, '%Y-%m-%d')
#   date = date.strftime('%d.%m.%Y')
#   existing_in_html_new_format.append(date)