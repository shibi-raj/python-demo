"""  bmi_cluster.py

Clustering Input: Country, Sector ID, Indicators/Topics
"""

import solr
import time
from   bmi_cluster_helper     import *
from   bmi_cleaner_helper     import *
from   taxonomy               import *

s                =  solr.SolrConnection('http://85.31.219.96:7183/solr')
id_industry      =   '2302'
topics           = [ 'sales', 'production', 'export', 'import' ]


title = 'facets_country.txt'
all_country   = [ x.strip() for x in open(title).readlines() ]

title = 'ind_names_ids.txt'
ind_ids_names = [ x.split() for x in open(title).readlines()]
ind_ids_names.sort()

for country in all_country:
    for ind in ind_ids_names:
        topics = []        
        for key_topic in industry_and_topics( ind[1] ).iterkeys():
            topics.append(key_topic) 
        d = related_ids( country , ind[1], topics )               
        for k in d.iterkeys():
            for id_chart in d[k]:
                if ( record_has_mult_topics( id_chart ) ): search_desmetier_segment( id_chart )


