import mwparserfromhell
import pywikibot
import argparse

def main():
    query = "merlot"
    enwp = pywikibot.Site('en', 'wikipedia')
    page = pywikibot.Page(enwp, query)
    wikitext=page.get()
    wikicode=mwparserfromhell.parse(wikitext)
    templates=wikicode.filter_templates()
    infobox=templates[1]
    for param in infobox.params:
        try:
            print param.name, param.value
        except:
            print " "

    print "The most popular regions of " + query + " are " + str(infobox.get('regions').value.get(1).text) + ", " + str(infobox.get('regions').value.get(3).text) + ", and " + str(infobox.get('regions').value.get(5).text) + "."

    print infobox.get('wine_general').value.get(0)



if __name__ == '__main__':
   main()