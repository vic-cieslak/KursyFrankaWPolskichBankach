import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup


# then send to
api_url = 'https://www.santander.pl/przydatne-informacje/kursy-archiwalne-kb?action=component_request.action&component.action=getRates&component.id=1980576&time-1980576={}&date-1980576={}'

# FULL URL
# api_url = 'https://www.santander.pl/przydatne-informacje/kursy-archiwalne-kb?action=component_request.action&component.action=getRates&component.id=1980576&time-1980576=10:15&date-1980576=15-10-2013' # 153a/22 is unique for whole system?



output_folder = 'dane/'


session = requests.Session()

def save_data(response_object, ts):
  filename = output_folder + ts + '.html'

  with open(filename, 'wb') as f:
      f.write(response_object.content)


def get_data(url):
  while True:
      try:
          res = session.post(
              url,
              timeout=10,
          )
          break
      except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
          print('request failed, trying again in 3s')
          time.sleep(3)
          continue
  return res

def extract_timestamp(response):
  soup = BeautifulSoup(response.content, 'html.parser')
  timestamp = soup.find_all("option", selected=True)[0].contents[0]
  return timestamp

with open('available_data.json', 'r') as f:
    available_data = f.read()
    available_data = json.loads(available_data)


for date, dostepne_godziny in available_data.items():

  for godzina in dostepne_godziny:
    link = api_url.format(godzina, date)
    print(date, godzina, ' started')
    response = get_data(link)
    time_of_data = extract_timestamp(response)
    timestamp = date + ' ' + time_of_data
    print(date, godzina, 'saving')
    save_data(response, timestamp)
