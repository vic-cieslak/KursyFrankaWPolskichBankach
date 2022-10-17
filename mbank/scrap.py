import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio

# https://www.mbank.pl/ajax/currency/getCSV/?id=1&date=2022-04-10%2016:30:00&lang=pl
api_url = "https://www.mbank.pl/ajax/currency/"

folder = 'dane/'
dates = pd.date_range(start="2004-01-01", end="2022-04-10").to_pydatetime().tolist()

async def fetch(session, link, folderlocation, date, time_id):
    async with session.get(link, timeout=0, allow_redirects=True) as response:
        try:
            filename_date = date.strftime('%Y-%m-%d')
            filename = folder + filename_date + ' ' + str(time_id) + '.csv'
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
            # date = date.date()
            date_string = date.strftime('%Y-%m-%d')
            print(date_string, 'started')
            # tutaj do sterowania sciagania danej godziny uzywany jest
            # id=0 to 8:00
            # id=1 to nastepna godzina
            # id=2 to przewaznie 16:00
            link_id_0 = api_url + "getCSV/?id=1&date={} 16:30:00&lang=pl".format(date_string)
            # link_id_1 = api_url + "getCSV/?id=1&date={} 16:00:00&lang=pl".format(date_string)

            await fetch(session, link_id_0, folder, date, "16:30")
            # await fetch(session, link_id_1, folder, date, "16:30")


loop = asyncio.get_event_loop()
loop.run_until_complete(rfunc())
