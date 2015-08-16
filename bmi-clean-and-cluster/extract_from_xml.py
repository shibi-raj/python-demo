""" extract_from_xml.py

Extracting xml data from SOLR.  Helpful for browser facet output since faceting is not
well-supported in solrpy.
"""

from xml.etree import ElementTree as ET

title = 'facets_country.xml'

data = ''

for line in open(title).readlines():
    value = ET.fromstring(line)
    print value.attrib[ 'name' ]
