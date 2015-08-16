
import operator

def list_to_dict( even_list = [] ):
    """ Converts list to dictionary, pair-wise.  Returns empty
        dictionary if list does not have even number of elements """

    d = {}
    if  len(even_list) % 2 == 0:
        d = dict(zip( even_list[::2], even_list[1::2]))
    d = { k:v for k,v in d.items() if str(v)!='0' }
    return d


def sort_dict( d = {} ):
    """ Sort dictionary based on value """
    """ Converting to dictionary destroys order """
    sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
    return sorted_d

