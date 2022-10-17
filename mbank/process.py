import pandas as pd
import os

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

def extract_kupno_sprzedaz_CHF(df):
    if 'Szwajcaria' in df[df.columns[0]][3]:
      row_number = 3
    elif 'Szwajcaria' in df[df.columns[0]][2]:
      row_number = 2
    else:
      raise Exception('Szwajcaria row not found')

    kupno = df[df.columns[0]][row_number].split(';')[4]
    sprzedaz = df[df.columns[0]][row_number].split(';')[5]

    return kupno, sprzedaz

def extract_timestamp(df):
  ts = df.columns[0][17:]
  ts = ts.strip(';')
  if 'mBanku S.A.' in ts:
    ts = df[df.columns[0]][0][17:]
    ts = ts.strip(';')

  return ts

def run():
  data = {
    #  example
    # '2008-08-08 09:15:00': [1.9537, 2.0519],
    # '2008-08-08 08:00:00': [1.9537, 2.0519],
  }
  # to_run_again = []

  for plik in pliki:
    df = pd.read_csv('dane/' + plik)
    kupno, sprzedaz = extract_kupno_sprzedaz_CHF(df)
    timestamp = extract_timestamp(df)
    print(timestamp, kupno, sprzedaz)
    data[timestamp] = [kupno, sprzedaz]

  df = pd.DataFrame.from_dict(data, orient='index')
  df.to_excel('mbank.xlsx')


# verify
def verify_swiss_on_line_5():
  for plik in pliki:
    path = 'dane/' + plik
    with open(path, 'r') as f:
      lines = f.readlines()
      print('checking ', plik)
      assert 'Szwajcaria' in lines[4]


def clean():
  for plik in pliki:
    with open('dane/' + plik, 'r') as f:
      lines = f.readlines()
      if len(lines) < 5:
        print('removing,', plik)
        # os.remove('dane/' + plik)
