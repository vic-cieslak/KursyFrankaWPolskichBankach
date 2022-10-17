import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio

# Because BPH is done a certain way we need to scrap the available times first
# then with second script we grab exchange rates


# date format is: "%Y-%m-%d"
api_url = "https://www.bph.pl/pi/api/currency/tw0/hours?date="
# this will return something like ["07:37","11:32"]


'''
WERSJA ASYNCHRONICZNA
'''

folder = 'dane/times/'

dates = pd.date_range(start="2021-03-12", end="2022-10-06").to_pydatetime().tolist()
# dates = pd.date_range(start="2021-08-28", end="2021-08-29").to_pydatetime().tolist()


async def fetch(session, link, folder_location, date):
    async with session.get(link, timeout=0, allow_redirects=True) as response:
        try:
            filename = folder + str(date) + '.json'
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
        for date in dates:
            print(date, 'started')

            link = api_url + date.strftime('%Y-%m-%d')
            await fetch(session, link, folder, date)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rfunc())
