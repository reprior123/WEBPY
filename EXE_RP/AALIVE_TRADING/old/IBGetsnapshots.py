# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash  + '/'
sys.path[0:0] = [EXEnoslash]
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
########################
import  rpu_rp, rpInd, ibutiles
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today
today =  rpu_rp.todaysdateunix()
##today = '20150526'
from datetime import datetime
global sym
global ibsymbol_list
sym = 'EUR'
global fname
fname = DataDown +  today + '.ticksnaps.csv'
 ###################  
bidstring = 'field=1'
bidstringsize = 'field=0'
askstring = 'field=2'
askstringsize = 'field=3'
bid = ask = bidsize = asksize = 0
global quotearray
quotearray =[1,0,0,0,0,'bla','somedate']
global linearray
linearray =[]
#####################################
def error_handler(msg):
    print "Server Error: %s" % msg
###################################
def reply_handler(msg):
    if msg.typeName == 'tickPrice' or msg.typeName == 'tickSize':
        tickpos =int((msg.tickerId) - 1)
        sym = ibsymbol_list[tickpos]
        if msg.field == 1:
            quotearray[1] = msg.price
        if bidstringsize in str(msg):
            quotearray[2] = msg.size
        if askstring in str(msg):
            quotearray[3] = msg.price
        if askstringsize in str(msg):
            quotearray[4] = msg.size
            quotearray[5] = sym
            quotearray[6] = today
    if msg.typeName == 'tickSnapshotEnd':
        quotearray[0] = datetime.now().time().isoformat()
        linearray = []
        linearray.append(quotearray)
        rpu_rp.WriteArrayToCsvfileAppend(fname,linearray)
        pass
    if  msg.typeName != 'tickPricexxx' and msg.typeName != 'tickSizexxx':
        print "Server Response: %s, %s" % (msg.typeName, msg)           
####################
##def parse_tickSnapshot(snapshotmsg):
'''
field 0 =  bidsize, f1 = bid price   field 2 = ask, f3 = asksize   f4 = ?
f6 = day hi, f7= day low, f9 = last   Server Response: tickPrice, <tickPrice tickerId=2, field=1, price=1.5465, canAutoExecute=1>
Server Response: tickSize, <tickSize tickerId=2, field=0, size=2070000>
'''
#################################
##def create_order(order_type, quantity, action, limitprice)  ##now found in ibutiles
##############################
# (The clientId is chosen by us and we will need separate IDs for both the execution connection and
tws_conn = Connection.create(port=7496, clientId=108)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
################

libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
##ES,ES,GLOBEX,USD,20150619,FUT
bardict = rpu_rp.create_dict(libbars,0,1)
barlist = bardict.keys()
##########################
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()
ibsymbol_list = rpsymdict.items()
#################################
global symib
for sym in symbol_list:
    symib = symdict[sym]
    fname = DataDown + today  + '.' + symib + '.ticksnaps.csv'
    if os.path.isfile(fname):
        pass
    else:
        rpu_rp.WriteStringsToFile(fname,'') # create the file
##############################
timelimit = 4000
timer = 1
###############
from datetime import datetime
while timer < timelimit:
    order_id = 1
    current_time = datetime.now().time()
    print current_time.isoformat()    
    for sym in symbol_list:
        symib = symdict[sym] #'CASH'
        ibsecType = typedict[sym] #'CASH'
        ibexchange = exchdict[sym] #'IDEALPRO'
        cashcurr = currdict[sym] #'USD'
        expiry = expiredict[sym] #'ignore'
        fname = DataDown +today  + '.' + sym + '.ticksnaps.csv'
        contract = ibutiles.create_ticksym(order_id,symib,ibsecType,ibexchange,cashcurr,expiry)
        tws_conn.reqMktData(order_id,contract,'BID',True)
        order_id +=1
        delay = 1        
        cycletime = ((len(symbol_list))*delay)
##        print cycletime
        sleep(delay)
    timer += 1
    sleep(30-cycletime) ## careful if this results in neg num, just hangs
    print 'running next loop after sleep of ',cycletime        
print 'disconnecting..loop is done..'
tws_conn.disconnect()
##reqGlobalCancel()
