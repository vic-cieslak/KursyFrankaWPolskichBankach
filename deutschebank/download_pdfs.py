import json
import requests

BASE_URL = 'https://country.db.com'
DOWNLOAD_FOLDER = 'dane/'

def extract_timestamp(link):
  pass
  # extract datetime string that can either
  # be in format 2003-11-03 or 12.09.2018

  # split at .pdf? at grab last X characters?
  return '2003-11-03'

with open('links_to_pdfs.json', 'r') as f:
    print('reading links data from json..')
    data = f.read()
    pdf_links = json.loads(data)


for link in pdf_links:
  # timestamp = extract_timestamp(link)

  print('fetching ', link)
  response = requests.get(BASE_URL + link)
  filename = link.replace('/',' ')
  with open(DOWNLOAD_FOLDER + filename, 'wb') as f:
    f.write(response.content)
