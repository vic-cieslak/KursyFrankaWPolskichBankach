import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio

# LINK ŹRÓDŁO https://www.pkobp.pl/waluty/?pobierz_xls&date=09-08-2000

api_url = "https://www.pkobp.pl/waluty/?pobierz_xls&date="

folder = 'dane/'

dates = pd.date_range(start="2021-03-11", end="2022-10-03").to_pydatetime().tolist()

async def fetch(session, link, folderlocation, date):
    async with session.get(link, timeout=0, allow_redirects=True) as response:
        try:
            filename = folder + str(date) + '.xlsx'
            file = await aiofiles.open(filename, mode='wb')

            content = await response.content.read()

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
            link = api_url + date.strftime('%d-%m-%Y')

            await fetch(session, link, folder, date)

loop = asyncio.get_event_loop()
loop.run_until_complete(rfunc())
