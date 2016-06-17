# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = rootpath + 'EXE' + localtag + '/'
sys.path[0:0] = [EXEnoslash]
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
########################
timeFormat = "%Y%m%d %H:%M:%S"
dateFormat = "%Y%m%d"
##########################
import rpu_rp, rpInd, ibutiles
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
############################################3
##   MODE #######
mode = 'intraday'#'intraday' #'hourly' ## 'daily'  'intraday'
global today
global sym
today =  rpu_rp.todaysdateunix()
newDataList = []
#################################
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
modedict  = rpu_rp.create_dict(libbars,0,5)
barlistall = bardict.keys()
barlist =[]
for b in barlistall:
    if modedict[b] == mode:
        barlist.append(b)
##########################
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()
##symbol_list = ['ZD']
print symbol_list
print barlist
#################################################
count =0
trans_id = 0
global symib
############################################################
def error_handler(msg):
    if  'historicalData' in str(msg):
        print 'error probably pacing hist data'
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        print "Server Error: %s" % msg
def reply_handler(msg):
    if msg.typeName == 'historicalData':
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        print "Server Response: %s, %s" % (msg.typeName, msg)
####################
def historical_data_handler(msg):  
    global newDataList
    fname = DataDown+ today + '.' + sym + '.'  + bar+'.csv'
    if ('finished' in str(msg.date)) == False:  ### keep building the list
##        print (int(msg.date))
        fstring = "%Y-%m-%d %H:%M:%S"
        dateold = localtime(int(msg.date))
        tdate = strftime(fstring, dateold)       
        if bar == '1 day':
            tdate = str((int(msg.date))) + ' 23:59:58'       
        dataStr = '%s, %s, %s, %s, %s, %s, %s' % (sym, tdate, msg.open, msg.high, msg.low, msg.close, msg.volume)  
        newDataList = newDataList + [dataStr]  
    else:
        print 'next list'
        rpu_rp.WriteStringsToFile(fname,'') #flush the file
        for a in newDataList:
            rpu_rp.WriteStringsToFileAppend(fname,a)
        newDataList = []  
####################################       
tws_conn = Connection.create(port=7496, clientId=109)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.register(historical_data_handler, message.historicalData)
#######################################

for sym in symbol_list:
    symib = symdict[sym] #'CASH'
    ibsecType = typedict[sym] #'CASH'
    ibexchange = exchdict[sym] #'IDEALPRO'
    cashcurr = currdict[sym] #'USD'
    expiry = expiredict[sym] #'ignore'
    for bar in barlist:
        duration = bardict[bar]
        print bar, sym, symib, ibsecType, ibexchange, cashcurr, expiry, duration
        contract = ibutiles.create_ticksym(trans_id,symib,ibsecType,ibexchange,cashcurr,expiry)
        tws_conn.reqHistoricalData(trans_id, contract, '', duration, bar, 'BID_ASK', 0, 2)
        trans_id = trans_id + 1  
        sleep(5)
###############
print 'disconnecting from ib..'
tws_conn.disconnect()
