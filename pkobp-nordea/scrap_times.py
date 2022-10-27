import pandas as pd
import time
import requests
import json
# LINK ŹRÓDŁO https://www.pkobp.pl/waluty-archiwumexn/

api_url = "https://www.pkobp.pl/waluty/?hours_archive_exn=&date="#22-10-2014

# next request should go to
#https://www.pkobp.pl/waluty/?rates_archive_exn=&time=14:36&date=22-10-2014

folder = 'dane/'
                           #                  31.10.2014
dates = pd.date_range(start="2008-01-01", end="2014-10-31").to_pydatetime().tolist()


for date in dates:
  print('fetching ', date)
  datetime_string = date.strftime('%d-%m-%Y')
  url = api_url + datetime_string
  while True:                                                                                 # 2004-01-03
    try:
      res = requests.get(url, timeout=10)
      break
    except (
      ConnectionResetError,
      requests.exceptions.ReadTimeout,
      requests.exceptions.ConnectionError,
      requests.exceptions.ConnectTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue


  with open('available_dates.csv', 'a') as f:
    values = json.loads(res.content)
    dates = ' '.join(values['result'])
    string_to_write = datetime_string + ' ' + dates + '\n'
    print('writing ', string_to_write)
    f.write(string_to_write)