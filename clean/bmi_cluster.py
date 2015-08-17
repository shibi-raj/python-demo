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
#__________________________



"""
title = 'facets_id_industry.txt'
all_id_ind = [ x.strip() for x in open(title).readlines() ]

"""

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
        print
        print
        print
        print 'HEADER'
        print country 
        print ind[1]
        print topics
        d = related_ids( country , ind[1], topics )               
        print
        for k in d.iterkeys():
            print
            print k
            for id_chart in d[k]:
                if ( record_has_mult_topics( id_chart ) ): search_desmetier_segment( id_chart )


"""
d          = related_ids( 'United_States', '2302', topics )

for k in d.iterkeys():
    print
    print k
    for id_chart in d[k]:
        if ( record_has_mult_topics( id_chart ) ): search_desmetier_segment( id_chart )


for each in ind_ids_names:
    d = industry_and_topics( each[1] )
    print each[0] 
    for topic in d.iterkeys():
        print topic.ljust(30), d[topic]
    print

for id_ind in all_id_ind:
    ind_ids_names.append( [ id_ind_to_ind_name( id_ind ), id_ind])    

for each in ind_ids_names:
    print each[0], each[1]

for id_ind in all_id_ind:
    d = industry_and_topics( id_ind )
    print id_ind_to_ind_name( id_ind )
    for topic in d.iterkeys():
        print topic.ljust(30), d[topic]
    print
"""



#for _id in all_id_ind:
#    print industry_and_topics( _id )



"""
for k in d.iterkeys():
    print k
    for each in cleaner(cluster_ids_2_ids_titles(d[k])):
        print each[1]
    print

"""


"""
i_c = 1329

if ( record_has_mult_topics( i_c ) ): search_desmetier_segment( i_c )


for item  in cl_terms():
    for rec in all_records:
        es = excl_simple( item, rec )
        print item
"""




#_________________________
"""
for country in countries:
    for id_ind in id_industries:
        if id_ind == '2302':
            x = TaxoIds(int(id_ind))
            print country+',', x.id_name_pair()[1]
            related_ids( country, id_ind, topics )
            print
"""

"""
# Taxo tree depricated ...
id_industries = []
for taxo_id in taxo_col(6):
    if taxo_id != '':
        if taxo_id not in id_industries:
           id_industries.append(taxo_id)  
id_industries.sort()
id_industries = map(str,id_industries)
"""




