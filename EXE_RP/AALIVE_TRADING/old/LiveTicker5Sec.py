import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp, rpInd, ibutiles, TicksUtile
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, sym, symbol_list, symdict, symbol_list2
symbol_list = symbol_list2
########################################
symTickerIddict ={}
contractdict ={}
symid=0
for sym in symbol_list:
    symid+=1
##    contract = ibutiles.create_ticksym(symid,sym)
##    contractdict.update({sym : contract})
    symTickerIddict.update({str(symid) : sym})
    fname1 = DataDown+ today + '.' + sym  +'.RTticks.csv'
    TicksUtile.backupTickfiles(fname1)
    rpu_rp.WriteArrayToCsvfile(fname1,[])
    
rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTticks',[])
#################
onerow =[]
def RTBar_reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        cleanonerow = TicksUtile.clean_RTTick5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticks.csv',[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[cleanonerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(TMP +'replys.RTticks',str(msg))
#################################
print 'Connecting to Live DATAFEED...please wait'
print 'Collecting 5Second Tick Bars in realtime for the following symbols...'
print symbol_list
tws_conn = Connection.create(port=7496, clientId=162) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(RTBar_reply_handler)
##########################
cycletime = 120 ## will need to be increase for more products because of delay
loopmax = 300000 # = allday
loop = 1
################
reqID=1
symid =0
strike=22
expiry = '22'
for sym in symbol_list:
    symid+=1
    contract = ibutiles.create_contract(sym,strike,expiry)
    ticktype = ticktypedict[sym]
    tws_conn.reqRealTimeBars(reqID,contract,'',ticktype,0)
    reqID +=1        
    sleep(1)
#############
symlist = symbol_list2
barlist = barlist_All
rpu_rp.WriteArrayToCsvfile(TMP +'symlist.csv',[symlist])
rpu_rp.WriteArrayToCsvfile(TMP+'barlist.csv',[barlist])
sleep(2)
import HistoricalDataDloadFLEX
####startmode = 'initialize'
####strike= 202

##ans = raw_input('start depth ticker? ')
##if ans == 'y':
##    print 'did not start...do it manually'
##    import DepthMarketTicker
while loop < loopmax:
    ###############
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER heartbeat is active',loop
    ################
print 'disconnecting..LIVE ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
