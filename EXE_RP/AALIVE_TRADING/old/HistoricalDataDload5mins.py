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
from ib.opt import Connection, message   #
############################################
global today
global sym
today =  rpu_rp.todaysdateunix()
newDataList = []
########
mode = 'intraday'#'intraday' #'hourly' ## 'daily'  'intraday'
##answer = raw_input('1. intraday \n 2. hourly \n 3. daily')
answer = '1'
if answer == '1':
    mode = 'intraday'
elif answer == '2':
    mode = 'hourly'
else:
    mode = 'daily'
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
barlist = ['5 mins']
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
symbol_list = ['NQ', 'ES']
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
    fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
    if ('finished' in str(msg.date)) == False:  ### keep building the list
##        print (int(msg.date))
        fstring = "%Y-%m-%d %H:%M:%S"
        dateold = localtime(int(msg.date))
        tdate = strftime(fstring, dateold)       
        if bar == '1 day':
            tdate = (str((int(msg.date))))[0:4] + '-' + str((int(msg.date)))[4:6]+ '-' + str((int(msg.date)))[6:8] + ' 23:59:58'
##            print tdate
##            print msg.date
        dataStr = '%s, %s, %s, %s, %s, %s, %s' % (sym, tdate, msg.open, msg.high, msg.low, msg.close, msg.volume)  
        newDataList = newDataList + [dataStr]  
    else:
        print 'next list'
        rpu_rp.WriteStringsToFile(fname,'') #flush the file
        for a in newDataList:
            if len(a) > 2:
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
    for bar in barlist:
        duration = bardict[bar]
        print bar, sym
        contract = ibutiles.create_ticksym(trans_id,sym)
        tws_conn.reqHistoricalData(trans_id, contract, '', duration, bar, 'MIDPOINT', 0, 2)
        trans_id = trans_id + 1  
        sleep(4)
###############
print 'disconnecting from ib..'
tws_conn.disconnect()
