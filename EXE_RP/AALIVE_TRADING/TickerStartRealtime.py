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
print TMP
sleep(20)
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open(EXE +'importmodlist.txt').readlines()
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
'''
<tickString tickerId=1, tickType=48, value=2023.00;476;1459252303719;164394;2028.0266205;false>
<updateMktDepth tickerId=1, position=0, operation=1, side=1, price=2023.0, size=160>
<updateMktDepth tickerId=1, position=9, operation=1, side=1, price=2020.75, size=238>
<updateMktDepth tickerId=1, position=4, operation=1, side=0, price=2024.25, size=246>
<tickSize tickerId=1, field=3, size=92>
<tickPrice tickerId=2, field=1, price=9887.0, canAutoExecute=1>
<tickSize tickerId=2, field=0, size=2>
<tickPrice tickerId=2, field=2, price=9888.5, canAutoExecute=1>
<tickSize tickerId=2, field=3, size=4>
'''
date = today
doall = 'n' #raw_input('do all syms for tickercompile? ')
if doall == 'y':
    symbol_list = ['ES','FDAX'] #symlistAll
else:
    symtodo = 'ES' #raw_input('enter sym here ')
    symbol_list = [symtodo]
############
symTickerIddict ={}
contractdict ={}
symid=0
### backup tick files ####
fneedblist = ['.5secs.recent.csv','.RTticks.csv','.RTMktDepth.csv']
for sym in symbol_list:
    print 'need to backup recent file before overwriting..'
    for froot in fneedblist:
        fname1 = DataDown+ today + '.' + sym  +froot
        Mod_TicksUtile.backupTickfiles(fname1)
        ## flush the file ##
        if os.path.isfile(fname1):
            os.remove(fname1)   
    print 'creating tickerdict for ',sym
    symid+=1
    symTickerIddict.update({str(symid) : sym})
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
    elif msg.typeName == 'updateMktDepth':
        msgarray = (str(msg)).split()
        reqid=(msgarray[1]).split('=')[1].replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        timenow= datetime.now().time().isoformat()
        ticktime = timenow.replace(':','').replace('.','')
        fname = DataDown+ today + '.' + sym  +'.rtDOMbar.' + ticktime+'.txt'
        cleanonerow = Mod_TicksUtile.clean_rtDOMbar(onerow,sym)
        rpu_rp.WriteArrayToCsvfile(fname,[cleanonerow])
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
    elif msg.typeName == 'tickPrice' or msg.typeName == 'tickSize'  :
        msgarray = (str(msg)).split()
        reqid=(msgarray[1]).split('=')[1].replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        timenow= datetime.now().time().isoformat()
        ticktime = timenow.replace(':','').replace('.','')
        fname = DataDown+ today + '.' + sym  +'.rtTICKbar.' + ticktime+'.txt'
        cleanonerow = Mod_TicksUtile.clean_rtTICKbar(onerow,sym)
        rpu_rp.WriteArrayToCsvfile(fname,[cleanonerow])
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
    elif msg.typeName == 'TickString'   :
        msgarray = (str(msg)).split()
        reqid=(msgarray[1]).split('=')[1].replace(',','')
##        sym=symTickerIddict[reqid]
##        onerow = (str(msg)).split(',')
##        timenow= datetime.now().time().isoformat()
##        ticktime = timenow.replace(':','').replace('.','')
##        fname = DataDown+ today + '.' + sym  +'.rtTICKStringsbar.' + ticktime+'.txt'
##        cleanonerow = Mod_TicksUtile.clean_rtTICKbar(onerow,sym)
##        rpu_rp.WriteArrayToCsvfile(fname,[cleanonerow])
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticksStrings',str(msg))        
    else:
        print str(msg) ## still need the TickString and Generic typeNames
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
GenTicker = 'on'
############
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
restartstatus = 'partialxxx'
##restartstatus = 'fullnoDAY'
if restartstatus== 'partial':
    import IBDownloaderShortTerms
    pass
else:    
    import IBDownloader
###############
while loop < loopmax:
    ## process single files into recent file ##
    for sym in symbol_list:
        Mod_TicksUtile.prepare_tickfilesto5secBars(date,sym,'initialize')
        Mod_TicksUtile.prepare_rtTICKbar(date,sym,'initialize')
##        Mod_TicksUtile.prepare_rtDOMbars(date,sym,'initialize')        
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER heartbeat is active',loop
    ################
print 'disconnecting..LIVE ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
################
'''
################
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
