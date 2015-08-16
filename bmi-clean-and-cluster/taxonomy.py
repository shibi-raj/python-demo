"""  taxonomy.py

class TaxoIds: matches codes to their names and vice versa from taxonomy xls file.

taxo_row(n): returns row n of the taxo xls

taxo_col(n): returns col n of the taxo xls

Notes for xlrd:
    Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
    cell_value = ws.cell_value(this_row, this_cell)
    cell_type  = ws.cell_type(this_row,  this_cell)
"""

import xlrd

wb     = xlrd.open_workbook('/home/srarlk/Downloads/rlk/Copie_de_taxo_ajour_01122009_v2.xlsx')
ws     = wb.sheet_by_name('Feuil1')
ncells = ws.ncols-1


class TaxoIds:

    def __init__(self, xinput):
        self.input = xinput
        self.nrows = ws.nrows-1
        self.delta = [0,1]
        try:                                         #  try to convert number to float  
            self.input = round(float(self.input), 1) #    (xlrd gives output in float)
        except ValueError:                           #  if not a number, search done in next column
            self.delta = [1,0]

    def id_name_pair(self):
        result = ''
        for self.dft_cell in range(0, 13, 2):
            self.sch_cell =  self.dft_cell + self.delta[0]
            self.ret_cell =  self.dft_cell + self.delta[1]
            if(self.search_column()):  
                a, b  = self.sch_cell, self.ret_cell
                if b  < a:  a, b = b , a
                result = [int(ws.cell_value(self.i_row, a)), ws.cell_value(self.i_row, b)]
                break
        return result

    def search_column(self):
        found = False
        for self.i_row  in    range(1, self.nrows):
            if  ws.cell_value(self.i_row, self.sch_cell) == self.input:  
                found = True
                break
        return  found
#______________

def taxo_row(n):
    nrows   = int(ws.nrows-1)
    if  n > nrows:  
        print "Input out of range"
        
    out_row = []
    for i_col in xrange(ncells):
        try:
            out_row.append( int(ws.cell_value(n,i_col)) )
        except ValueError:
            out_row.append( ws.cell_value(n,i_col)      )
        
    return out_row
#______________

def taxo_col(n):

    nrows = ws.nrows-1
    ncols   = int(ncells)
    if  n > ncols:  
        print "Input out of range"

    out_col = []
    for i_row in xrange(1,nrows):
        try:
            out_col.append( int(ws.cell_value(i_row,n)) )
        except ValueError:
            out_col.append( ws.cell_value(i_row,n) )
        
    return out_col
#_________________________

if __name__ == '__main__':
    x = TaxoIds('Heavy Industry')
    print x.id_name_pair()


