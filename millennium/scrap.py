import pandas as pd
import asyncio
import aiohttp
import aiofiles
import asyncio


# https://www.bankmillennium.pl/o-banku/serwis-ekonomiczny/kursy-walut

# date format is: "%d-%m-%Y"
api_url = "https://www.bankmillennium.pl/portal-apps/getFxRates?date={date}&language=pl"

# NEED TO PASS CORRECT COOKIES (JUST COPY FROM WEB BROWSER)
cookies = {
  'PSESSIONID': '',
  'LB_bank_cookie': '',
  '_snrs_p': '',
  '_snrs_puuid':  '',
  '_snrs_sa': '',
  '_snrs_sb':'',
  '_snrs_uuid': '',
}

headers = {
  'Authorization': ''
}

folder = 'dane/'

dates = pd.date_range(start="2021-03-15", end="2022-10-03").to_pydatetime().tolist()

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

    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        for date in dates:
            print(date, 'started')
            link = api_url.format(date=date.strftime('%d-%m-%Y'))
            await fetch(session, link, folder, date)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rfunc())
