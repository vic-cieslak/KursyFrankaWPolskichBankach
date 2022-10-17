import os

folder = 'dane/'

pliki = os.listdir('dane/')
pliki.sort()

for plik in pliki:
  with open('dane/' + plik, 'r') as f:
    lines = f.readlines()
    if "DOCTYPE html" in lines[0]:
      print('removing,', plik)
      os.remove('dane/' + plik)

