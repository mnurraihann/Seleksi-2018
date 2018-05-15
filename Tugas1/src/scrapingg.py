from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import time

def scrape_smallpic(url):
    result = []
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    
    name = soup.find("title").text
    result.append(name)
    
    location = soup.find("meta",{"property":"urbanindocom:location"})['content']
    result.append(location)
    
    tipe1 = soup.find("li",{"class":"col-md-6 pb5 attribute-propertyType"})
    tipe = tipe1.find("span",{"class":"col-xs-5"}).text
    result.append(tipe)
    
    iklan1 = soup.find("li",{"class":"col-md-6 pb5 attribute-listingType"})
    iklan = iklan1.find("span",{"class":"col-xs-5"}).text
    result.append(iklan)
    
    harga1 = soup.find("li",{"class":"col-md-6 pb5 attribute-price"})
    harga = harga1.find("span",{"class":"col-xs-5"}).text
    result.append(harga)
    
    land1 = soup.find("li",{"class":"col-md-6 pb5 attribute-landSize"})
    land = land1.find("span",{"class":"col-xs-5"}).text
    result.append(land)
    
    if tipe == "Rumah":
        kt1 = soup.find("li",{"class":"col-md-6 pb5 attribute-bedrooms"})
        kt = kt1.find("span",{"class":"col-xs-5"}).text
        result.append(kt)
    
        km1 = soup.find("li",{"class":"col-md-6 pb5 attribute-bathrooms"})
        km = km1.find("span",{"class":"col-xs-5"}).text
        result.append(km)
    
    if tipe != "Tanah":
        building1 = soup.find("li",{"class":"col-md-6 pb5 attribute-buildingSize"})
        building = building1.find("span",{"class":"col-xs-5"}).text
        result.append(building)
    
    return result

def scrape_bigpict(url):
    page = urlopen(url).read()
    soup = BeautifulSoup(page,'html.parser')
    text = soup.find_all("meta",{"itemprop":"url"})
    result = [line['content'] for line in text]
    return result

urls = scrape_bigpict("https://www.urbanindo.com/cari/bandung")
result = []
for url2 in urls:
    url = "https://www.urbanindo.com"+url2
    x = scrape_smallpic(url)
    result.append(x)
    time.sleep(1)
print(result)
with open('data.json', 'w') as outfile:
    json.dump(result, outfile)

