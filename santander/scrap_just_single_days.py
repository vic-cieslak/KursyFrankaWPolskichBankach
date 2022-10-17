
# request doesnt need any cookies or headers


# 1. send first request to api_url with just date.

# 2. parse html to get

# <option value="118a/22">07:10</option>
# <option value="118b/22">10:10</option>
# <option selected="selected" value="118c/22">15:10</option>

# build a list / json with all availalbe values ['148a/09', '148b/09', '148c/09', 'etc']
# { '01-02-2008' : ['148a/09', '148b/09', '148c/09'] }

# 3. send additional requests to get the rest of the data

# 4. (not needed?) send request to with param &t-2397314={}

import pandas as pd
import requests
import time

# first send to
api_url = 'https://www.santander.pl/przydatne-informacje/kursy-walut?action=component_request.action&component.action=getRates&component.id=2397314&date-2397314=' # format -> 17-05-2022

# then send to
# api_url = 'https://www.santander.pl/przydatne-informacje/kursy-walut?action=component_request.action&component.action=getRates&component.id=2397314&t-2397314=153a/22' # 153a/22 is unique for whole system?


folder = 'html/'

dates = pd.date_range(start="2014-06-15", end="2022-10-07").to_pydatetime().tolist()

for date in dates:
  print(date, 'started')
  link = api_url + date.strftime('%d-%m-%Y')

  while True:
    try:
      res = requests.get(link, timeout=10)
      break
    except (
      ConnectionResetError,
      requests.exceptions.ReadTimeout,
      requests.exceptions.ConnectionError,
      requests.exceptions.ConnectTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue

  filename = folder + str(date) + '.html'

  with open(filename, 'wb') as f:
    f.write(res.content)
