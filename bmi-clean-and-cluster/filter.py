import itertools
from bmi_cleaner_helper import *


def filter_list_generator(data = []):
    for d in data:
        yield d
    print "stopping"

title = 'all_bmi_records3.txt'
records = get_records( title )

seq = [ int(s.strip()) for s in open('jnk').readlines() ]

print seq

print

seq.sort()

print seq.pop(-1)
print seq.pop(-1)


#seq = ['182077', '182119', '182455', '192221', '192284']
#seq = [ int(s) for s in seq ]

"""
d = {'id_chart':'222641'}

print
print


print 'look here ', d['id_chart'],function(d)
print d['id_chart'],seq

print
print
y = int(d['id_chart'])
print y
print binary_search(seq, y)
print
print
"""

#function = lambda x: int(x['id_chart']) not in seq #(x not in seq) 
function = lambda x: binary_search(seq, int(x['id_chart'])) < 0
numbers  = filter_list_generator(records)


records = filter(function, numbers)
for r in records:
    print r['title_url']

for r in records:
    print r
    print
#print "look again", records
#for r in records:
#    print r['id_chart']


