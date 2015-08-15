from contextlib import closing
import MySQLdb
import time
import  pickle
import logging

logging.basicConfig(level=logging.DEBUG)

currencies = []

def good_title(bmi):
    """Keep titles that do not have terms from cl_terms()"""
    good = True
    for term in cl_terms():
        if  is_match( term, bmi.title.lower() ): 
            good = False
            break
    if  good: good = handle_currency(bmi)
    if  good: good = handle_unit(bmi)
    return  good

def is_match(string, title):
    """Search for sub-string 'string' of 'title.'"""
    try:
        if  string and (string in title):  
            string = True
        else:  
            string = False
    except Exception, e:  
        logging.exception(e)
    return string

def handle_currency(bmi):
    """Special function for handling special conditions for currencies."""
    good  = True
    eur   = [ 'eur,','eurbn,','eur per', 'eurmn', 'eurbn', 'eur bn', 'eur/' ]
    try:
        title_lower = bmi.title.lower()
        if "eur" in bmi.unit.lower():  
            good = False
        elif any( e  for e in eur if e in bmi.title.lower() ):
            good = False
        elif title_lower[-3:] == "eur":
            good = False
        if  good: # all other currencies
            ex_curr = get_invalid_currency(bmi.country)
            if any(x in title_lower for x in ex_curr):  
               good = False
            if good and bmi.country.lower() == "iran" and ("irr" in title_lower) : # Iranian currency
               good = False
            if good and "/us" in title_lower: # move ratios to us currency
               good = False
    except Exception, e:  
        logging.exception(e)
    return good

def handle_unit(bmi):
    good = True
    excl_cur = get_invalid_currency(bmi.country)
    #print [ec for ec in excl_cur if ec in bmi.unit.lower() ]
    if any( [ ec for ec in excl_cur if ec in bmi.unit.lower() ] ):
        good = False
    return good

def get_invalid_currency(country):
    excl_cur = []
    for pc in pickle_curry():
        if any([ p  for p in pc if p == country.lower() ]): excl_cur.append(pc[0])
    return excl_cur

def pickle_curry():
    global currencies
    currency = './currency_list.dat'
    with open(currency,'r') as filename:
        currencies = pickle.load(filename)
    return currencies

def cl_terms():

    terms = ('y-o-y', 'exchange rate', 'cagr', ' ber,',\
             'at constant exchange rate,  us$bn', 'risk', 'gdp', 'consumer price index', 'units,  mn', 'units mn',\
             'population', 'growth', 'reward', 'birth', 'debt', 'inflation', 'rating', 'consumer spending', 'death',\
             'producer prices', 'ster', 'private final consumption', 'exports of goods and services',\
             'imports of goods and services', 'government final consumption', 'fixed capital formation', 'mortality',\
             'healthy life', 'popn', 'life expectancy', 'change in stocks', 'money', 'm1', 'lter', 'm2', 'transfers',\
             'reserve assets', 'm3', 'capital account', 'statistical discrepancy', 'current expenditure',\
             'total investment', '<loc', 'demographics', 'bn bbl', 'total final consumption', 'total domestic demand',\
             'import duties', 'wholesale price index', 'm0', 'currency bond yield', 'money market rate', 'policy rate',\
             'share prices', 'total revenue', 'total expenditure', 'capital expenditure', 'budget balance',\
             'primary balance', 'goods imports', 'goods exports', 'balance of trade in goods',\
             'trade in goods concentration', 'services imports', 'services exports', 'balance of trade in services',\
             'goods and services exports', 'goods and services imports', 'income account', 'current account balance',\
             'openness to international trade', 'financial account', 'fdi', 'portfolio investment inflows',\
             'portfolio investment outflows', 'net portfolio investment', 'net other investment',\
             'net errors and omissions', 'foreign reserves', 'import cover', 'stpr', 'ltpr', 'srr', 'world exports',\
             'world imports', 'government revenue', 'government expenditure', 'gdp methodology', 'goods exports',\
             'goods imports', 'lending rate', 'expenditure scenario including governement spending',\
             'manpower fit for military services', 'global average', 'other,')

    return terms

def sheets_excl():
    excluded = ('GDP','GDP at PPP','GDP Expenditure','GDP By Output','Population','Labour Force',\
                'Wages','Stratification','Inflation & CPI Breakdown','Money Supply','Interest Rates',\
                'Equity Markets','Exchange Rate','Fiscal','BoP','FDI Stock','Foreign Reserves',\
                'Debt','Ratings','Global Regional Indicators')
    return excluded




