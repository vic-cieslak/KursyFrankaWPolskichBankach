import pandas as pd
import requests
import time

api_url = "https://www.getinbank.pl/api/modules/exchange-rates/changeDate"
# TODO YOU NEED TO ADD CORRECT TOKENS/HEADERS/COOKIES HERE

cookies =  {
    "_gcl_au": "1.1.1469532936.1665650482",
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

dates = pd.date_range(start="2004-12-01",
                      end="2022-10-08").to_pydatetime().tolist()

# first round is to download first hour of the day
# second round need to parse times
# to send next request dateTime	"2022-09-19+10:00:59" needs to be passed
folder = 'dane/'

session = requests.Session()
session.headers = headers
# session.cookies = cookies
for date in dates:
    print(date, 'started')
    date_string = date.strftime('%Y-%m-%d')
    # date_string = "2022-09-08+23:59:59"
    # date_string = "2022-09-15+23:59:59"
    form_data['dateTime'] = date_string
    print(date_string)
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

    filename = folder + str(date) + '.json'

    with open(filename, 'wb') as f:
        f.write(res.content)
