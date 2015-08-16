#  bmi_cluster_helper.py
#
#  Helper functions for BMI clustering of related files: 
#      Country, Sector, Topics

import ast
import solr
import pysolr
from   general_python_helpers import *
from   bisect                 import bisect_left
from   bmi_cleaner_helper     import *


s        =  solr.SolrConnection('http://85.31.219.96:7183/solr')




#______________________________________________________________
#
#  Cluster Formatting Functions - Possibly temporary, up to Ben
#______________________________________________________________


def cat_top_tle(country, ind, records = []):

    id_ind = int(ind[0])
    d_ctt  = {} 
    msd    = ''

    for r in records:
        id_ok =  no_key_err(  r, 'id_industry' )
        if any( io == id_ind for io in id_ok  ): 
            ctry    =  no_key_err(  r, 'country' )
            if any(  c for c in ctry ):
               ctry  = rm_list_underscores( ctry )
               for c in ctry:
                   if c == country:
                        # Category
                        msd  =   max_seg_des(r)
                        if   not msd :   msd =  'category???'
                        if   msd     not in  d_ctt: d_ctt[msd] =     {}
                        # --- Topic
                        topic   = no_key_err(  r, 'topic'   )
                        content = no_key_err(  r, 'content' )
                        the_topic = []
                        if any ( t for t in topic ):
                            for top in topic:
                                #if  top not in d_ctt[msd]: 
                                    the_topic.append(top)
                        elif any (ctnt for ctnt in content):
                            #print content[0]
                            if 'trade balance' in content[0]:  
                                    the_topic = ['trade balance']
                            if 'density'       in content[0]:  
                                    the_topic = ['density']
                        if not the_topic: the_topic = ['No Topic']
                        # ----- Titles
                        for t in the_topic:
                            if t not in d_ctt[msd]:  d_ctt[msd][t] = [ r['title_url'] ]
                            else: d_ctt[msd][t].append(r[ 'title_url' ])
    #print 'look here', d_ctt
    #print
    #for cat in d_ctt.iterkeys():
    #    d_ctt[cat] = top_and_tle( d_ctt[cat] )
    #print msd.upper()
    #print d_ctt
    #format_ctt(d_ctt)
    for cat in d_ctt.iterkeys():
        print  '\t', cat 
        for topic in d_ctt[cat].iterkeys():
            print '\t\t\t',topic
            for title in d_ctt[cat][topic]:
                print '\t\t\t\t\t', title




def format_ctt(d_ctt):
    for cat in d_ctt.iterkeys():
        print '\t', cat.upper()
        d_tt = d_ctt[cat]   
        for record in d_tt:
            print '\t\t\t', record['id_chart'],record['title_url']
             
        """
        for top in d_tt:
            if top != 'No Topic':
                print '\t\t',top#.upper()
                for tle in d_tt[top]:
                    print '\t\t\t',tle
        """


def no_key_err(record = {}, string = '' ):
    try:
        if ( record[string] ): 
            ls = record[string] 
    except KeyError:
        ls = [False]
    return ls


def max_seg_des( r = {} ):

    bsd     = []
    sd_keep = []
    sdmax   = ''

    seg_des = [ 'best_segment',   'best_desmetier'  ]
    seg_des = [  no_key_err(r ,x)  for x in seg_des ]

    for s_d in seg_des:
        for sd in s_d:
            if  sd:  
                for each in s_d: 
                    if each not in bsd:  bsd.append(each)

    bsd = rm_list_underscores(bsd)

    for sd in bsd:
        if sd in r['title_url'].lower():  sd_keep.append(sd)
    if sd_keep:
        sdmax =  max(sd_keep, key=len)

    return sdmax



def top_and_tle( records = [] ):

    d_tt = {}
    d_tt['No Topic'] = []

    for r in records:
        try:
            for top in r['topic']:
                if    top not in d_tt:  d_tt[top]     = [ r['title_url'] ]
                else:                   d_tt[top].append( r['title_url'] )
        except KeyError as ke: 
            d_tt['No Topic'].append(r['title_url'])
    return d_tt

#______________________________________________________________


def loc_topic_facet( id_ind, records ):
    topics = [ 'sales', 'production', 'export', 'import', 'consumer', 'price', 'wage', \
               'market share', 'population' ]
    i_topics = [0]*len(topics)
    id_ind = int(id_ind)
    #d = {}
    i = 0
    for d in records:  
        try:
            for idi in d['id_industry']: 
                if id_ind == idi: 
                    for t in d['topic']:  
                        if t not in topics:
                            topics.append(t)
                            i_topics.append(0)
                        for it, top in enumerate(topics):
                            if t == top: i_topics[it] += 1
        except KeyError:
            pass

    # Convert to and return a dictionary
    dict = {}
    for it, topic in enumerate(topics):
        if i_topics[it] != 0: dict[topic] = i_topics[it]

    return dict


def out_segment_topics( ind_id_name, d = {} ):
    print ind_id_name[0]
    for k in d.iterkeys():
        print k, d[k]
    print

#________________________________________________
#
#  Input records
#________________________________________________


def get_condensed_records( file_name ):
    records = []
    with open(file_name) as f:
        for line in f:
            if  line.strip():
                line_dict = str_to_dict(line.strip())
                records.append( line_dict )
    return records


def get_records( file_name, seq     = ['id_chart', 'title_url', 'id_industry']):
    records = []
    count = 0
    with open(file_name) as f:
        for line in f:
            if  line.strip():
                line_dict = str_to_dict(line.strip())
                try:
                    records.append( { k:line_dict[k] for k in seq } )
                except KeyError as ke:
                    count += 1
                    records.append( { k:line_dict[k] for k in seq if k in line_dict} )
    return records
        
#__________________________________________________________________    
#
#  String manipulation functions
#__________________________________________________________________    


def str_to_dict( string = '' ):
    d = {}
    try:
        d = ast.literal_eval(string.strip())
    except SyntaxError, ValueError:
        pass
    return d



def rm_list_underscores( ls = [] ):
    ls = [ l.replace('_',' ') for l in ls]        
    return ls


#________________________________________________
#
#  Functions that fetching from the SOLR database
#________________________________________________

def related_ids( country, id_ind, topics ):	
    """ Input:  country, industry id, and list of topics
        Output: dictionary with topics as keys and lists of record ids having the input criteria  """

    filter   =  "country:" +   country  + " AND "     + "id_industry:"   + id_ind
    response =  s.query(q='*', fq=filter,  rows="1000")
    #response =  s.query(q='*', fq=filter,  rows="1000",  fields="title_url,id_chart,topic,country")
    d        =  {}

    for topic in topics:
        d[topic] = []
        for hit in response.results:
            try:
                if   topic  in     hit['topic']:
                   d[topic].append(hit['id_chart'])
                   #print hit['country'], hit['id_industry'], hit['topic']
            except KeyError:
                pass
    return d


def cluster_ids_2_ids_titles(id_list):
    """ Takes list of ids and retrieves the titles via SOLR.
        Returns list of sublists of form [ [id, title], ... ] """

    id_title =  []
    for each in id_list:
        query    = 'id_chart:'   + str(each)
        response =  s.query(query, fields =  "title_url")
        [ id_title.append( [each,hit['title_url'] ] ) for hit in response.results ]
    return id_title


def industry_and_topics( id_industry ):
    """  
    !!! NOW USING pysolr PACKAGE INSTEAD OF solrpy !!!
    """
    """ Input : id_industry
        Output: dictionary of topics and their faceted counts """  

    query   = 'id_industry:' + str(id_industry)

    solr    = pysolr.Solr('http://85.31.219.96:7183/solr/')
    params  = {  'facet.field' : 'topic',  } 
    results = solr.search(query, facet = 'on', **params )

    facets = results.facets['facet_fields']['topic']
    return list_to_dict(facets)


def id_ind_to_ind_name(id_industry):
    query   = 'id_industry:' + str(id_industry)
    solr    = pysolr.Solr('http://85.31.219.96:7183/solr/')
    results = solr.search(query)
    name = ''
    for hit in results:
        name = hit['industry'][0]
        break    
    return name


def record_has_mult_topics( id_chart ):

    query   = 'id_chart:' + str(id_chart)
    solr    = pysolr.Solr('http://85.31.219.96:7183/solr/')
    results = solr.search( query, fl='topic', rows='100' )

    id_chart = False
    for hit in results:
        try:
            if ( len(hit['topic']) > 1 ): id_chart = True
        except KeyError:
            pass
    return id_chart


#____________________________
#
#  Codes not presently in use
#____________________________


"""
def get_records( file_name ):
    records = []
    function = lambda x: filter_get_records(x['title_url'].lower())
    title_generator = get_rec_generator(file_name)
    records = filter(function, title_generator)
    return records

def get_rec_generator(file_name):
    seq     = ['id_chart', 'title_url', 'id_industry', 'industry', 'topic' ]
    with open(file_name) as f:
        for line in f:
            if line.strip():
                line_dict = str_to_dict(line.strip())
                try:
                    yield { k:line_dict[k] for k in seq }
                except KeyError:
                    pass

def filter_get_records(title):
    good_title = True
    for term in cl_terms():
        if term in title:  
            good_title = False
            break
    return good_title    
"""


"""
#_______________________________________________
#bufsize=4096
def delimited(file, delimiter='\n', bufsize=64):
    buf = ''
    while True:
        newbuf = file.read(bufsize)
        print newbuf
        if not newbuf:
            yield buf
            return
        buf += newbuf
        lines = buf.split(delimiter)
        for line in lines[:-1]:
            yield line
        buf = lines[-1]
"""
