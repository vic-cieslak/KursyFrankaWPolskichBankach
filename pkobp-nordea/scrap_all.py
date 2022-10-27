import requests

dates_dict = {}
# We open the source file and get its lines
with open('available_dates_clean.csv', 'r') as inp:
    lines = inp.readlines()
    for line in lines:
      line = line.strip()
      date, *times = line.split(' ')
      dates_dict[date] = times

folder = 'dane/'

  # 31-10-2014
for date, times in dates_dict.items():

  for time in times:
    print('fetching ', date, ' ', time)

    api_url = f"https://www.pkobp.pl/waluty/?rates_archive_exn=&time={time}&date={date}"

    while True:
      try:
        res = requests.get(api_url, timeout=10)
        break
      except (
        ConnectionResetError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout):
        print('request failed, trying again in 3s')
        time.sleep(3)
        continue

    filename = folder + date + ' ' + time + '.html'
    with open(filename, 'wb') as f:
      print('writing ', filename)
      f.write(res.content)
    # write response to file