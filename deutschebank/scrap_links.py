import requests
from bs4 import BeautifulSoup
import json

main_links = [
  'https://country.db.com/poland/kursy-walut/', # 2022
  'https://country.db.com/poland/kursy-walut/2021',
  'https://country.db.com/poland/kursy-walut/2020',
  'https://country.db.com/poland/kursy-walut/2019',
  'https://country.db.com/poland/kursy-walut/2018',
  'https://country.db.com/poland/kursy-walut/2017',
  'https://country.db.com/poland/kursy-walut/2016',
  'https://country.db.com/poland/kursy-walut/2015',
  'https://country.db.com/poland/kursy-walut/2014',
  'https://country.db.com/poland/kursy-walut/2013',
  'https://country.db.com/poland/kursy-walut/2012',
  'https://country.db.com/poland/kursy-walut/2011-2009',
  'https://country.db.com/poland/kursy-walut/2008-2006',
  'https://country.db.com/poland/kursy-walut/2005-2003',
]

l = []

def extract_pdf_links(response):
  soup = BeautifulSoup(response.content, 'html.parser')

  for link in soup.find_all('a', href=True):
      if link['href'].lower().endswith(".pdf"):
          l.append(link['href'])
          # print(link['href'])


for link in main_links:
  print('fetching ', link)
  response = requests.get(link)
  pdf_links = extract_pdf_links(response)

with open('links_to_pdfs.json', 'w') as f:
  print('saving to file')
  f.write(json.dumps(l))


