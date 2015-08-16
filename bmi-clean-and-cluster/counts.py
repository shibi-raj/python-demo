import ast
import solr
import time
from   bmi_cluster_helper import *
from   taxonomy           import *
from   bmi_cleaner_helper import *

"""
"""        

title = 'all_cleaned_premium_records.txt'

start   = time.time()

records = get_cleaned_records(title)

print "get_cleaned_records takes [s]:" , time.time() - start
print "number of records            :" , len(records)
print


seq     = ['id_chart'    , 'title_url', 'id_industry', 'industry', 'topic',\
           'best_segment', 'best_desmetier' ]
lseq    = len(seq)

d          = {}

count_all  = 0
c_top_both = 0
c_top_neth = 0
c_top_segm = 0
c_top_desm = 0
c_no_topic_nor_sd_match = 0

bd         = []

for r in records:

    iseq     = [0]*lseq
    tmp_keys = []

    for i, key in enumerate(r.iterkeys()):
        tmp_keys.append(key)
        """
        if    key not in d: 
              d[key]  = 1 
        else: d[key] += 1
        """

    for i,  s in enumerate(seq):
        if  s in tmp_keys: iseq[i] = 1
 
    if  iseq[4] == 0: # only care about the case where no topic field
        if iseq[5] == 1 and iseq[6] == 1: c_top_both +=1
        if iseq[5] == 0 and iseq[6] == 0: c_top_neth +=1
        if iseq[5] == 1 and iseq[6] == 0: c_top_segm +=1
        if iseq[5] == 0 and iseq[6] == 1: c_top_desm +=1

        bsd     = []
        sd_keep = []

        for i in xrange(5, 7):
            if iseq[i] == 1:
                for rs in r[seq[i]]:
                    if rs not in bsd:  bsd.append(rs)
        bsd = rm_list_underscores(bsd)
        
        for sd in bsd:
            if sd in r['title_url'].lower():  sd_keep.append(sd)
        if sd_keep:
            sdmax =  max(sd_keep, key=len)
            if  sdmax not in d:
                  d[sdmax]  = 1
            else: d[sdmax] += 1
        else:   
            c_no_topic_nor_sd_match  +=1


#_________________________


sorted_x = sorted(d.iteritems(), key=operator.itemgetter(1))
sorted_x.reverse()

for topic in sorted_x:
    print topic[0],':', topic[1]

print
print "Number of topics now extended   :", len(sorted_x)


print 'Those without topic, but with seg and desm   :', c_top_both
print 'Those without topic, and without both        :', c_top_neth
print 'Those without topic, but with segment only   :', c_top_segm
print 'Those without topic, but with desmetier only :', c_top_desm
print
print 'Those without topic, and no seg or desm match:', c_no_topic_nor_sd_match
print

print 'Here is the seq list                         :', seq

