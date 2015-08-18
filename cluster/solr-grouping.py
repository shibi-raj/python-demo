import urllib2
import xml.etree.ElementTree as ET


#facet=true&facet.pivot=country,seg,description,id_chart&facet.limit=10
#http://localhost:8983/solr/select?q={!child%20of=%22type:parent%22}industry:heavy_truck

def bold(s):
    """Function to embolden strings output to screen."""
    return '\033[1m' + s + '\033[0m'

J = "http://localhost:8983/solr/select?q={!child%20of=%22type:parent%22}industry:heavy_truck"

openurl = urllib2.urlopen(J)
tree = ET.ElementTree(file=openurl)
root = tree.getroot()


for doc in root.iter(tag='doc'):
    display = []
    for each in doc.iter():
        title = ''
        try:
            if each.attrib['name'] == 'title':  title = each.text
        except: pass
        if each.text and not each.attrib: 
                display.append( '  ' + each.text.lower() )

    display.insert(0,title)
    for i,d in enumerate(display):
        if i == 0: print bold(d)
        else: print d
    print

"""
for each in root.getchildren():
    for e in each.getchildren():
        print e.tag, e.attrib
"""

