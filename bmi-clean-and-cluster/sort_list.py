"""  sort_list.py

Reading list from file, sorting it, and writing it to another file
"""

import time
import bisect

li = [ x.split('\t') for x in open('excluded/main_file').readlines() ]

li.sort( key=lambda x: int(x[0]) )

for l in li:
    print l[0]

#start_time = time.time()
#print time.time() - start_time, "seconds"

#_________________________

if  __name__ == '__main__':
    pass

