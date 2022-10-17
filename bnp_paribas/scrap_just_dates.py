
# request doesnt need any cookies or headers


# 1. send first request to api_url with just date.


import pandas as pd
import requests
import time

# first send to
api_url = 'https://www.bnpparibas.pl/kursy-walut?action=component_request.action&component.action=changeRates&component.id=3485195'

# then send to

folder = 'html/'

dates = pd.date_range(start="2008-01-18", end="2022-10-07").to_pydatetime().tolist()

form_data = {
  'componentId': 3485195,
  'ratesDate': '', # 2022-10-06
  'bankCode': '',
}

for date in dates:
  print(date, 'started')
  date_string = date.strftime('%Y-%m-%d')
  form_data['ratesDate'] = date_string

  while True:
    try:
      res = requests.post(api_url, timeout=10, data=form_data)
      break
    except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue

  filename = folder + str(date) + '.html'

  with open(filename, 'wb') as f:
    f.write(res.content)
