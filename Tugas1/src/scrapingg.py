from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import time

#Scrape big picture
def scrape_smallpic(url):
    result = {}
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    
    #Judul iklan
    name = soup.find("title").text
    result['nama']=name
    
    #Tipe properti
    tipe1 = soup.find("li",{"class":"col-md-6 pb5 attribute-propertyType"})
    tipe = tipe1.find("span",{"class":"col-xs-5"}).text
    result['tipe']=tipe
    
    #Lokasi properti
    location = soup.find("meta",{"property":"urbanindocom:location"})['content']
    result['lokasi']=location
    
    #Harga properti
    harga = soup.find("meta",{"property":"urbanindocom:price"})['content']
    result['harga']=harga
    
    if tipe == "Rumah":
        #Jumlah kamar tidur
        kt1 = soup.find("i",{"uif uif-property-bedrooms"})
        kt = (kt1.find_next_sibling("span",{"attr-item"}).text).strip()
        result['jumlah kamar tidur']=kt
        
        #Jumlah kamar mandi
        km1 = soup.find("i",{"uif uif-property-bathrooms"})
        km = (km1.find_next_sibling("span",{"attr-item"}).text).strip()
        result['jumlah kamar mandi']=km
    
    if tipe != "Tanah":
        #Luas bangunan
        building1 = soup.find("i",{"uif uif-property-buildingSize"})
        building = (building1.find_next_sibling("span",{"attr-item"}).text).strip()
        result['luas bangunan']=building
    
    if tipe != "Apartemen":
        #Luas tanah
        land1 = soup.find("i",{"uif uif-property-landSize"})
        land = (land1.find_next_sibling("span",{"attr-item"}).text).strip()
        result['luas tanah']=land
    
    return result

#Scrape small picture
def scrape_bigpict(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    text = soup.find_all("meta",{"itemprop":"url"})
    result = [line['content'] for line in text]
    return result

#find all urls
allurls = []
for i in range (10):
    urls = scrape_bigpict("https://www.urbanindo.com/cari/Indonesia/location_bandung/listingType_sale/radius_-1/page_"+str(i+1)+"/marketType_0")
    print(urls)
    allurls = allurls + urls

#scrape from those urls
result = []
for url2 in allurls:
    url = "https://www.urbanindo.com"+url2
    print(url)
    x = scrape_smallpic(url)
    print(x)
    result.append(x)
    time.sleep(5)

with open('data.json', 'w') as outfile:
    json.dump(result, outfile,indent=4)
