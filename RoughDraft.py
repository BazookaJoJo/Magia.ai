   
import mwparserfromhell
import pywikibot
import urllib2
from bs4 import BeautifulSoup
import urllib
import json
import sys
import csv
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

'''
variables
will add in input later
'''
PORT_NUMBER = 8080
varietal = "Merlot"
region = "Long Island"
year = '2008'
enwp = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(enwp, varietal)
wikitext=page.get()
wikicode=mwparserfromhell.parse(wikitext)
templates=wikicode.filter_templates()
infobox = templates[1]
climate = ""
flavor = ""
detail_desc = ""
vintage = ""


def summary():
    '''
    Use the Google Knowledge Graph API to get a general summary about this wine.
    Right now, the summary can be more than a sentence, but it can be trimmed down.
    '''

    '''
    Getting URL which uses an API key to access the Google Knowledge Graph API.
    Uses variables such as query, how many responses, indentation, etc...
    '''
    api_key = 'AIzaSyCYo_GVl-dxSGkb-e2uWNnIhRqrErhHjxA'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': varietal,
        'limit': 1,
        'indent': True,
        'key': api_key,
        }
    global climate, flavor, detail_desc
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    '''
    Data parsing
    detail_desc = detailed description = summary
    '''
    for element in response['itemListElement']:
        try:
            detail_desc = element['result']['detailedDescription']['articleBody']
            print detail_desc
        except KeyError:
             detail_desc = "N/A"
        except UnicodeEncodeError:
            detail_desc = "N/A"

    '''
    Use Winkler Index to determine climate of that region
    '''
    wiki = "https://en.wikipedia.org/wiki/Winkler_index"
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")


    reload(sys)
    sys.setdefaultencoding("utf-8")
    table = soup.find_all("table", {"class" : "wikitable"})[1]
    country = ""
    reg = ""
    city = ""
    Winkler = ""
    regions = {}

    for row in table.findAll("tr"):
        cells = row.findAll("td")
        country = str(cells[0].find(text=True))
        reg = str(cells[1].findAll(text=True))
        city = str(cells[2].find(text=True))
        Winkler = str(cells[5].find(text=True))
        regions[reg] = Winkler

    print str(region)
    print regions.keys()
    print region
    regionFormatted = "[u'" + str(region) + "']"
    print Winkler
    try:
        if regions[regionFormatted] == 'Region Ia' or Winkler == 'Region Ib':
            climate = "cool"
            flavor = str(infobox.get('wine_cool').value.get(0)).lower()
        elif regions[regionFormatted] == 'Region II' or regions[regionFormatted] == 'Region III':
            climate = "medium"
            flavor = str(infobox.get('wine_medium').value.get(0)).lower()
        else:
            climate = "hot"
            flavor = str(infobox.get('wine_hot').value.get(0)).lower()
    except KeyError:
        print 'failed to find region'



def popularInRegion():
    '''
    Use the MediaWiki API to access the infobox of a Wikipedia article and retrieve the regions where a certain varietal is grown
    The chardonnay wikipedia page has a different format, so the second template(index 1) isn't the infobox.
 Also the regions section for chardonnay has a different access method compared to the other major varietals.
    This problem may occur with some less popular varietals as well, fix not implemented yet.
    '''

    '''
    retrieve the information in the infobox, which has a list of flavors in climates and popular regions
    '''
    '''
    enwp = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(enwp, varietal)
    wikitext=page.get()
    wikicode=mwparserfromhell.parse(wikitext)
    templates=wikicode.filter_templates()
    infobox = templates[0]
    '''
    for num in range(10):
        infobox=templates[num]
        try:
            infobox.get('regions')
            break
        except:
            continue

    for num in range(10):
        try:
            if region in str(infobox.get('regions').value.get(2*num+1).text):
                return "popular"
                break
        except:
            return "not popular"
            break


def findVintage():
    '''
    vintage.csv file contains a numerical rating for how good the wine in that year was as well as a letter representing if
    the wine is ready to drink, is too late to drink, or should be waited for to drink in the future
    '''
    global vintage
    with open('vintage.csv') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
             if row['Region'] == region:
                 vintage = row[str(year)]


class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        global varietal, region, year

        qs = {}
        path = self.path

        print '******************************'
        print self.path

        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)

        print qs
        print path

        try:
            varietal = qs['query'][0]
        except:
            varietal = "merlot"

        try:
            region = qs['region'][0]
        except:
            region = "Bordeaux"

        try:
            year = qs['year'][0]
        except:
            year = '2008'
        print '*******'
        print varietal
        print region
        print year
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        summary()
        popularInRegion()
        findVintage()
        self.wfile.write("Description = " + detail_desc)
        self.wfile.write("Climate = " + climate)
        self.wfile.write("Flavor = " + flavor)
        self.wfile.write("Vintage = " + vintage)
        varietal=""
        region=""
        year=""




try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER



    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()





    
        
    
    


