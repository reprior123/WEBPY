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
global today, sym, symbol_list2, symbol_list_opts, symdict, replyfname, symTickerIddict, contractdict, tws_conn
global tws_conn
#########################
print symbol_list2
print symbol_list_opts
########################################
##flush files here is bad if building on hist....
replyfname = TMP +'replys.vola2.txt' 
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
    print str(msg)
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
tws_conn = Connection.create(port=7496, clientId=179)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.register(reply_handler)

##########################
symTickerIddict ={}
symid =1
for sym in symbol_list2:
    print sym, symid
    symTickerIddict.update({str(symid) : sym})
    symid +=1

    
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
def build_c_dbase(slist):
    symid = 1
    symTickerIddict ={}
    contractdict ={}
    for sym in slist:
        contract = ibutiles.create_ticksym(symid,sym)
        contractdict.update({sym : contract})
        symTickerIddict.update({str(symid) : sym})
        symid +=1
    print symTickerIddict
    return contractdict
##start_tickers()
#####################
def get_vola(symbol_list_opts):
    reqID =111
    symid = 0
    for sym in symbol_list_opts:
        if sym != 'SPY':
            print sym
            underlying = symdict[sym]
            if underlying == 'SPY':
                underPricenew =  float(TicksUtile.recenttick(underlying,'1min'))
                optionpricenew = float(TicksUtile.recenttick(sym,'both'))
                optionprice = underPricenew # 5.00
                underPrice = underPricenew #200.0
                
                ticktype = ticktypedict[sym]
                
                ATMstrike = round(underPrice,0)
                
                if 'SPYF' in sym:
                    print sym, underPrice, optionprice, typedict[sym], 'atm', ATMstrike
                    symid+=1
##                    contract  = contractdict[sym]
                    ATMspyoption = ibutiles.create_option_contract(sym,ATMstrike)
##                    tws_conn.reqRealTimeBars(reqID,ATMspyoption,'',ticktype,0)
##                    print rpu_rp.CsvToLines(replyfname)
##                    reqID +=1 
                    tws_conn.calculateImpliedVolatility(reqID,ATMspyoption,optionprice,underPrice)
                    reqID +=1        
                    sleep(1)
##                    tws_conn.cancelCalculateImpliedVolatility(reqID)

############
#########################  run the downloader via def #####
##import HistoricalDataDload
##HistoricalDataDload.dload_list(symbol_list2)
##HistoricalDataDload.dload_list(symbol_list_opts)
########################
##### could run vola part here
contractdict = build_c_dbase(symbol_list_opts)
get_vola(symbol_list_opts)
###########################
cycletime = 5 ## will need to be increase for more products because of delay
loopmax = 2 # = allday
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

def parse_vola_msg(filein):
    lines = rpu_rp.CsvToLines(filein)
    for line in lines:
        print line

filein = replyfname
parse_vola_msg(filein)
'''
['<tickOptionComputation tickerId=112', ' field=53', ' impliedVol=0.155027818636', ' delta=2147483647', ' optPrice=6.9', ' pvDividend=2147483647', ' gamma=2147483647', ' vega=2147483647', ' theta=2147483647', ' undPrice=201.75>']
'''
