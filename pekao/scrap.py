
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import time
import os

# table id is 1 or 2 (possible there is 3 somewhere, but its hard to check)
# date format is 2022-10-03
api_url = 'https://www.pekao.com.pl/.currencies/file?type=XML&source=PEKAO&date={date}&table={table_id}'
# https://www.pekao.com.pl/.currencies/file?type=XML&source=PEKAO&date=2010-04-06&table=1

# could try with table_id=3 to see if some data is not hidden there

# then send to

folder = 'dane/'

dates = pd.date_range(start="2004-01-01", end="2022-10-07").to_pydatetime().tolist()

added = []

for date in dates:
  print(date, 'started')

  date_string = date.strftime('%Y-%m-%d')
  url = api_url.format(date=date_string, table_id=1)
  # print(url)
  # grab table 3
  while True:
    try:
      res = requests.get(url, timeout=10, )
      break
    except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
      print('request failed, trying again in 3s')
      time.sleep(3)
      continue

  filename = folder + str(date) + '1' + '.xml'
  file_exists = os.path.isfile(filename)

  with open(filename, 'wb') as f:
    f.write(res.content)

  # check if response is correct
  try:
    tree = ET.parse(filename)
    os.path.isfile(filename)
    if not file_exists:
      print('file doesnt exists', date_string)
      added.append(date_string)
  except:
    os.remove(filename)

  # grab table 4
  # url = api_url.format(date=date_string, table_id=4)
  # while True:
  #   try:
  #     res = requests.get(url, timeout=10, )
  #     break
  #   except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
  #     print('request failed, trying again in 3s')
  #     time.sleep(3)
  #     continue
  # filename = folder + str(date) + '4' + '.xml'

  # with open(filename, 'wb') as f:
  #   f.write(res.content)

