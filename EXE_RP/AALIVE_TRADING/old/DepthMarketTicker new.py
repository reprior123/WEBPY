import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
#########################################
import ENVvars

nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, TicksUtile, RP_Snapshot, ibutiles
import glob, csv, subprocess, datetime, shutil, time, os.path
from datetime import datetime
import ctypes 
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, sym, symbol_list
symbol_list = symdict.keys()
symbol_list =['ES']#,'EUR.USD']
########################################
symTickerIddict ={}
contractdict ={}
symid=0
strike = 90
expiry = ''
##flush files here is bad if building on hist....
for sym in symbol_list:
    print sym
    symid+=1
    contract = ibutiles.create_contract(sym,strike,expiry)
    contractdict.update({sym : contract})
    symTickerIddict.update({str(symid) : sym})
    
    fname1 = DataDown+ today + '.' + sym  +'.RTMktDepth.csv'
    TicksUtile.backupTickfiles(fname1)
    fname3 = DataDown+ today + '.' + sym  +'.RTtickData.csv'
    TicksUtile.backupTickfiles(fname3)
    ######################
rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTtickDOMs',[])
#################
onerow =[]
current_time = datetime.now().time()
timenow=current_time.isoformat()
'''
2048.75', ' size=385>', '22:12:56.097000']
<updateMktDepth tickerId=1, position=8, operation=1, side=0, price=2049.75, size=415>
['<updateMktDepth tickerId=1', ' position=8', ' operation=1', ' side=0', ' price=2049.75', ' size=415>', '22:12:56.121000']
'''
global depthpricearray, depthsizearray
depthpricearray = [1,1,1,1,1,1,1,1,1,1,1]
depthsizearray = [1,1,1,1,1,1,1,1,1,1,1]
def RTDepth_reply_handler(msg):
    depthpricearray = [1,1,1,1,1,1,1,1,1,1,1]
    depthsizearray = [1,1,1,1,1,1,1,1,1,1,1]
    if msg.typeName == 'updateMktDepth' or msg.typeName == 'tickString' or msg.typeName == 'tickSize' or msg.typeName == 'tickPrice'  :
        current_time = datetime.now().time()
        timenow=current_time.isoformat()
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        onerow.append(timenow)

    if msg.typeName == 'updateMktDepth':
##        print msg
##        print onerow
        domprice = onerow[4].replace(' price=','')
        domsize = onerow[5].replace(' size=','').replace('>','')
        domposition = int(onerow[1].replace(' position=',''))
        depthpricearray[domposition] = domprice
        depthsizearray[domposition] = domsize
        print depthpricearray
        print depthsizearray
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTMktDepth.csv',[onerow])
    elif msg.typeName  == 'tickString' or msg.typeName == 'tickSize' or msg.typeName == 'tickPrice'  :
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTtickData.csv',[onerow])
##    elif  msg.typeName == 'tickString': if msg.tickType == 48:    
    else:
        print str(msg)
        current_time = datetime.now().time()
        timenow=current_time.isoformat()
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTtickDOMs',str(msg))
    if msg.typeName  == 'tickString'   :
##        print str(msg)
        pass
#################################
tws_conn = Connection.create(port=7496, clientId=179) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(RTDepth_reply_handler) ###RTDepth_reply_handler
##########################
cycletime = 120000 ## will need to be increase for more products because of delay
loopmax = 300000 # = allday
loop = 1
################
reqID=1
symid =0
strike = 999
expiry = 'NA'
for sym in symbol_list:
    symid+=1
    contract = ibutiles.create_contract(sym,strike,expiry)
    ticktype = ticktypedict[sym]
    numRows = 10
    mktdepthoptions = 'XYZ'
    tws_conn.reqMktDepth(reqID,contract,numRows)
    snapshot = False
    genericTicks = '233'
    tws_conn.reqMktData(reqID,contract,genericTicks,snapshot)
    reqID +=1        
    sleep(1)
##    cancelMktDepth(reqID) # save the reqIDs to library for later use to cxl
#############
current_time = datetime.now().time()
print 'REALTIME MARKET DEPTH TICKER for SPZ Emini Contract...',current_time.isoformat()
while loop < loopmax:
    ###############
    current_time = datetime.now().time()
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME DEPTH TICKER heartbeat....',current_time.isoformat()
print 'disconnecting..ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()

##genericTicks other types with return codes:
##100 Option Volume (currently for stocks) 29, 30
##101 Option Open Interest (currently for stocks) 27, 28
##104 Historical Volatility (currently for stocks) 23
##162 Index Future Premium 31
##165 Miscellaneous Stats 15, 16,17, 18,19, 20,21
##221 Mark Price (used in TWS P&L computations) 37
##225 Auction values (volume, price and imbalance) 34, 35,36
##########233 RTVolume - contains lasttradeprice, lastsize, lasttime, totalvolume, VWAP, single trade flag.48
##Single trade flag - True indicates filled by a single market maker; False is multiple marketmakers
##Here is an example of the RTVolume formatting for AAPL:
##RTVolume=701.28;1;1348075471534;67854;701.46918464;true
##RTVolume=701.26;3;1348075476533;67857;701.46917554;false
