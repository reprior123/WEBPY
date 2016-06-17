# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash  + '/'
TMP = rootpath + 'TMP' + localtagSLASH
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
global today, sym, quotearray
global symbol_list
today =  rpu_rp.todaysdateunix()
from datetime import datetime
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
##ibsymbol_list = symdict.values()
#################################
quotearray =[1,0,0,0,0,'bla','somedate',1,1,1,1,1,1,1,222,333]
#####################################
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)
global symTickerIddict
value = 'empty'
########################################
def local_reply_handler(msg):
    value = 'empty'
    fnum = 45
    if  msg.typeName == 'tickString':
        fnum = msg.tickType
        value = msg.value
    if msg.typeName == 'tickPrice':
        fnum = msg.field
        value = msg.price       
        quotearray[5] = symTickerIddict[msg.tickerId]
    if msg.typeName == 'tickSize':
        fnum = msg.field
        value =msg.size
    quotearray[int(fielddict[str(fnum)])] = value
    if msg.typeName == 'tickSnapshotEnd':
        sym = quotearray[5] 
        quotearray[6] = today
        quotearray[0] = datetime.now().time().isoformat()
        linearray = []
        linearray.append(quotearray)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.ticksnaps.csv',linearray)
    rpu_rp.WriteStringsToFileAppend(TMP +'replys.snapshots',str(msg))
#################################
tws_conn = Connection.create(port=7496, clientId=108) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(local_reply_handler)
##########################
symTickerIddict ={}
def create_contract_dictionary(ordid,sym):
    contract = ibutiles.create_ticksym(ordid,sym)
    contractdict.update({sym : contract})
    symTickerIddict.update({ordid : sym})
##    print contractdict
##########################
ordid =0
contractdict ={}
for sym in symbol_list:
    ordid+=1
    create_contract_dictionary(ordid,sym)
    sleep(1)
#####################################
cycletime = 15 ## will need to be increase for more products because of delay
delay = 1     
usedtime = ((len(symbol_list))*delay)
cyclepause = cycletime - usedtime
loopmax = 36000 # = allday
loop = 1
controlfname = TMP + 'QUOTEcontroller.txt'
while loop < loopmax:
    command = (rpu_rp.CsvToLines(controlfname)[0])[0]    
    controlflag = True
    if command != 'RUN-setting':
        controlflag = False   
        print 'got the order to exit program....!!! <<<'
        sys.exit()
        loopmax = 1
    ###############
    sym_id = 1
    current_time = datetime.now().time()
       
    for sym in symbol_list:
        contract = contractdict[sym]
##        contract = ibutiles.create_ticksym(sym_id,sym)
        quotearray =[1,0,0,0,0,'bla','somedate',1,1,1,1,1,1,1,222,333]
        tws_conn.reqMktData(sym_id,contract,'BID',True)
        sym_id +=1        
        sleep(delay)
    loop += 1
    sleep(cyclepause) ## careful if this results in neg num, just hangs
    print current_time.isoformat(),'getting one round of snaps...looptime/cycletime',usedtime,cycletme 
print 'disconnecting..ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
