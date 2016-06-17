################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
######################
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global  sym, symbol_list, symdict
########################################
symbol_list = symlistTicker
symTickerIddict ={}
contractdict ={}
symid=0
### backup tick files ####
print symbol_list
for sym in symbol_list:
    symid+=1
    symTickerIddict.update({str(symid) : sym})
    for filename in ['.RTticks.csv','.RTMktDepth.csv','.RTtickData.csv']:
        fname1 = DataDown+ today + '.' + sym  +filename
        TicksUtile.backupTickfiles(fname1)
##        flush file
        rpu_rp.WriteArrayToCsvfile(fname1,[])
##flush tick files where necessary   
rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTticks',[])
rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTtickDOMs',[])
#################
onerow =[]
current_time = datetime.now().time()
timenow=current_time.isoformat()
################
def reply_handler(msg):
    msgarray = (str(msg)).split()
    print msgarray, 'rawmessg'
    reqid=(msgarray[1]).split('=')[1].replace(',','')
    fieldnum = (msgarray[2]).split('=')[1].replace(',','')   
    sym=symTickerIddict[reqid]
    onerow = (str(msg)).split(',')
    print onerow,'onerow split by comma'
    timenow= datetime.now().time().isoformat()
    print msg.typeName, sym, timenow    
    if msg.typeName == 'realtimeBar':
        cleanonerow = TicksUtile.clean_RTTick5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticks.csv',[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[cleanonerow])
########    elif msg.typeName == 'tickString' or msg.typeName == 'tickSize' or msg.typeName == 'tickPrice'  :
########        onerow.append(timenow)
########        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTtickData.csv',[onerow])        
########    elif msg.typeName == 'updateMktDepth':
########        onerow.append(timenow)
########        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTMktDepth.csv',[onerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
########    if msg.typeName == 'tickPrice' and fieldnum == '1':
########        ##<tickPrice tickerId=1, field=4, price=1927.0, canAutoExecute=0>
########        onerow.append(timenow)
########        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquoteTicker.csv',[onerow])
#################################
print 'Connecting to Live DATAFEED,depth, and per tick trade counter...please wait'
tws_conn = Connection.create(port=7496, clientId=178) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
##########################
cycletime = 60 ## will need to be increase for more products because of delay
cyclesperhour = 3600 / cycletime
loopmax = cyclesperhour*10 # = allday
loop = 1
################
reqID=1
symid =0
strike=22
expiry = '22'
##############
for sym in symbol_list:
    symid+=1
    contract = ibutiles.create_contract(sym,strike,expiry)
    ticktype = ticktypedict[sym]
    tws_conn.reqRealTimeBars(reqID,contract,'',ticktype,0)
    numRows = 10
    mktdepthoptions = 'XYZ'
    if sym == 'ESxxxx':
        tws_conn.reqMktDepth(reqID,contract,numRows)
    snapshot = False
    genericTicks = '233'
    tws_conn.reqMktData(reqID,contract,genericTicks,snapshot)
    reqID +=1        
    sleep(1)
#############
print 'gothere'
symlist = symbol_list
barlist = barlist_All
rpu_rp.WriteArrayToCsvfile(TMP +'symlist.csv',[symlist])
rpu_rp.WriteArrayToCsvfile(TMP+'barlist.csv',[barlist])
sleep(2)
########
ransw = 'n'
##ransw =raw_input('fullrestart? ')
if ransw == 'y':
    import IBHistlDataDloadALLSYMSALLBARS
    pass
else:
##    import IBHistlESFDAX1min
    print 'not doing any imports'
###############
while loop < loopmax:
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER heartbeat is active',loop
    ################
print 'disconnecting..LIVE ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
