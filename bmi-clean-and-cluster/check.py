"""  check.py

"""
import ast
import solr
import time
from   bmi_cluster_helper import *
from   taxonomy           import *
from   bmi_cleaner_helper import *

"""
title = 'tmp_test_fnc_dupli_titles.txt'


records = get_records(title, seq)

print len( records )
print len( cleaner(records) )
"""

#title = 'tmp2.txt'
#title = 'condensed_cleaned_premium_records.txt'
title = 'auto_condensed_cleaned_premium_records.txt'

#seq = ['id_chart','country', 'best_segment','best_desmetier', 'topic', 'title_url', 'id_industry', 'content']



#  get records
start   = time.time()

records = get_condensed_records( title)

print "get_records takes [s]:" , time.time() - start
print "number of records    :" , len(records)
print


#  clean records
start   = time.time()

#records = cleaner( records )

#print "cleaner takes [s]:" , time.time() - start
#print "number of records:" , len(records)
#print

#  cats_topics_titles('United_States', '2302', records)
ind_ids = [2306,2309,2308,2307,\
           2310,2304,2303,2301,2302,\
           2297,2299,2298,2296]
ind_nme = ["Auto Electronic and Electric Equipment","Automobile  Brake","Automobile Engine","Tire",\
           "Clean Vehicle","Heavy Truck and Bus","Light Truck and Van","Motorcycle","Passenger Car",\
           "Automotive Dealer","Automotive Part Store","Automotive Repair and Maintenance",\
           "Vehicle Renting and Leasing"]

ind = []
#ind = [[2257,'Pharmaceutical']]

for i, indus in enumerate(ind_ids):
    ind.append([ind_ids[i], ind_nme[i]])


top5 = ['United States', 'China', 'Japan', 'Germany', 'South Korea']


for country in top5:
    for each in ind:
        print each[1].upper()
        cat_top_tle(country, each, records)





"""
"""

"""
ind_ids = [2306,2309,2308,2307,2310,2304,2303,2301,2302,2297,2299,2298,2296]

ind_nme = ["Auto Electronic and Electric Equipment","Automobile  Brake","Automobile Engine","Tire","Clean Vehicle","Heavy Truck and Bus","Light Truck and Van","Motorcycle","Passenger Car","Automotive Dealer","Automotive Part Store","Automotive Repair and Maintenance","Vehicle Renting and Leasing"]
"""

"""
#title   = 'condensed_cleaned_premium_records2.txt'
title = 'all_catalog_records.txt'
records =  get_records(title)

seq     = ['title_url','topic', 'best_segment']

c = 0
for r  in records:
    try:
        for e in r['id_industry']:
            if  str(e) == '2302': c += 1
    except: pass
print c
"""

"""
#title = 'all_premium_records.txt'
out_title = 'jnk.txt'
out_file  = open(out_title, 'w')

title = 'all_premium_records.txt'


start   = time.time()

records = get_records( title )

print "get_records takes [s]:" , time.time() - start
print "number of records    :" , len(records)
print



start   = time.time()

records = cleaner( records )

print "cleaner takes [s]:" , time.time() - start
print "number of records:" , len(records)
print



for item in records:
  out_file.write("%s\n" % item)    
"""




"""
#print records
title = 'ind_names_ids.txt'
ind_ids_names = [ x.split() for x in open(title).readlines()]
ind_ids_names.sort()


tmp = []
records = sorted(records, key=lambda k: k['id_chart'] )
for r in  records:
    tmp.append(r['id_chart'])
    #print r['id_chart']

x =240558
print tmp
tmp.pop(binary_search(tmp, x, lo=0, hi=None))

print tmp
"""

#for each in ind_ids_names:
#    out_segment_topics( each, loc_topic_facet( each[1], records ) )
    

#id_ind = 2302


#for string in get_records( title ):
#    d = str_to_dict( string )
    
#d          = related_ids( 'United_States', '2302', topics )

"""
search_desmetier_segment( 1155 )

title       =  'all_bmi_records.txt' 
all_records = [ rec.strip().split("\t") for rec in open(title).readlines() ]
all_records_orig = list(all_records)

all_records = [ [ x[0],x[1].lower()   ] for x   in all_records  ]
all_records.sort()

for a in all_records_orig:
    print a

for ar in all_records:
    if 'commercial vehicle sales' in ar[1]: 
        if 'units' in ar[1]: 
            if 'united states' in ar[1]: print indicator(ar[1])
"""

"""
dt = dupli_titles('units,  mn', 'units', all_records)
print dt

    if 'units,  mn'  in ar[1]:    print ar

dt = dupli_titles('units,  mn', 'units', all_records)
for d in dt:
    print d
"""

"""
"""

#if __name__ == '__main__':



"""
# Setup

title       =  'all_bmi_records.txt' 
all_records = [ rec.strip().split("\t") for rec in open(title).readlines() ]
all_records = [ [ x[0],x[1].lower()   ] for x   in all_records ]

f        = []

#terms = ['europe']
#terms    = geo_zones + indic_rep + indic_name
terms    = [ t.lower() for t in terms ] 

all_excl = OP_Handler( 'excluded/', 'main_file' )
keep     = OP_Handler( './'       , 'keep'      )
#_____________________________________________________

# Cleaning

print 'beginning count of records ', len(all_records)

for i, item in enumerate(terms):
    f.append(  OP_Handler('excluded/',item) )
    remove  =  []
    for rec  in all_records:
        if item in rec[-1]:
            f[i].record(     str(rec[0])+'\t'+str(rec[-1]) )
            all_excl.record( str(rec[0])+'\t'+str(rec[-1]) )
            remove.append(rec[0])
    all_records = [ it for it in all_records if it[0] not in remove ]
    print item, len(all_records)

remove = europe(all_records)
print len(all_records)

print 'final count of records     ', len( all_records )
#_____________________________________________________
"""
# Clean up
"""
for rec in all_records:
    keep.record( str(rec[0])+'\t'+str(rec[-1]) )
keep.cleanup()

for file in f:
    file.cleanup()
"""

