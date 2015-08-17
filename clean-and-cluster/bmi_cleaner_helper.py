"""  bmi_cleaner_helper.py

Set of helper functions for the cleaning of BMI titles.
Handler for output files
"""

import re
import time
import itertools
#from   bmi_cluster_helper import *

class OP_Handler:
    def __init__(self,path,file_name):
        self.counter   = 0
        self.path      = path
        self.file_name = file_name
        self.file      = open(self.path+self.file_name, 'w')
        self.info      = ''

    def record(self, info):
        self.counter += 1
        self.info     = info
        self.file.write(str(self.info)+'\n')

    def cleanup(self):
        self.file.write('\n'+str(self.counter))
        self.file.close()

    def echo(self):
        print
        print self.file_name
        print self.counter
        print self.info


#__________________________________________________________________
#
# Cleaner function
#__________________________________________________________________


def keep_title( title ):
    absent = False
    for term in cl_terms():
        absent =  not  match( term, title )
        if   not  absent  : break
    return  absent


def cleaner( records = [] ):
    """ Input  - all records raw, uncleaned
        Output - will soon return records kept after cleaning   """

    remove     = []
    ids_titles = []

    for rec in records:  
        ids_titles.append( [ rec['id_chart'], rec['title_url'].lower() ] )

    start = time.time()

    # ___Applying cleaning rules___


    function = lambda x: binary_search(remove, int(x['id_chart'])) < 0

    for term in cl_terms():
        remove    += [ it[0] for it in ids_titles if match(term.lower(), it[1]) ]
    remove.sort()
    rec_generator  = filter_list_generator(records)
    records        = filter(function, rec_generator)
    ids_titles = []
    for rec in records:  
        ids_titles.append( [ rec['id_chart'], rec['title_url'].lower() ] )

    remove         = spec_currency( ids_titles ) 
    remove.sort()
    rec_generator  = filter_list_generator(records)
    records        = filter(function, rec_generator)
    ids_titles = []
    for rec in records:  
        ids_titles.append( [ rec['id_chart'], rec['title_url'].lower() ] )

    remove         = dupli_titles( 'units,  mn', 'units', ids_titles)
    remove        += dupli_titles( 'units mn'  , 'units', ids_titles)
    remove.sort()
    rec_generator  = filter_list_generator(records)
    records        = filter(function, rec_generator)

    return records # want this to return records


def filter_list_generator( data = [] ):
    for d in data:
        yield d


def remove_records( records = [], id_remove = [] ):
    return [ rec for rec in records if rec[0] not in id_remove ]


def match( string, title ):
    """   Input:   'string' to search for in 'title' """
    title = title.lower()
    if    (string != '')   and (string in title):  string = True
    else:  string  = False
    return string


#_____________________________________________________________________________
#
#  Supporting functions working on Titles
#_____________________________________________________________________________

def pivot(title):
    return title.split(',')[0].strip()


def indicator(title):
    """ Take indicator from title; depends on number of commas. """
    indic = ''
    if len(title.split(',')) == 2:       
       indic = str(title.split(',')[-1].strip())
    elif len(title.split(',')) == 3:       
       split = re.split( ',(\s+)', title)
       indic = split[-3] + "," + split[-2] + split[-1]
    else:  indic = ''
    return indic


def rm_nest_dupli(seq1, seq2):
    """ fnc keeps titles based on pivot, i.e. first part before any comma
        seq2 - prefered list, i.e., always accepted
        seq1 - if no duplicate, accept """
    found = set()
    for item in seq2:
        found.add(pivot(item[1]))
    for item in seq1:
        if  pivot(item[1]) in found:  yield item[0]


def dupli_titles(search, replace_with, all_records):
    """ Find a title with 'search' subtring and another with 'replace_with' but that are otherwise identical.
        If there is a match, keep titles with 'replace_with', otherwise keep the one with 'search'.
        Returns list of record ids to remove.  """
    s   = []
    r   = []
    for item in all_records:
        if  search == indicator(item[1]):
            s.append(item)
        if replace_with == indicator(item[1]):
            r.append(item)
    return list(rm_nest_dupli(s,r))


def spec_currency(all_records):
    """ Special function for handling special conditions for currencies. """

    rm_currency = [ ]
    eur         = [ 'eur,','eurbn,','eur per', 'eurmn', 'eurbn', 'eur bn' ]
    for rec in all_records:
        if ( "gbp" in rec[1] ) and not ( 'cocoa' in rec[1]  ):  rm_currency.append(rec[0])
        if ( "cad" in rec[1] ) and not ( 'barley' in rec[1] ):  rm_currency.append(rec[0])
        if ( "myr" in rec[1] ) and not ( 'palm' in rec[1]   ):  rm_currency.append(rec[0])
        if ( "eur" in indicator(rec[1])                     )\
              or (  any( e  for e in eur if e in rec[1] )   ):  rm_currency.append(rec[0])
    return rm_currency


def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end


#_____________________________________________________________________________
#
#  Cleaning terms
#_____________________________________________________________________________

def cl_terms():

    indic_rep = [ "growth","% change y-o-y","% chg y-o-y","% y-o-y","y-o-y",'<loc',"5 year trailing CAGR,  %",\
        "5 year forward CAGR,  %","10 year forward CAGR,  %","at constant exchange rate,  US$bn" ]

    indic_name = [ 'Risk','Reward','Rating','Population','demographics','mortality','birth',\
        'death','healthy life','life expectancy','consumer spending','GDP','Private final consumption',\
        'Government final consumption','Fixed capital formation','Exports of goods and services',\
        'Imports of goods and services','Change in stocks','Statistical discrepancy','Total final consumption',\
        'Total domestic demand','Import duties','Consumer price index','Producer prices','Wholesale price index',\
        'M0','M1','M2','Money','M3','currency bond yield','money market rate','policy rate','Share prices',\
        'Total revenue','Total expenditure','Current expenditure','Capital expenditure','Budget balance',\
        'Primary balance','Goods imports','Goods exports','Balance of trade in goods','Trade in goods concentration',\
        'Services imports','Services exports','Balance of trade in services','Goods and services exports',\
        'Goods and services imports','Income account','transfers','Current account balance',\
        'Openness to international trade','Capital account','Financial account','FDI',\
        'Portfolio investment inflows','Portfolio investment outflows',\
        'Net portfolio investment','Total investment','Net other investment','Reserve assets',\
        "Net errors and omissions","Foreign reserves","Import cover","debt","STPR","LTPR","STER",\
        "LTER","BER","SRR","inflation","World exports","World imports","Government Revenue",\
        "Government Expenditure","GDP Methodology","goods exports","goods imports","Lending rate",\
        "Exchange rate","Expenditure scenario including governement spending","Manpower fit For military services",\
        "global average" ]
    #   "Other, US$mn ASSETS","LIABILITIES: Other, US$mn",
    
    return list( x.lower() for x in (indic_rep + indic_name) )




#_____________________________________________________________________________
#
#  Code Not Currently Being Used
#_____________________________________________________________________________

"""
def europe(all_records):
    ''' Special function for handling 'Europe' - may be needed if excluding this zone. '''
    rm_europe = []
    for rec in all_records:
        if   ( 'europe' == rec[1].split()[0] ):  rm_europe.append( rec[0] )
        elif ( 'european car' in rec[1] )         :  pass
        elif ( 'europe' in rec[1]) and (('in-bound' in rec[1]) or ('out-bound' in rec[1])):  pass
        elif ( 'european union' in rec[1] ):  rm_europe.append( rec[0] )
    return rm_europe
"""


"""
def cleaner( ids_titles = [] ):
"""
""" Input  - list of form [ ['id', 'title'], ... ] raw, uncleaned sublists
        Output - list of form [ ['id', 'title'], ... ] keep[] after cleaning   """
"""

    ids_titles_lower = [ [ x[0],x[1].lower() ] for  x in ids_titles ]

    remove = []
    for term in cl_terms():
        remove  += [ it[0] for it in ids_titles_lower if match(term.lower(), it[1]) ]

    # remove records
    ids_titles = remove_records( ids_titles, remove )
    ids_titles = remove_records( ids_titles, dupli_titles(  'units,  mn'  , 'units', ids_titles) )
    ids_titles = remove_records( ids_titles, spec_currency(  ids_titles)  )

    return ids_titles
"""

