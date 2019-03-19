import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd
import re

page_counter = 8040 #8575
page_url     = "https://www.xeno-canto.org/explore?dir=0&order=xc&pg="
download_url = "https://www.xeno-canto.org"
folder       =  "/media/neramas1221/Maxtor/sounds/"
row_Data     = []
col_Data     = []
cont         = True
table_data   = np.array([])

while cont:
    print("loop " + str(page_counter))
    row_Data     = []
    page         = requests.get(page_url + str(page_counter))
    soup         = BeautifulSoup(page.text, 'lxml')
    table        = soup.find(class_="results")
    rows         = table.find_all('tr')
    for row in range(1, len(rows)):
        cols     = rows[row].find_all('td')
        col_Data = []
        for col in range(1, len(cols)):
            if cols[col].contents !=[]:
                info = cols[col].contents[0]
            else:
                info = " "
            if cols[col].find_all('p') != []:
                info = cols[col].find('p')
                info = info.contents[0]

            elif cols[col].find_all('a') != []:
                info = cols[col].find('a')

                if 'download' in str(info):
                    info = info['href']

                else:
                    info = info.contents[0]
            if cols[col].find_all(class_='rating') != []:

                if cols[col].find_all(class_='selected') != []:
                    section = cols[col].find(class_='selected')
                    rating  = section.contents[0]
                    rating  = rating.contents[0]
                    col_Data.append(rating)
                else:
                    col_Data.append(" ")

            info = " ".join(str(info).split())
            col_Data.append(info)
        row_Data.append(col_Data)
    f = open("/media/neramas1221/Maxtor/bird_data_text.txt", "a")
    for i in range(0, len(row_Data)):
        for j in range(0, len(cols)):
            row_Data[i][j] = re.sub('[!@#$",]', '', row_Data[i][j])
            f.write('"' + str(row_Data[i][j]) + '"'  + ",")
        f.write("\n")
    f.close()
    for i in range(0, len(row_Data)):
        print("Downloading...")
        if "img" not in (download_url + str(row_Data[i][11])):
    
            r = requests.get(download_url + str(row_Data[i][11]), stream=True)
            with open(folder+str(row_Data[i][12])+".mp3", 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            f.close()
        print("...Done")

    time.sleep(0.1)
    
    # if page_counter == 1:
    #     table_data = np.array(row_Data)
    # else:
    #     table_data = np.vstack((table_data, row_Data))
    
    if len(row_Data) != 30:
        cont = False
    else:
        page_counter = page_counter + 1

#output = pd.DataFrame(table_data,columns = ['Common name','Length','Recordist','Date','Time','Country',
 #                                           'Location','Elev. (m)','Type','Remarks','Rating','Download link',
  #                                          'ID'])
#output.to_csv("data_set.csv")
print(table_data.size)
print(table_data.shape)
