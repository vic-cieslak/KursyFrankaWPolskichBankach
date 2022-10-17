import pandas as pd
import requests
import time
import json
# first send to
api_url = 'https://www.bnpparibas.pl/kursy-walut?action=component_request.action&component.action=changeRates&component.id=3485195'

# then send to

folder = 'dane/'

with open('available_data.json', 'r') as f:
    tabele_kursowe = f.read()
    tabele_kursowe = json.loads(tabele_kursowe)

form_data = {
  'componentId': 3485195,
  'ratesTable': '', # 27376
  'bankCode': '',
}

for numer_tabeli_kursowej in tabele_kursowe:
  print(numer_tabeli_kursowej, 'started')
  form_data['ratesTable'] = numer_tabeli_kursowej

  while True:
    try:
      res = requests.post(api_url, timeout=10, data=form_data)
      break
    except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue

  filename = folder + numer_tabeli_kursowej + '.html'

  with open(filename, 'wb') as f:
    f.write(res.content)
