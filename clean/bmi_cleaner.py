"""  bmi_cleaner.py

Main code for cleaning BMI titles
"""

import time
from   bmi_cleaner_helper import *

start_time = time.time()

geo_zones = []
"""
    "Europe",\
    "Africa", "Middle East",\
    "Western Europe","MENA","Sub-Saharan Africa","SSA","Asia-Pacific",\
    "Latin America","Developed markets","Emerging states","Emerging economies",\
    "Frontier Markets","OECD","G7","NAFTA","OPEC","BRIC","EU-27","EU-15",\
    "Nordic region","CIS States","Baltic States","Emerging Europe","Central Europe",\
    "Caucasus","Central Asia","South Eastern Europe","Western Balkans","Middle East",\
    "GCC","North Africa","Gulf","East Med","East and Central Africa","West Africa",\
    "CFA Franc Zone","COMESA","ECOWAS","EAC","SADC","SACU","African Continent",\
    "Emerging Asia","ASEAN-10","ASEAN-5","North East Asia","South East Asia",\
    "South Asia","Central America","DR-CAFTA","Carribean","Southern Cone","Andean",\
    "Mercosur","Central America","North America"
"""

indic_rep = [
    "growth","% change y-o-y","% chg y-o-y",'<locccur>',"5 year trailing CAGR,  %",\
    "5 year forward CAGR,  %","10 year forward CAGR,  %","at constant exchange rate,  US$bn"
]

indic_name = [
    'Risk','Reward','Rating','Population','demographics','mortality','birth',\
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
    "Other, US$mn ASSETS","LIABILITIES: Other, US$mn","global average" 
]



# Setup

title         =  'all_bmi_records.txt' 
all_records   = [ rec.strip().split("\t") for rec in open(title).readlines() ]
all_records_o =   list(all_records)

all_records   = [ [ x[0],x[1].lower()   ] for x   in all_records ]

f             = [ ]
terms         =   geo_zones + indic_rep + indic_name
terms         = [ t.lower() for t  in terms ] 

all_excl = OP_Handler( 'excluded/', 'main_file' )
keep     = OP_Handler( './'       , 'keep'      )



# Cleaning

print 'beginning count of records ', len(all_records)

for ar in all_records:
    print ar

for i,  item  in enumerate(terms):
    # Each title has its own file
    f.append( OP_Handler('excluded/',item) )  
    remove =  []
    for rec in all_records:
        if  item in  rec[-1]:
            f[i].record(     str(rec[0])+'\t'+str(rec[-1]) )
            all_excl.record( str(rec[0])+'\t'+str(rec[-1]) )
            remove.append(rec[0])
    all_records = [ it for it in all_records if it[0] not in remove ]
    print item, len(all_records), time.time() - start_time


#  Treat titles with same meaning but just in different units
print 'dupli titles'
remove      =   dupli_titles( 'bn bbl'     , 'mn bbl', all_records ) \
              + dupli_titles( 'tcm'        , 'bcm'   , all_records ) \
            #  + dupli_titles( 'units,  mn' , 'units' )
all_records = [ it for it in all_records if it[0] not in remove ]
print time.time() - start_time


# Treat special currencies
print 'spec_currency'
remove      = spec_currency(all_records)
all_records = [ it for it in all_records if it[0] not in remove ]
print time.time() - start_time


# Treat mention of 'europe'
print 'europe'
remove      = europe(all_records)
all_records = [ it for it in all_records if it[0] not in remove ]
print time.time() - start_time


print 'final count of records     ', len( all_records )



# Clean up

for rec in all_records:
    keep.record( str(rec[0])+'\t'+str(rec[-1]) )
keep.cleanup()

for file in f:
    file.cleanup()

print 'total time: ', time.time() - start_time

