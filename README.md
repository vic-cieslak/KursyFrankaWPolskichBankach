# KursyFrankaWPolskichBankach
Scraper and parser for CHF/PLN pairs to excel format for most major banks in Poland

This scraping code is messy AF but produces 100% correct output.
It can even parse pdfs from deutsche bank (FU deutsche bank, get a proper API)



It requires some fiddling with the code sometime or running scripts in correct order.
But the basic flow is: 
1. scrap data (json, html, xml, pdfs)
2. parse data

Sometimes it's:
1. scrap available times/dates
2. scrap again using given times or dates
3. process to build a data list/pandas dataframe
4. convert to excel

If you lack some basic coding skills you will probably have trouble running it 
(hit me for ready excel spreadsheets or help, I did not had the reason to clean up the code) 

Some code looks like async but it's not, it takes a while anyway to download all the data. 

# Setup 

1. create virtual environment for python
2. install dependencies with ```pip install -r requirements.txt```
3. enter folder of given bank.
4. create directory named /dane 
5. to start scraping -> ```python scrap.py```
6. after scraping all the data run ```python process.py``` (or similar, some banks are more complex to parse and require more scripts to run)
