from bmi_cluster_helper import get_records, get_condensed_records
from bmi_cleaner_helper import cleaner


def thin_premium_records(in_fname = 'all_premium_records.txt'):

    out_name = 'tmp_condensed_premium_records.txt'

    # Optional input:        specify fields desired in output
    seq     = [ 'id_chart', 'title_url',    'id_industry',    'industry',\
                'topic',    'best_segment', 'best_desmetier', 'country', \
                'content' ]

    records =  get_records(in_fname, seq)

    fout    = open(out_name, 'w')
    for r  in records:
        fout.write(str(r)+'\n')

    return out_name



def clean_records(records = [], out_name = 'tmp_condensed_cleaned_premium_records.txt',\
                                in_fname = 'condensed_premium_records.txt'):

    if not records:  records =  get_condensed_records(in_fname)

    records = cleaner(records) 

    fout    = open(out_name, 'w')
    for r  in records:
        fout.write(str(r)+'\n')

    return out_name



def iso_recs_by_ind(records = [], out_name = 'auto_condensed_cleaned_premium_records.txt',\
                                  in_fname = 'tmp_condensed_cleaned_premium_records.txt'):


    ind_ids = [2306,2309,2308,2307,2310,2304,2303,2301,2302,2297,2299,2298,2296]
    ind_nme = ["Auto Electronic and Electric Equipment","Automobile  Brake","Automobile Engine","Tire",\
               "Clean Vehicle","Heavy Truck and Bus","Light Truck and Van","Motorcycle","Passenger Car",\
               "Automotive Dealer","Automotive Part Store","Automotive Repair and Maintenance",\
               "Vehicle Renting and Leasing"]

    ind = []

    for i, indus in enumerate(ind_ids):
        ind.append([ind_ids[i], ind_nme[i]])


    if not records:  records =  get_condensed_records(in_fname)

    function = lambda x: try_filter(x, ind_ids )

    rec_gen = filter_list_gen(records)
    print 'before: ',len(records)
    records = filter(function, rec_gen)
    print 'after : ',len(records)

    fout    = open(out_name, 'w')
    for r  in records:
        fout.write(str(r)+'\n')

    return out_name



def filter_list_gen( records = []):
    for r in records:
        yield r



def try_filter( r = {}, ind_ids = [] ):

    good = False    
    try:
        if  any( ident for ident in ind_ids if ident == int(r['id_industry'][0]) ):
            good = True
    except:
        pass
    return good



#_____________________


#thin_premium_records()


#for r in jnk():
#    print r['id_industry']

