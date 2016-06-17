import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
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
##    print var
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, sym, symbol_list, symdict, replyfname, symTickerIddict, contractdict
global tws_conn
#########################
symbol_listall = symdict.keys()
symbol_list2 =[]
for b in symbol_listall:
    if typedict[b] == 'OPT' or typedict[b] == 'STK':
        symbol_list2.append(b)
print symbol_list2
########################################
symbol_list_opts =[]
for b in symbol_listall:
    if typedict[b] != 'OPT' and typedict[b] != 'STK':
        symbol_list_opts.append(b)
print symbol_list_opts
########################################
##flush files here is bad if building on hist....
replyfname = TMP +'replys.vola.txt' 
rpu_rp.WriteArrayToCsvfile(replyfname,[])
onerow =[]
########################   
def backupTickfiles(fname1):
    fname2  = fname1.replace('.csv','bu.csv')
    f1 = rpu_rp.CsvToLines(fname1)
    f2 = rpu_rp.CsvToLines(fname2)
    for line in f1:
        f2.append(line)
    rpu_rp.WriteArrayToCsvfile(fname2,f2)
    rpu_rp.WriteArrayToCsvfile(fname1,[])
##########################
def reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        cleanonerow = TicksUtile.format_RTTickoneline_to_5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticks.csv',[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTtickslastquote.csv',[cleanonerow])
    else:
        if 'connection is OK' in str(msg):
            pass
        else:
            print str(msg)
            rpu_rp.WriteStringsToFileAppend(replyfname,str(msg))
#################################
tws_conn = Connection.create(port=7496, clientId=169)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
##########################

def start_tickers():
    symTickerIddict ={}
    contractdict ={}
    reqID=1
    symid =1
    for sym in symbol_list2:
        print sym, symid
        fname1 = DataDown + today + '.' + sym  +'.RTticks.csv'
        ## backup the tick files before restarting
        backupTickfiles(fname1)
        ## flush the tickfile
        rpu_rp.WriteArrayToCsvfile(fname1,[])
        ### restart ticker

        ##build the cntract dict but probably not use
        contract = ibutiles.create_ticksym(symid,sym)
        contractdict.update({sym : contract})
        symTickerIddict.update({str(symid) : sym})
        print symTickerIddict
        ticktype = ticktypedict[sym]
        ## restart the ticker
        tws_conn.reqRealTimeBars(reqID,contract,'',ticktype,0)
        symid+=1
        reqID +=1 
        sleep(1)
########################
start_tickers()
#####################
def get_vola():
    reqID =111
    contract = ibutiles.create_ticksym(99,'SPY')
    genericTicks =''
    snapshot = True
######    sym = 'SPY'
######    contract = contractdict[sym]
    tws_conn.reqMktData(reqID,contract,genericTicks,snapshot)
    #########################################
    symid = 0
    for sym in symbol_list_opts:
        print sym
        underlying = symdict[sym]
        if underlying == 'SPY':
            underPricenew = TicksUtile.recenttick(underlying,'dload')
            optionpricenew = TicksUtile.recenttick(sym,'dload')
            optionprice = 5.00
            underPrice = 200.0
            print underPricenew, optionpricenew
            print typedict[sym]
            ATMstrike = round(underPrice,-2)
            print 'atm', ATMstrike
            if typedict[sym] == 'OPT':
                symid+=1
                contract  = contractdict[sym]
                tws_conn.calculateImpliedVolatility(reqID,contract,optionprice,underPrice)
                reqID +=1        
                sleep(1)
                tws_conn.cancelCalculateImpliedVolatility(reqID)
############
#########################  run the downloader via def #####
import HistoricalDataDload
HistoricalDataDload.dload_list(symbol_list2)
HistoricalDataDload.dload_list(symbol_list_opts)
########################
##### could run vola part here
get_vola()
###########################
cycletime = 12 ## will need to be increase for more products because of delay
loopmax = 20000 # = allday
loop = 1
current_time = datetime.now().time()
while loop < loopmax:
    ###############
    current_time = datetime.now().time()
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER',current_time.isoformat()
print 'disconnecting..ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
