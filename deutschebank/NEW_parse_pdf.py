import camelot
import tabula
import os

from extract_date import get_string_date

folder = "dane/"

pliki = os.listdir(folder)

# filtruj na indywidualne
pliki = [p for p in pliki if 'ndywidu' in p]

def parse_with_tabula(file_path):
  tables = tabula.read_pdf(file_path, pages="all")

  try:
    kraje = [kraj for kraj in tables[1]['Kraj']]
    chf_index = kraje.index('Szwajcaria')

    kupno = tables[1]['kupno'][chf_index]
    sprzedaż = tables[1]['sprzedaż'][chf_index]
  except:
    import ipdb
    ipdb.set_trace()

  return kupno, sprzedaż

  # try:
  # line = find_CHF_line(tables[0][data_key])
  # # except TypeError:
  # #   countries = [c for c in tables[0][data_key]]
  # #   index_of_chf = countries.index('Szwajcaria')
  # #   assert 'kupno' in tables[0]['Unnamed: 2'][1]
  # #   assert 'sprzedaż' or 'sprzedaz' in tables[0]['Dewizy'][1]
  # #   sprzedaż = tables[0]['Dewizy'][index_of_chf]
  # #   kupno = tables[0]['Unnamed: 2'][index_of_chf]
  # #   return kupno, sprzedaż

  # sprzedaż = line.split(' ')[1]
  # kupno = line.split(' ')[2]

  # return kupno, sprzedaż

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

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

def find_CHF_row(df):
  list_ = [a for a in df[0]]

  chf_indexes = (find_indices(list_, 'CHF'))

  if len(chf_indexes) != 2:
    import ipdb;ipdb.set_trace()
    raise Exception("WTF")
  # return second index
  return chf_indexes[1]

def find_tabela_kursowa(tables):
  # Tabela kursów dla kredytów mieszkaniowych i konsolidacyjnych w walutach obcych

  sizes = [len(table.df.columns) for table in tables]
  if sizes.count(4) not in (1, 0):
    import ipdb
    ipdb.set_trace()
    raise Exception('more 4 sized tables than expected.')

  for table in tables:
    if len(table.df.columns) == 4:
      return table
  print('not found!')
  import ipdb
  ipdb.set_trace()

def parse(string_number):
  if isinstance(string_number, float):
    return string_number

  string_number = string_number.replace(',', '.')

  if '-' in string_number:
    return 'BRAK DANYCH'

  return float(string_number)

def extract_from_table_of_size_1(tables):
  chf_index = find_CHF_row(tables[0].df)

  # weird assert for kupno sprzedaz (lower/uppercase safe)
  assert 'rzeda' in tables[0].df[2][1]
  assert 'upno' in tables[0].df[1][1]

  sprzedaz = tables[0].df[2][chf_index] # sprzedaz
  kupno = tables[0].df[1][chf_index] # kupno

  sprzedaz = parse(sprzedaz)
  kupno = parse(kupno)

  return kupno, sprzedaz

def extract_from_regular(tabela_kursowa):
  kraje = [kraj for kraj in tabela_kursowa.df[0]]
  chf_index = kraje.index('Szwajcaria')

  assert 'upno' in tabela_kursowa.df[2][0]
  assert 'eda' in tabela_kursowa.df[3][0]

  kupno = tabela_kursowa.df[2][chf_index]
  sprzedaż = tabela_kursowa.df[3][chf_index]

  return kupno, sprzedaż

# index number
# idx, x in enumerate(xs)
for id, plik in enumerate(pliki):
  # if id < 414:
  #   print('skipping', id)
  #   continue

  # Edge case
  # if plik == ' poland documents exchange-rates 2014 11 klienci_indywidualni_i_biznesowi_2014-11-21.pdf':
  #   with open('data.csv', 'a') as f:
  #     data = str(id) + ' ' +  "2014-11-21" + ' ' + "3.6520"  + ' ' + "3.3659" + plik + '\n'
  #     print('writing 1')
  #     f.write(data)
  #     continue

  file_path = folder + plik
  print(plik)
  tables = camelot.read_pdf(file_path, pages="all")

  date_string = get_string_date(plik)

  if tables.n == 1:
    list_ = [a for a in tables[0].df[0]]
    if 'Szwajcaria' in list_:
      kupno, sprzedaż = parse_with_tabula(file_path)
    else:
      kupno, sprzedaż = extract_from_table_of_size_1(tables)
  else:
    tabela_kursowa = find_tabela_kursowa(tables)
    kupno, sprzedaż = extract_from_regular(tabela_kursowa)

  with open('data.csv', 'a') as f:
    print('writing', id, date_string, str(kupno), str(sprzedaż))
    data = str(id) + ' ' +  date_string + ' ' + str(kupno) + ' ' + str(sprzedaż) + plik + '\n'
    f.write(data)



