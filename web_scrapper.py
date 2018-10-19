import requests
from bs4 import BeautifulSoup
import numpy as np
import webbrowser

page_counter = 1

page_url = "https://www.xeno-canto.org/explore?dir=0&order=xc&pg="

#print(page_url + str(page_counter))

page = requests.get(page_url+ str(page_counter))

soup = BeautifulSoup(page.text,'lxml')

table = soup.find(class_="results")
rows = table.find_all('tr')
data =[]

for row in range (1,len(rows)):
    cols = rows[row].find_all('td')
    
    for col in range(1,len(cols)):

        info = cols[col].contents[0]
        if cols[col].find_all('p') != []:
            info = cols[col].find('p')
            info = info.contents[0]
            
        elif cols[col].find_all('a') != []:
            info = cols[col].find('a')
            
            if 'download' in str(info):
                print(info['href'])
                info = info['href']
            else:
                info = info.contents[0]
            
        #elif cols[col].find('img') !=[]:#,attrs = {'title'})
            #info = cols[col].find('img')
            #print(info)
           
        data.append(info)#str(cols[col].contents[0]))
        
f = open("test.txt","w")
for i in range(0,len(data)):
    f.write(str(data[i]) + "\n")

f.close()