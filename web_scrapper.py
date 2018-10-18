import requests
from bs4 import BeautifulSoup
import numpy as np
import webbrowser

page_counter = 1
page_url = "https://www.xeno-canto.org/explore?dir=0&order=xc&pg="
print(page_url + str(page_counter))
page = requests.get(page_url+ str(page_counter))

soup = BeautifulSoup(page.text,'lxml')

table = soup.find(class_="results")#'table',attrs={'class':'results'})
rows = table.find_all('tr')
cols = []
for row in rows:
    cols.append(row.find_all('td'))
