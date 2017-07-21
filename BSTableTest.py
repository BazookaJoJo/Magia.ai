from bs4 import BeautifulSoup
import urllib2
import sys



wiki = "https://en.wikipedia.org/wiki/Winkler_index"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "html.parser")

#print soup.contents
 
 
reload(sys)
sys.setdefaultencoding("utf-8") 
 
table = soup.find_all("table", {"class" : "wikitable"})[1]

country = ""
region = ""
city = ""
Winkler = ""
climate = ""

regions = {}

for row in table.findAll("tr"):
    cells = row.findAll("td")
    country = str(cells[0].find(text=True))
    region = str(cells[1].findAll(text=True))
    city = str(cells[2].find(text=True))
    Winkler = str(cells[5].find(text=True))
    regions[region] = Winkler
    print Winkler

    
    
#print regions['Bordeaux']

