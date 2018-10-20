import requests
from bs4 import BeautifulSoup

page_counter = 1
page_url     = "https://www.xeno-canto.org/explore?dir=0&order=xc&pg="
download_url = "https://www.xeno-canto.org"
page         = requests.get(page_url+ str(page_counter))
soup         = BeautifulSoup(page.text,'lxml')
table        = soup.find(class_="results")
rows         = table.find_all('tr')
data         = []
data_two     = []

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
                info = info['href']
            else:
                info = info.contents[0]
        info = " ".join(str(info).split())        
        data_two.append(info)
    data.append(data_two)

f = open("test.txt","w")
for i in range(0,len(data)):
    for j in range(0,len(cols)):
        f.write(str(data[i][j]) + "\n\n")

f.close()

print("Downloading...")
r = requests.get(download_url + str(data[3][10]),stream=True)
with open(str(data[3][11])+".mp3",'wb') as f:
    for chunk in r.iter_content(chunk_size = 1024):
        if chunk:
            f.write(chunk)
print("...Done")