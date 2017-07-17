import mwparserfromhell
import pywikibot
import argparse
import wikipedia
import urllib2
from bs4 import BeautifulSoup
import urllib
import json


varietal = ""
region = ""
year = 0

def summary():
    api_key = 'AIzaSyCYo_GVl-dxSGkb-e2uWNnIhRqrErhHjxA'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

    params = {
        'query': varietal,
        'limit': 1,
        'indent': True,
        'key': api_key,
        }

    url = service_url + '?' + urllib.urlencode(params)  # TODO: use requests
    response = json.loads(urllib.urlopen(url).read())
    # Parsing the response  TODO: log all responses

    for element in response['itemListElement']:
        try:
            detail_desc = element['result']['detailedDescription']['articleBody']
            print detail_desc
        except KeyError:
            detail_desc = "N/A"
        except UnicodeEncodeError:
            detail_desc = "N/A"
            
            
def popularInRegion():
    




