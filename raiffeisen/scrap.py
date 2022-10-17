import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio


# date format is: "%Y-%m-%d"
api_url = "https://www.rbinternational.com.pl/rest/rates/?type=kursywalut&range=all&date="

folder = 'dane/'

dates = pd.date_range(start="2021-03-11", end="2022-10-07").to_pydatetime().tolist()

async def fetch(session, link, folderlocation, date):
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

loop = asyncio.get_event_loop()
loop.run_until_complete(rfunc())
