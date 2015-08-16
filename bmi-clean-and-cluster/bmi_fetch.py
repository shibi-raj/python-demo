import solr

import time

start_time = time.time()


s             = solr.SolrConnection('http://85.31.219.96:7183/solr')


def fetch_all_records():

    response      = s.query("id_chart:*", rows="10000", start='0')

    id_and_titles = "all_bmi_records_take2.txt"

    num_fetched   = 0
    f             = open(id_and_titles, 'w')

    #f.write( str(response.results).encode('utf8') + '\n\n' )
    
    while(len(response.results) > 0):
        num_fetched += 10000
        print num_fetched
        if  (num_fetched % 50000) == 0:
            print "time elapsed, sec:", time.time() - start_time
        for item in response.results:
           f.write( str(item).encode('utf8') + '\n\n' )
        response = response.next_batch()
    f.close()

    print "\ntime elapsed, sec: ", time.time() - start_time



def fetch_all_record_ids():

    response      = s.query("id_chart:*", fields="id_chart, title_url",rows="10000",start="709974")

    id_and_titles = "all_bmi_record_ids4.txt"

    num_fetched   = 710000
    f             = open(id_and_titles, 'w')

    while(len(response.results) > 0):
        num_fetched += 10000
        print num_fetched
        if  (num_fetched % 50000) == 0:
            print "time elapsed, sec:", time.time() - start_time
        for hit in response.results:
            try:
                f.write(str(hit['id_chart']).encode('utf8') + "	" + str(hit['title_url']).encode('utf8') + '\n')
            except UnicodeEncodeError:
                pass
        response = response.next_batch()
    f.close()

    print "\ntime elapsed, sec: ", time.time() - start_time


def fetch_one():
    response      = s.query("id_chart:*",rows="1",start="399990")
    for hit in response:
        print hit

def faceted_retrieval():
    
#    response = s.query("id_chart:*", facet='true', facet_field='best_desmetier', fields='best_desmetier',rows=1000)
    response = s.query("id_chart:*" , fields='best_desmetier, best_segment',rows=1000, facet='true', facet_limit='-1', \
                        ** {'facet.field' : ['best_desmetier']})

    return response.results


#________________________________


#fetch_one()
fetch_all_records()


#for each in faceted_retrieval(): 
#    print each
#    for key in each:
#        print key
#    for key in list.iterkeys:
#        print key




