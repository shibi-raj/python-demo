class BreakIt(Exception): pass



import os
import json
from   bisect import *

rd_json = '/home/srarlk/data/bmi/rdBMI/json'
rd_xml  = '/home/srarlk/data/bmi/rdBMI/xml'

class solrGroupTransfer():

    def __init__(self,dataset):
        self.group_fields = ["group_id", "country", "type",    "industry"]
        self.doc_fields   = ["id_chart", "title",   "country", "seg",     "last_data"]
        self.get_fields   = ["country", "industry", "id_chart", "title", "seg", "last_data"]
        self.d            =   dict( (x,"") for x in self.get_fields ) 

    def getFields(self):
        """Returns dictionary of the import fields from the R&D Elastic Search
        output.
        """
        for gf  in self.get_fields:
            try:    
                if gf == 'country' or gf == 'industry':  
                    self.d[gf] = self.formatString(dataset[gf]['name'])
                else:
                    self.d[gf] = dataset[gf]
            except: pass
        return self.d

    def formatString(self, string):
        ls = string.strip().split()
        return '_'.join([l.lower() for l in ls])

def setData(number):
    fname = "chart1_%s.json" % number
    json_path = os.path.join(rd_json,fname)
    rd_data=open(json_path, 'r')
    data = json.load(rd_data)
    rd_data.close()
    return data['hits']['hits'][0]['_source']['dataset']



import xml.etree.cElementTree as ET

class solrInput():

    def __init__(self,rd_xml,fname):
        self.rd_xml = rd_xml
        self.fname  = fname        
        self.tree   = ET.ElementTree(file=rd_xml+fname)
        self.r      = self.tree.getroot()
        self.counter = 0

    def addRecord(self,d):
        """Handles main procedures for inserting new data from dictionary.  

        Search for existing group to place data.  If no group, create one.

        Input fields are: id_chart, title, country, industry, seg, and
        'last_data' which is a list (method 'insertSubdoc()').
        """
        try:
            self.d        = d
            self.country  = d['country']
            self.industry = d['industry']
            grp = self.findGroup()  
            self.doInsert(grp)
        except:  
            if  self.counter == 0:
                self.counter += 1
        print 'look here',self.d['id_chart']
        """
        """
        return self.counter

            
    def makeNewGroup(self):
        pass

    def findGroup(self):
        """Search xml for a matching triplet of fields, i.e., find the 
        insertion point.  If there is not already a match, create a doc.
        """
        the_o_doc = ""
        try:
            for o_doc  in self.getOuterDocs():
                pfs =  []
                for field in o_doc.iterfind('field'):
                    pfs.append(field.text)
                    if  self.isTriple(pfs):  
                        the_o_doc = o_doc
                        raise BreakIt
            if not the_o_doc: the_o_doc = ET.SubElement(self.r,'doc')
        except BreakIt: pass
        return the_o_doc

    def isTriple(self,pfs):
        """Check if current triplet of fields in xml file matches."""
        the_triple     =  False
        if set(pfs)    == set(['parent',self.country,self.industry]):  
            the_triple =  True
        return  the_triple

    def getOuterDocs(self):
        """Get iterator for current outer docs."""
        return (self.tree.iterfind('doc'))

    def doInsert(self,grp):
        """Insert according to solr schema requirements.  Modify called methods
        for changes to desired output.
        """
        parent = ET.SubElement(grp,'doc')
        self.insertTriple(parent)
        sub_doc = ET.SubElement(parent,'doc')
        self.insertSubdoc(sub_doc)

    def insertTriple(self, parent):
        """Insert data triplet (identifier) for SOLR block-join."""
        ET.SubElement(parent,'field',{'name':'type'}).text='parent'
        ET.SubElement(parent,'field',{'name':'country'}).text=self.country
        ET.SubElement(parent,'field',{'name':'industry'}).text=self.industry

    def insertSubdoc(self,sub_doc):
        """Insert rest of data fields under type <doc>, i.e., a subdoc."""
        ET.SubElement(sub_doc,'field',{'name':'id_chart'}).text=str(self.d['id_chart'])
        ET.SubElement(sub_doc,'field',{'name':'title'}).text=self.d['title']
        ET.SubElement(sub_doc,'field',{'name':'country'}).text=self.d['country']
        ET.SubElement(sub_doc,'field',{'name':'seg'}).text=self.d['seg']
        for data_point in self.d['last_data']:
            ET.SubElement(sub_doc,'field',{'name':'last_data'}).text=str(data_point)



if __name__ == '__main__':

    import logging
    logging.basicConfig(level=logging.DEBUG)


    retrieve_fields = ["country", "industry"]

    sets = range(1000,2000)

    rd_xml = '/home/srarlk/data/bmi/rdBMI/'
    fname  = 'monfichier.xml'

    y = solrInput(rd_xml,fname)

    for s in sets:
        dataset = setData(s)
        d = solrGroupTransfer(dataset).getFields()
        y.addRecord(d)
        
    y.tree.write('outTree.xml')

    """
    try:
        y.tree.write('outTree.xml')
    except TypeError as te:
        print logging.debug(te)
        print logging.info(te)
        print logging.warning(te)
        print logging.error(te)
    """
        


