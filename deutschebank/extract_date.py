import datefinder


def get_string_date(nazwa_pliku):
  matches = extract_date(nazwa_pliku)
  return normalize_date(matches)

def normalize_date(matches):
  if type(matches) == str:
    return matches
  else:
    return matches[0].strftime('%Y-%m-%d')

# Format is
# 2004-01-02
# %Y-%m-%d
# this is a terrible date parser
def extract_date(nazwa_pliku):
  if 'Klienci' in nazwa_pliku:
    # split on 'Klienci"
    string_do_wyciagania = nazwa_pliku.split('Klienci')[1]
    if '02.03.2022' in string_do_wyciagania:
      return '2022-03-02'
    elif '08.03.2022' in string_do_wyciagania:
      return '2022-03-24'
    elif '24.02.2022' in string_do_wyciagania:
      return '2022-02-24'
  elif 'klienci' in nazwa_pliku:
    # split on 'klienci"
    string_do_wyciagania = nazwa_pliku.split('klienci')[1]
  else:
    string_do_wyciagania = nazwa_pliku.split(' ')[-1]

  matches = list(datefinder.find_dates(string_do_wyciagania))

  if not matches:
    if '_' in string_do_wyciagania:
      new = string_do_wyciagania.split('_')[0]
      matches = list(datefinder.find_dates(new))
      if not matches:
        if len(string_do_wyciagania.split('_')) == 5:
          new = string_do_wyciagania.split('_')[-2]
          matches = list(datefinder.find_dates(new))
          if len(matches) == 2:
            print(nazwa_pliku)
          return matches
        else:
          # print("NO MATCHES STILL")
          raise Exception('no match')

      else:
        if len(matches) == 2:
          print(nazwa_pliku)
        return matches
    else:
      # Format is
      # 2004-01-02
      # %Y-%m-%d
      if '21-09-2020-2' in nazwa_pliku:
        return '2020-09-21'
      elif '19-11-2018-2' in nazwa_pliku:
        return '2018-11-19'
      elif '29-07.2021.pdf' in nazwa_pliku:
        return '2021-07-29'
      elif '%20indywidualni%20-%2002.08.2021.pdf' in nazwa_pliku:
        return '2021-08-02'
      elif '26-05-2020-2.pdf' in nazwa_pliku:
        return '2020-05-26'
      elif '0209.pdf' in nazwa_pliku:
        return '2021-09-02' # TODO
      elif '29-03.2021.pdf' in nazwa_pliku:
        return '2021-03-29'
      elif '15-11-2018-2.pdf' in nazwa_pliku:
        return '2018-11-15'
      elif '17-03-2020-2.pdf' in nazwa_pliku:
        return '2020-03-17'
      elif '16-11-2018-2.pdf' in nazwa_pliku:
        return '2018-11-16'
  else:
    return matches


def extract_date_from_pdf(tables):
  try:
    if "TABELA KURSÓW KUPNA" in tables[0].df[0][0]:
      date = tables[0].df[0][0].split('w dniu ')[-1]

      print('found ', date, '!')
      return date
    else:
      print('not found')
      print(tables[0].df[0][0])
  except AttributeError:
    print('AttributeError')


  return None