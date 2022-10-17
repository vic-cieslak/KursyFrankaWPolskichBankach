import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio
import os
import json
import requests
from datetime import datetime

# date format is: "%Y-%m-%d"
api_url = "https://www.bph.pl/pi/api/currency/tw0/currencies?date="

folder = 'dane/rates/'
times_folder = 'dane/times'

# this badly named variable means
#         "at this date -> 2021-03-12 this time is available -> 07:37 "
times_and_dates = {}


def load_times():

    pliki = os.listdir(times_folder)
    pliki.sort()
    for plik in pliki:
        date = plik.split(' ')[0]
        # print('doing  ', date)
        with open(times_folder + '/' + plik, 'r') as f:
            times = f.read()
            #times = json.loads(f.read())
            print(times)
            if times:
                # we choose the earliest one - so around 7-9am
                # time_available = times[0]
                times_and_dates[date] = json.loads(times)


def start_from_later():
    from_dt = datetime.strptime('2013-10-27', '%Y-%m-%d')
    new_times_and_dates = {}
    for key, values in times_and_dates.items():
        #print(key)
        dt = datetime.strptime(key, '%Y-%m-%d')
        if dt > from_dt:
            print(dt)
            new_times_and_dates[key] = values

    times_and_dates = new_times_and_dates

# dates = pd.date_range(start="2003-01-15", end="2021-03-12").to_pydatetime().tolist()
print('loading times')
load_times()
print('starting to fetch')



async def fetch(session, link, date, time):
    async with session.get(link, timeout=0, allow_redirects=True) as response:
        try:
            filename = folder + str(date) + ' ' + time + '.json'
            file = await aiofiles.open(filename, mode='w')
            content = await response.text()
            await file.write(content)
            await file.close()
            print(date, 'ended')
        except FileNotFoundError as e:
            print(date, '---ERROR---')
            print(e)


async def rfunc():
    async with aiohttp.ClientSession() as session:
        for date, times in times_and_dates.items():
            from_dt = datetime.strptime('2021-06-29', '%Y-%m-%d')
            dt = datetime.strptime(date, '%Y-%m-%d')
            if dt < from_dt:
                print('skipping ', dt)
                continue

            for time in times:
                print(date, time, 'started')
                formatted_time = requests.utils.quote(time)
                link = api_url + date + ' ' + formatted_time
                await fetch(session, link, date, time)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rfunc())


