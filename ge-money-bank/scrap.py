import requests
import json
import pandas as pd

dates = pd.date_range(start="2021-08-28", end="2022-10-27").to_pydatetime().tolist()


BASE_URL = "https://www.bph.pl/pi/api/currency/twge/currencies?date="#2022-10-10

folder = 'dane/'

for date in dates:
  date_string = date.strftime('%Y-%m-%d')
  api_url = BASE_URL + date_string

  res = requests.get(api_url)
  if res.content.decode():
    print(res.content)
    # print(json.loads(res.content))
    filename = folder + date_string + '.json'

    with open(filename, 'wb') as f:
      f.write(res.content)
  else:
    print('no data for', date_string)