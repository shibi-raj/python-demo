#  Cleaning rules for BMI file names
import solr
import numpy as np

class Cleaning_Rules:

    def __init__(self, db, primary_list = []):
        self.db = db
        self.pl = primary_list

    def carg_5_trailing(self):
        self.phrase   = '5 year trailing CAGR,  %'
        self.response = self.db.query("title_url:(5 AND year AND trailing AND CAGR)")
        return self.search_responses()

    def carg_5_forward(self):
        self.phrase   = '5 year forward CAGR,  %'
        self.response = self.db.query("title_url:(5 AND forward AND year AND CAGR)")
        return self.search_responses()

    def carg_10_forward(self):
        self.phrase   = '10 year forward CAGR,  %'
        self.response = self.db.query("title_url:(10 AND year AND forward AND CAGR)")
        return self.search_responses()

    def const_exch_rate(self):
        self.phrase   = 'at constant exchange rate'
        self.response = self.db.query("title_url:(10 AND year AND forward AND CAGR)")
        return self.search_responses()

    def yoy(self):
        self.phrase   = '% change y-o-y'
        self.response = self.db.query("% change y-o-y")
        return self.search_responses()

    def growth(self):
        self.phrase   = ',  % growth'
        self.response = self.db.query("title_url:(growth)")
        return self.search_responses()

    # -------------------------

    def search_responses(self):
        self.exclude = []
        #print "Number Results from search:               ", self.response.numFound
        while   len(self.response.results) > 0:
            for hit in self.response.results:
                #if(self.is_match(hit)):  
                    #print hit['title_url']
                self.exclude.append(hit['id_chart'])
            self.response = self.response.next_batch()
        return self.exclude

    def is_match(self, hit):
        match = False
        if (self.phrase in hit['title_url']):  
            match = True
        return match

    def drop(self, remove_items = []):
        for each in remove_items:
            try:   self.pl.remove(each)
            except ValueError as eVE:   pass
        return self.pl

    def write_out(self, tmp_file = 'default_out.txt'):
        f = open(tmp_file, 'w')
        for element in self.pl:
            f.write(str(element)+'\n')
        f.close()

    def carg_5_trailing_2(self):
        self.phrase   = '5 year trailing CAGR,  %'
        query_string  = "title_url:(5 AND year AND trailing AND CAGR)"
        self.response = self.db.query(query_string)
        self.exclude  = []
        ii=0
        while ii < 10:
#        while len(self.response.results) > 0:
            for hit in self.response.results:
                self.exclude.append([hit['id_chart'], hit['title_url']])
            ii+=1
            self.response = self.response.next_batch()
        return self.exclude
        #return self.search_responses()


#-------------------------

if __name__ == '__main__':

    s           = solr.SolrConnection('http://85.31.219.96:7183/solr')
    all_records = [ int(rec_id.strip()) for rec_id in open('all_bmi_record_ids_sorted.txt').readlines() ]

    #a = [x for x in xrange(0,10)]
    #b = [x for x in xrange(5,10)]

    x           = Cleaning_Rules(s, all_records)
    for each in x.carg_5_trailing_2():
        print each
    #x.write_out('tmp_out.txt')

    








"""
topics = ['production', 'sales', 'exports', 'imports']
#x = Cluster(
#exclude_titles = ['y-o-y','mn']
exclude_titles = [
                  'Risk','Reward','Rating','Population','demographics','mortality','birth',\
                  'death','healthy life','life expectancy','consumer spending','GDP','Private final consumption',\
                  'Government final consumption','Fixed capital formation','Exports of goods and services',\
                  'Imports of goods and services','Change in stocks','Statistical discrepancy','Total final consumption',\
                  'Total domestic demand','Import duties','Consumer price index','Producer prices','Wholesale price index',\
                  'M0','M1','M2','Money','M3','currency bond yield','money market rate','policy rate','Share prices',\
                  'Total revenue','Total expenditure','Current expenditure','Capital expenditure','Budget balance',\
                  'Primary balance','Goods imports','Goods exports','Balance of trade in goods',\
                  'Trade in goods concentration',\
                  'Services imports','Services exports','Balance of trade in services','Goods and services exports',\
                  'Goods and services imports','Income account','transfers','Current account balance',\
                  'Openness to international trade',\
                  'Capital account','Financial account','FDI','Portfolio investment inflows',\
                  'Portfolio investment outflows',\
                  'Net portfolio investment','Total investment','Net other investment','Reserve assets'
                 ]

excl_regions = [
                "Europe","Western Europe","MENA","Sub-Saharan Africa","SSA","Asia-Pacific","Latin America",\
                "Developed markets","Emerging states","Emerging economies","Frontier Markets","OECD",\
                "G7","NAFTA","OPEC","BRIC","EU-27","EU-15","Nordic region","CIS States","Baltic States",\
                "Emerging Europe","Central Europe","Caucasus","Central Asia","South Eastern Europe",\
                "Western Balkans","Middle East",'GCC',"North Africa","Gulf","East Med","East and Central Africa",\
                "West Africa","CFA Franc Zone",'COMESA','ECOWAS','EAC','SADC','SACU',"African Continent",\
                "Emerging Asia",'ASEAN-10','ASEAN-5',"North East Asia",'South East Asia',"South Asia",\
                "Central America","DR-CAFTA","Carribean","Southern Cone","Andean","Mercosur","Central America",\
               ]

"""

"""
#response = s.query('id_chart:[ 40000 TO * ] AND id_industry:2302 AND lst:premium')
#response = s.query('id_chart:41685')
#response = s.query('lst:premium')
#response = s.query('id_chart:[ 40000 TO * ] AND id_industry:2302 AND lst:premium')
#response = s.query('id_industry:2302 AND country:Brazil', facet='true', facet_field='topic')
#response = s.query("title_url:((5 OR 10) AND year forward trailing CAGR)")
#response = s.query("title_url:((5 OR 10) AND (forward OR trailing) AND year AND CAGR) and title_url:(\% change y-o-y)")
"""

"""
indicator_rep = [
    "title_url:(5 AND year AND trailing AND CAGR)",\
    "title_url:(5 AND forward AND year AND CAGR)",\
    "title_url:(10 AND year AND forward AND CAGR)",\
    "title_url:(at AND constant AND exchange AND rate AND  US$bn)",\
    "title_url:(% AND change AND y-o-y)",\
    "title_url:(growth)"
]
"""


#response = s.query("id_chart:*", fields="id_chart", rows="1000", score="false")
#print response.numFound


