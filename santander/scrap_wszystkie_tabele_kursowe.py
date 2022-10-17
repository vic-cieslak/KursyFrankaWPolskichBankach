import pandas as pd
import requests
import time
import json
from bs4 import BeautifulSoup


# then send to
api_url = 'https://www.santander.pl/przydatne-informacje/kursy-walut?action=component_request.action&component.action=getRates&component.id=2397314&t-2397314=' # 153a/22 is unique for whole system?

# FULL URL
# api_url = 'https://www.santander.pl/przydatne-informacje/kursy-walut?action=component_request.action&component.action=getRates&component.id=2397314&t-2397314=153a/22' # 153a/22 is unique for whole system?

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


for date, tabele_kursowe in available_data.items():

  for id_tabeli_kursowej in tabele_kursowe:
    link = api_url + id_tabeli_kursowej
    print(id_tabeli_kursowej, ' started')
    response = get_data(link)
    time_of_data = extract_timestamp(response)
    timestamp = date + ' ' + time_of_data
    print(id_tabeli_kursowej, 'saving')
    save_data(response, timestamp)
