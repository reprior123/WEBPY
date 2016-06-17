################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)

for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################

global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open(EXE +'importmodlist.txt').readlines()
##for module in moduleNames:
##    modulestripped = module.strip()
##    if modulestripped != titleself:
####        print '...',modulestripped,'xxx',titleself
##        my_module = importlib.import_module(modulestripped)
##        pass
##    else:
##        print 'is self'
######################
'''
change allhref module actions to webpy views...
first choose default page
then map phpmodules to webmodules
'''

import rpu_rp
viewsarea = 'layoutaddfinthemehome.html'
viewsarea = 'C:/WEB2PY/EXE_RP/web2py/applications/AddfinV5simple/views/'
print viewsarea
files = glob.glob(viewsarea+'*')
for f in files:
    print f
newf ='C:/WEB2PY/EXE_RP/web2py/applications/AddfinV5simple/views\layoutaddfinthemehome.html'
newf = 'C:/WEB2PY/EXE_RP/web2py/applications/AddfinV5simple/views\layoutaddfintheme.html'

###############
def prepare_views_file(filein,fileout):
    newlines =[]
    lines = rpu_rp.CsvToLines(filein)
    newlines.append('')
    for l in lines:
        if ' ' in str(l):
            print l
prepare_views_file(newf,'bla.txt')



        
###############
def prepare_imp_file(filein,fileout):
    newlines =[]
    lines = rpu_rp.CsvToLines(filein)
    headerline =['Action', 'Quantity', 'Symbol', 'TimeInForce', 'SecType', 'OrderType', 'LmtPrice', 'Exchange', 'Currency', 'CUSIP', 'ISIN', '']
##    itemlist = [Action, Quantity, Symbol, TimeInForce, SecType, OrderType, LmtPrice, Exchange, Currency, CUSIP, ISIN]

    newlines.append(headerline)
    for l in lines:
        newline =[]
        print l
        isin = l[6]
        action = l[0]
        title = l[3]
        qty = l[5]
        price = l[2]
        c=0
        for i in headerline: # itemlist:   
##            print i
##            newline.append(i)
            newline.append(l[c])
            c+=1
        newlines.append(newline)
    rpu_rp.WriteArrayToCsvfile(fileout,newlines)
##prepare_imp_file(documents+'bla.csv',documents +'fileout.csv')
