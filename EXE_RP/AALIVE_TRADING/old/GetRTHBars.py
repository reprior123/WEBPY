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
global today, sym
global symbol_list
today =  rpu_rp.todaysdateunix()
from datetime import datetime
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
########################################
symTickerIddict ={}
contractdict ={}
symid=0
##flush files here is bad if building on hist....
for sym in symbol_list:
    symid+=1
##    sleep(1)
    contract = ibutiles.create_ticksym(symid,sym)
    contractdict.update({sym : contract})
    symTickerIddict.update({str(symid) : sym})
##    rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.rthbars.csv',[])
rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTticks',[])
#################
rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+ '.RTticks.csv',[]) ### flush
onerow =[]
def RTBar_reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
##        print str(msg)
##        print 'is a bar..', sym
        onerow = (str(msg)).split(',')
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticks.csv',[onerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[onerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
#################################
tws_conn = Connection.create(port=7496, clientId=177) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(RTBar_reply_handler)
##########################
cycletime = 4 ## will need to be increase for more products because of delay
loopmax = 300000 # = allday
loop = 1
################
##controlfname = TMP + 'QUOTEcontroller.txt'
reqID=1
symid =0
for sym in symbol_list:
    symid+=1
    contract = ibutiles.create_ticksym(symid,sym)
    tws_conn.reqRealTimeBars(reqID,contract,'','MIDPOINT',0)
    reqID +=1        
    sleep(1)
while loop < loopmax:
##    command = (rpu_rp.CsvToLines(controlfname)[0])[0]
    command = 'go'
    if command == 'QUIT-setting':
        print 'got the order to exit program....!!! <<<'
        loopmax = 1
    ###############
    current_time = datetime.now().time()
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print current_time.isoformat(),'just loop rtbar '
print 'disconnecting..ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
