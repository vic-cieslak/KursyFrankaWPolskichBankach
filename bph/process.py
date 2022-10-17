import pandas as pd
import os
import json

times_folder = 'dane/times'

# this badly named variable means
#         "at this date -> 2021-03-12 this time is available -> 07:37 "
times_and_dates = {}

# def load_times():

#   pliki = os.listdir(times_folder)
#   pliki.sort()
#   for plik in pliki:
#     date = plik.split(' ')[0]
#     # print('doing  ', date)
#     with open(times_folder + '/' + plik, 'r') as f:
#       times = json.loads(f.read())
#       if times:
#         # time_available = times[0] # we choose the earliest one - so around 7-9am
#         times_and_dates[date] = times

folder = 'dane/rates/'

pliki = os.listdir('dane/rates')
pliki.sort()

# load_times()

l = []
for plik in pliki:

  with open(folder + plik, 'r') as f:
    raw_data = f.read()
    data_dict = json.loads(raw_data)
    timestamp = plik.split('.')[0]
    for pair in data_dict:
      if pair['currency'] == 'CHF':
        l.append([timestamp, pair['buying'], pair['selling']])


df = pd.DataFrame(l)
df.to_excel('bph.xlsx')
###
### Problem with this data is that rates dict has times for different rates [wtf]

