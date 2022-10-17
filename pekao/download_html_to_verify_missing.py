

# !! THIS SCRIPT WILL PRODUCE INVALID OUTPUT
# we hit a link
# but it says "Braku kursu"
# because we manually need to select different input date
#







import pandas as pd
import requests
import time

folder = 'html/'

dates = pd.date_range(start="2017-09-06", end="2022-10-07").to_pydatetime().tolist()


for date in dates:
  print('fetching ', date)
  datetime_string = date.strftime('%Y-%m-%d')
  url = f"https://www.pekao.com.pl/kursy-walut/lista-walut.html?nbpDate=2022-10-11&pekaoDate={datetime_string}&debitCardDate=2022-10-11&reutersDate=undefined&mortgageDate=2022-10-11&customerSegment=CORPO#-kursy-walut-banku-pekao-sa" # 2004-01-01
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

  filename = folder + str(date) + '.html'

  with open(filename, 'wb') as f:
    f.write(res.content)