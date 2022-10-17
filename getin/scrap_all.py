import pandas as pd
import requests
import time
import os
import json

api_url = "https://www.getinbank.pl/api/modules/exchange-rates/changeDate"

# TODO YOU NEED TO ADD CORRECT TOKENS/HEADERS/COOKIES HERE

cookies =  {
		"comm100_guid2_100020000": "",
		"salesmore_affId": "GB",
		"salesmore_tdpeh": "kampania strona wnioski.getinbank.pl",
		"user_session": "",
		"XSRF-TOKEN": ""
}

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pl",
    "Connection": "keep-alive",
    "Content-Length": "103",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "",
    "DNT": "1",
    "Host": "www.getinbank.pl",
    "Origin": "https://www.getinbank.pl",
    "Referer": "https://www.getinbank.pl/kursy-walut",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (X11; Windows; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "X-CSRF-TOKEN": "",
    "X-Requested-With": "XMLHttpRequest",
}

form_data = {
    # "dateTime":  # format is -> 2022-09-15 or "2022-09-19+10:00:59"
    "type": "credits", # credits
    "locale": "pl",
    "_token": ""
}

folder = 'dane/'


# to send next request dateTime	"2022-09-19+10:00:59" needs to be passed

session = requests.Session()
session.headers = headers

def save_data(response_object, ts):
  filename = folder + ts + '.json'

  with open(filename, 'wb') as f:
      f.write(response_object.content)


def get_data(form_data):
  while True:
      try:
          res = session.post(
              api_url,
              timeout=10,
              data=form_data,
              cookies=cookies
          )
          break
      except (ConnectionResetError, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
          print('request failed, trying again in 3s')
          time.sleep(3)
          continue
  return res

with open('available_data.json', 'r') as f:
  available_data = json.loads(f.read())


for date_string, times in available_data.items():
  print('fetching ', date_string)

  if times:
    for time_ in times:
      ts = date_string + '+' + time_
      form_data['dateTime'] = ts
      res = get_data(form_data)
      print('saving ', ts)
      save_data(res, ts)
  else:
    # just get one day
    form_data['dateTime'] = date_string
    res = get_data(form_data)
    save_data(res, date_string)
    print('saving ', date_string)





