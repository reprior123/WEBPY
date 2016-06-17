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
moduleNames = open('importmodlist.txt').readlines()
for module in moduleNames:
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
import Mod_TicksUtile, Mod_ibutiles
######################
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global  sym, symbol_list, symdict
########################################
date = today
symbol_list = ['ES'] #symlistTicker
symTickerIddict ={}
contractdict ={}
symid=0
### backup tick files ####
fneedblist = ['.RTticks.csv','.RTMktDepth.csv','.RTtickData.csv']
fneedblist = ['.5secs.recent.csv']
for sym in symbol_list:
    ## flush the recent 5sec file ##
    rfile = DataDown+ today + '.' + sym  +'5secs.recent.csv'
    if os.path.isfile(rfile):
        os.remove(rfile)
    
    print 'creating tickerdict for ',sym
    symid+=1
    symTickerIddict.update({str(symid) : sym})
    print 'need to backup recent file before overwriting..'
    for froot in fneedblist:
        fname1 = DataDown+ today + '.' + sym  +froot
        Mod_TicksUtile.backupTickfiles(fname1)
#################
onerow =[]
timenow = datetime.now().time().isoformat()
################
def reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        msgarray = (str(msg)).split()
        reqid=(msgarray[1]).split('=')[1].replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        timenow= datetime.now().time().isoformat()
        ticktime = timenow.replace(':','').replace('.','')
        fname = DataDown+ today + '.' + sym  +'.rtimebar.' + ticktime+'.txt'
        cleanonerow = Mod_TicksUtile.clean_RTTick5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfile(fname,[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[cleanonerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
#################################
print 'Connecting to Live DATAFEED,depth, and per tick trade counter...please wait'
tws_conn = Connection.create(port=7496, clientId=178) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(Mod_ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
##########################
cycletime = 30 ## will need to be increase for more products because of delay
cyclesperhour = 3600 / cycletime
loopmax = cyclesperhour*10 # = allday
loop = 1
################
reqID=1
symid =0
strike=22
expiry = '22'
FivesecBarTicker = 'on'
DOMTicker = 'off'
GenTicker = 'off'
##############
for sym in symbol_list:
    symid+=1
    contract = Mod_ibutiles.create_contract(sym,strike,expiry)
    ticktype = ticktypedict[sym]
    
    if FivesecBarTicker == 'on':
        print 'starting 5sec ticker for ', sym
        tws_conn.reqRealTimeBars(reqID,contract,'',ticktype,0)

    if DOMTicker == 'on':        
        numRows = 10
        mktdepthoptions = 'XYZ'
        tws_conn.reqMktDepth(reqID,contract,numRows)
        
    if GenTicker == 'on':        
        snapshot = False
        genericTicks = '233'
        tws_conn.reqMktData(reqID,contract,genericTicks,snapshot)
    reqID +=1     # perhaps this has to be incremented for each ticker?    
    sleep(1)
#############
## done with starting tickers....now download fillinbars   ###
import IBDownloader
###############
doall = 'y' #raw_input('do all syms for tickercompile? ')
if doall == 'y':
    slist = ['ES','FDAX'] #symlistAll
    pass
else:
    symtodo = raw_input('enter sym here ')
    slist = [symtodo]
    pass
############
while loop < loopmax:
    ## process single files into recent file ##
    for sym in slist:
        Mod_TicksUtile.prepare_tickfilesto5secBars(date,sym,'initialize')
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER heartbeat is active',loop
    ################
print 'disconnecting..LIVE ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
################
'''
################
def reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        cleanonerow = Mod_TicksUtile.clean_RTTick5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticks.csv',[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[cleanonerow])
    elif msg.typeName == 'tickString' or msg.typeName == 'tickSize' or msg.typeName == 'tickPrice'  :
        timenow= datetime.now().time().isoformat()
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        onerow.append(timenow)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTtickData.csv',[onerow])
        
    elif msg.typeName == 'updateMktDepth':
        timenow= datetime.now().time().isoformat()
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        onerow.append(timenow)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTMktDepth.csv',[onerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
######    if msg.typeName == 'tickPrice' and (((str(msg)).split()[2]).split('=')[1]).replace(',','') == '1':
########<tickPrice tickerId=1, field=4, price=1927.0, canAutoExecute=0>
######        timenow= datetime.now().time().isoformat()
######        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
######        sym=symTickerIddict[reqid]
######        onerow = (str(msg)).split(',')
######        onerow.append(timenow)
######        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[onerow])
#################################
'''
