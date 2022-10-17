import camelot
import tabula
import os
import datefinder

folder = "dane/"

pliki = os.listdir(folder)

# filtruj na indywidualne
pliki = [p for p in pliki if 'ndywidu' in p]

def find_CHF_line(string_table):
  n = 0
  for line in string_table:
    n += 1
    if 'mieszkan' in line:
      #   sprzedaz kupno   kurs bazowy
      # CHF 4,2544 4,3608 4,3076
      break
      # return line

  for line in string_table[n:]:
    if 'CHF' in line:
      #   sprzedaz kupno   kurs bazowy
      # CHF 4,2544 4,3608 4,3076
      return line

  return None

def parse_with_tabula(file_path):
  tables = tabula.read_pdf(file_path, pages="all")
  data_key = tables[0].keys()[0]

  if len(tables) == 3:
    kraje = [k for k in tables[1]['Kraj']]
    index_of_chf = kraje.index('Szwajcaria')
    sprzedaż = tables[1]['sprzedaż'][index_of_chf]
    kupno = tables[1]['kupno'][index_of_chf]
    return kupno, sprzedaż

  try:
    line = find_CHF_line(tables[0][data_key])
  except TypeError:
    countries = [c for c in tables[0][data_key]]
    index_of_chf = countries.index('Szwajcaria')
    assert 'kupno' in tables[0]['Unnamed: 2'][1]
    assert 'sprzedaż' or 'sprzedaz' in tables[0]['Dewizy'][1]
    sprzedaż = tables[0]['Dewizy'][index_of_chf]
    kupno = tables[0]['Unnamed: 2'][index_of_chf]
    return kupno, sprzedaż

  sprzedaż = line.split(' ')[1]
  kupno = line.split(' ')[2]

  return kupno, sprzedaż


def make_a_number(string_number):
  if isinstance(string_number, float):
    return string_number

  string_number = string_number.replace(',', '.')

  if '-' in string_number:
    return 'BRAK DANYCH'

  return float(string_number)

dane = []


# index number
# idx, x in enumerate(xs)
for id, plik in enumerate(pliki):
  # if id < 414:
  #   print('skipping', id)
  #   continue
  if plik == ' poland documents exchange-rates 2014 11 klienci_indywidualni_i_biznesowi_2014-11-21.pdf':
    with open('data.csv', 'a') as f:
      data = str(id) + ' ' +  "2014-11-21" + ' ' + "3.6520"  + ' ' + "3.3659" + plik + '\n'
      print('writing 1')
      f.write(data)
      continue

  file_path = folder + plik
  print(plik)
  tables = camelot.read_pdf(file_path, pages="all")

  date_string = get_string_date(plik)

  if tables.n == 1:
    kupno, sprzedaż = parse_with_tabula(file_path)
    print(date_string, kupno, sprzedaż)

    sprzedaż = make_a_number(sprzedaż)
    kupno = make_a_number(kupno)
    if isinstance(sprzedaż, float) and isinstance(kupno, float):
      if sprzedaż > kupno:
        kupno_faktyczne = sprzedaż
        sprzedaz_faktyczna = kupno
        sprzedaż = sprzedaz_faktyczna
        kupno = kupno_faktyczne
    with open('data.csv', 'a') as f:
      data = str(id) + ' ' +  date_string + ' ' + str(kupno) + ' ' + str(sprzedaż) + plik + '\n'
      print('writing 2')

      f.write(data)
    continue

  list_of_countries = [country for country in tables[1].df[0]]
  try:
    index_of_chf = list_of_countries.index('Szwajcaria')
  except ValueError:
    # check next page
    list_of_countries = [country for country in tables[2].df[0]]
    index_of_chf = list_of_countries.index('Szwajcaria')

  assert 'kupno' or 'Kupno' in tables[1].df[2][0]
  assert 'sprzedaż' or 'przedaz' in tables[1].df[3][0]


  assert len(tables[1].df.columns) == 4
  # find dataframe that has 4 columns

  kupno = tables[1].df[2][index_of_chf]

  sprzedaż = tables[1].df[3][index_of_chf]
  print(date_string, kupno, sprzedaż)
  sprzedaż = make_a_number(sprzedaż)
  kupno = make_a_number(kupno)
  if isinstance(sprzedaż, float) and isinstance(kupno, float):
    if sprzedaż > kupno:
      kupno_faktyczne = sprzedaż
      sprzedaz_faktyczna = kupno
      sprzedaż = sprzedaz_faktyczna
      kupno = kupno_faktyczne

  with open('data.csv', 'a') as f:
    data = str(id) + ' ' +  date_string + ' ' + str(kupno) + ' ' + str(sprzedaż) + plik +  '\n'
    print('writing 3')

    f.write(data)
  # except:
  #   import ipdb
  #   ipdb.set_trace()
  #   print()


