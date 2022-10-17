import json
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import time
import os

api_url = 'https://www.pekao.com.pl/.currencies/file?type=XML&source=PEKAO&date={date}&table={table_id}'

headers = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Windows; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
}

folder = 'dane/'

with open('missing.json', 'r') as f:
  missing_dates = f.read()
  missing_dates = json.loads(missing_dates)

found_missing = []

for date in missing_dates[::-1]:
  # date_string = date.strftime('%Y-%m-%d')
  url = api_url.format(date=date, table_id=1)
  print(date, 'started')
  while True:
    try:
      res = requests.get(url, timeout=10, headers=headers)
      break
    except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue

  filename = folder + str(date) + '1' + '.xml'

  file_exists = os.path.isfile(filename)

  if file_exists:
    print('File already exists!')

  with open(filename, 'wb') as f:
    f.write(res.content)

  try:
    tree = ET.parse(filename)
    # we got a correct response yupi
    print('got valid XML, adding to found_missing')
    found_missing.append(date)
  except:
    print('not valid XML, removing...')
    os.remove(filename)
  # time.sleep(3)


#-------------------

# for found in found_missing:
#   try:
#     missing_json.remove(found)
#     print('removed ', found)
#   except ValueError:
#     pass


# with open('missing.json', 'w') as f:
#   f.write(json.dumps(missing_json))



missing_non_weekends = []

for date in dates:
  dt = datetime.strptime(date, '%d.%m.%Y')
  print(dt.weekday())
  # if dt.weekday() > 4:
  #   print(dt, 'is weekend')

dt = datetime.strftime('%d.%m.%Y')


missing_data = []
# we have data for

for date in dates_non_weekends_strings:
  if date not in dates:
    print(date, ' missing')

