import requests
from bs4 import BeautifulSoup
import time


page_counter = 1
page_url     = "https://www.xeno-canto.org/explore?dir=0&order=xc&pg="
download_url = "https://www.xeno-canto.org"
folder       = "./sounds/"
"""page         = requests.get(page_url + str(page_counter))
soup         = BeautifulSoup(page.text, 'lxml')
table        = soup.find(class_="results")
rows         = table.find_all('tr') """
data         = []
data_two     = []
cont         = True

while cont:
    print("loop " + str(page_counter))
    data         = []
    page         = requests.get(page_url + str(page_counter))
    soup         = BeautifulSoup(page.text, 'lxml')
    table        = soup.find(class_="results")
    rows         = table.find_all('tr')
    for row in range(1, len(rows)):
        cols     = rows[row].find_all('td')
        data_two = []
        for col in range(1, len(cols)):

            info = cols[col].contents[0]
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
                    data_two.append(rating)
                else:
                    data_two.append(" ")

            info = " ".join(str(info).split())
            data_two.append(info)
        data.append(data_two)
    f = open("test.txt", "w")
    for i in range(0, len(data)):
        for j in range(0, len(cols)-1):
            f.write(str(data[i][j]) + "\n\n")

    f.close()
    for i in range(0, len(data)):

        print("Downloading...")
        r = requests.get(download_url + str(data[i][11]), stream=True)
        with open(folder+str(data[i][12])+".mp3", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        f.close()
        print("...Done")
        time.sleep(0.1)

    if len(cols) != 30:
        cont = False
    else:
        page_counter = page_counter + 1
