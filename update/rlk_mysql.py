from contextlib import closing
import MySQLdb
import time
import  pickle
import logging

logging.basicConfig(level=logging.DEBUG)



#  Functions for SQL statement execution.

def sql_results(db, sql):  
    """Generic, reusable function for MySQL querying and returning the 
    results.
    """
    results = []
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
    except Exception, e: 
        logging.exception(e)
        results = []
    return results

def sql_execute(db, sql):  
    """Generic, reusable function just for MySQL statement executions."""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        cursor.close()
    except Exception, e: 
        logging.exception(e)
        print "error for query:  ",sql



#  Related functions for matching BMI titles to those in the RLK database.

def sql_title_match(db, title, table='chart1'):
    """Makes title query and returns [title, source, id_chart] of the match"""
    pmatch  =  False
    sql     =  sql_split_title( title, table )    
    results =  sql_results(db, sql)
    x = [ p.lower().strip() for p in title.split(',')   ]
    for each in results:
        y = [ q.lower().strip() for q in each[0].split(',') ]
        if  set(x)  == set(y):
            pmatch =  [each[0], each[1], each[-1]]
            break
    return pmatch

def sql_split_title(title, table='chart1'):
    """Produces the MySQL query string from title components."""
    split =   title.split(',')
    split = [ x.strip() for x in split]
    sql   =  "select name, sa, id_chart from %s where name like '%s'"\
          % (table, split[0]  +  "%")  
    return sql



#  Functions for operations acting on the RLK database.

def get_last_id(db, table='chart1', id_label='id_chart'):
    """Fetch highest id from table."""
    sql = "select %s from %s order by %s desc limit 1" % (id_label,table,id_label)
    return sql_results(db, sql)[0][0]

def insert_chart_data1(db, table, id_chart, data_values, data_time, source):
    """Insert new data into BMI data table.""" 
    if  not source:  
        source = "'Publisher > BMI'"
    else:
        source = "'"+source+"'"
    columns = "id_chart, value, dim_1_1, value_source, value_insert"
    sql =  "insert into %s (%s) values (%s, %s, %s, %s, %s)" \
            % (table, columns, id_chart, data_values[0], data_time[0], source, "Now()")
    for data, time  in zip(data_values[1:], data_time[1:]):
        sql +=  ", (%s, %s, %s, %s, %s)" % (id_chart, data, time, source, "Now()")
    sql_execute(db, sql)
    return len(data_values) == len(data_time)

def insert_chart1(db, obj, table='chart1'):
    """Insert data into BMI info table."""
    fields = ['name', 'description', 'comments', 'source', 'update_rate']
    fields =  fields + ['unit', 'lst', 'bm', 'price', 'id_editeur', 'sa']
    values = [obj.title, obj.description, obj.comments,obj.source,\
              obj.update_rate, obj.unit, obj.lst, obj.bm, obj.price,\
              obj.id_editeur, obj.sa]
    tmp_f = []
    tmp_v = []
    for i, v  in enumerate(values):
        if v: 
            tmp_f.append(fields[i])
            tmp_v.append(str(v))
    fields = ",".join(tmp_f)
    values = "'" + "','".join(tmp_v) + "'"
    sql    = "insert into %s (%s) values (%s)" % (table,fields,values)
    try:
        sql_execute(db, sql)
        new_id   = int(get_last_id(db, table=table))
    except Exception, e: 
        logging.exception(e)            
        print     
    return new_id

def delete_data(db, id_chart, table="chart_data1"):
    sql = "delete from %s where id_chart = %s" % (table,id_chart)
    sql_execute(db, sql)



#  Final numbers checks

def equiv_data(l1, l2):
    equiv = True
    if  len(l1) != len(l2):
        equiv = False
    else:
        for v1, v2 in zip(l1,l2):
            if  abs(v1-v2) > .1:
                equiv = False
    return equiv


def get_data(db,id,table='chart_data1', field='dim_1_1'):
    sql = "select value,dim_1_1 from %s where id_chart = %s order by %s asc" % (table,id,field)
    data = sql_results(db, sql)
    data = zip(*data)
    #print "inside get_data: ", data
    return data




class Sheet_Info:
    def __init__(self, name):
        self.name = name
        self.kept = None
        self.new  = None
        self.repl = None
        self.disc = None
        self.ex   = None

        self.last_data_id  = None
        self.start_data_id = None

        self.last_id_chart  = None
        self.start_id_chart = None
  
        self.time_seq = []

    def add_up(self):
        self.new_repl = (int(self.kept) == int(self.new) + int(self.repl))
        self.data_align = (self.last_data_id - self.start_data_id)/len(self.time_seq)
        self.data_numbers = ( self.data_align == self.new + self.repl)
        self.del_id_chart = (self.last_id_chart - self.start_id_chart)
        self.records = ( self.del_id_chart == self.new)

    def __repr__( self ):
        string =  "Sheet Info: \n name = '%s' \n kept = %s \n new = %s \n replaced = %s \n discarded = %s"
        string += "\n exceptions = %s "%\
                (self.name, self.kept, self.new, self.repl, self.disc, self.ex)
        string += '\n\n Is Kept = New + Replaced? %s' % self.new_repl

        string += '\n\n Records End      = %s' % self.last_id_chart
        string += '\n Records Start    = %s'   % self.start_id_chart
        string += '\n Change in id_chart ?= New records?  %s, %s'   % (self.records, self.del_id_chart)
        
        string += '\n\n Data End      = %s' % self.last_data_id
        string += '\n Data Start    = %s'   % self.start_data_id
        string += '\n len(time_seq) = %s'   % len(self.time_seq)
        string += '\n\n Is New + Replaced ?= (End - Start)/len(time_seq):  %s, %s' % (self.data_numbers,self.data_align)
        
        return string


def add_it_up(db, sheet_name, kept, new, repl, disc, ex, time_seq, start_id_chart, start_data_id):
    """Do numbers check for each sheet:
       kept - tot. # kept from sheet
       new  - # kept and new to MySQL db
       repl - # of titles replaced in MySQL db
       disc - tot. # of discarded titles
       ex   - # exceptions raised
    """
    si = Sheet_Info(sheet_name)
    si.kept = kept
    si.new  = new
    si.repl = repl
    si.disc = disc
    si.ex   = ex

    si.last_data_id  = get_last_id(db, table='chart_data1', id_label='data_id')
    si.start_data_id = start_data_id

    si.last_id_chart   = get_last_id(db, table="chart1", id_label='id_chart') 
    si.start_id_chart  = start_id_chart

    si.time_seq = time_seq
    si.add_up()
    return si




