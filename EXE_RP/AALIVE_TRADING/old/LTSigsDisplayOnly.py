# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
from datetime import datetime
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
#######################################
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import  rpu_rp, rpInd, ibutiles, TicksUtile
from datetime import datetime
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
time_format = "%H:%M:%S"
dateFormat = "%Y%m%d"
##############################
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)

libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
modedict = rpu_rp.create_dict(libbars,0,5)

symdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
tickdict = rpu_rp.create_dict(libsyms,0,8)
tsizedict = rpu_rp.create_dict(libsyms,0,7)
roundfactordict = rpu_rp.create_dict(libsyms,0,9)
entrywiderdict = rpu_rp.create_dict(libsyms,0,10)
libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)
symbol_list = symdict.keys()
##symbol_list = ['AUD.USD']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':
        barlist.append(b)
barlist = ['1 hour']
print barlist
##################
prevsigid = ''
mode = 'livescan'
today =  rpu_rp.todaysdateunix()
##today ='20150618'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def read_vars(): ##read variables from the control panel file
    cpfile = TMP + 'signalcontroller.txt'
    paramlines = rpu_rp.CsvToLines(cpfile)
    varstrings = ['TimeLimitRecentSigs','SignalsToShow','DurationToShow']
    var = {}
    for varstring in varstrings:
        for line in paramlines:
            if len(line) > 0:
                if line[0] == varstring:
                    var[varstring] = line[1]
##    return int(var['TimeLimitRecentSigs'])
    return 3000
############################
def get_orderid():
################    tws_conn.reqIds(100)
##    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
##        order_id = 122
    return order_id
###################################
recentlimit = read_vars()
print 'recent limit is now.. ', recentlimit
##################     
loopmax = 2
loop = 0
sigs = rpu_rp.CsvToLines(sigarea + today +'.sigs.csv')
########################
controlfname = TMP + 'LT_Controller.txt'
##delaytime = 5
cycledelay = int(3)
rpu_rp.WriteArrayToCsvfile(sigarea +today+'.LTsigs.csv', '') # flush the file to keep all sigs
print 'delay is set at .. ', cycledelay
print 'THIS IS LONGTERM SEIGNALS HOURLEY ETC'
while loop < loopmax:
    ###############
    loop +=1
    sleep(cycledelay)
    now = datetime.strftime(datetime.now(),time_format)
    recentsigs =[]
    for sym in symbol_list:
        for barsize in barlist:
##            print barsize
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            decimalboost = dboostdict[sym]
            dur = barsize
            RTticksFile = DataDown +today+'.'+sym+ '.RTticks.csv'
            RTBarsin = rpu_rp.CsvToLines(RTticksFile)
            
            import datetime as dt
            june1= dt.datetime.strptime(' 2015-06-01 12:12:12', ' %Y-%m-%d %H:%M:%S')
            RTBars5Sec=TicksUtile.create_bars_from_barsAll(RTBarsin,today,sym,'5 secs',1,june1,'RTbars')
       
            HistBars5SecFile = DataDown +today+'.'+sym+ '.5 secs' + '.BarsHist.csv'
            HistBars5Sec = rpu_rp.CsvToLines(HistBars5SecFile)
            
            BothBars5Sec = []
            for a in HistBars5Sec:
                BothBars5Sec.append(a)
            for b in RTBars5Sec:
                BothBars5Sec.append(b)
            BothBars5SecClean= TicksUtile.CleanBarOverlap(BothBars5Sec)

##            rpu_rp.WriteArrayToCsvfile(DataDown +'blasigs.csv', BothBars5SecClean)

            
            lastHistBartime = TicksUtile.time_of_last_histbar(today,sym,dur,'newformat')
            TicksUtile.create_bars_from_barsAll(BothBars5SecClean,today,sym,dur,durinseconds,lastHistBartime,'normalmode')
            ## create recent here above
            
            
            filetomerge = DataDown +today+'.'+sym+'.'+barsize+'.ddload.csv' 
            lines = TicksUtile.merge_bar_files(filetomerge)
            
            ma = rpInd.process_ticks(lines,decimalboost,barsize)
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', ma)     
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +today+'.sigs.csv', ma)
##############################
            prevt = 0
            numsigs = len(ma)
            signum =0
            import datetime as dt  
            now = datetime.strftime(datetime.now(),time_format)
            now_dt = dt.datetime.strptime(now, time_format)
            prevbart_dt = now_dt
            for l in ma:
                sym = l[1] #.split()[0])
                sigprice = float(l[3]) #.split()[0])
                signum +=1
                if len(l[0].split()) == 2:  
                    currentbar =  l[0].split()[1]
                else:
                    currentbar = (l[0].split()[0])   
                currentbar_dt = dt.datetime.strptime(currentbar, time_format)
                now_dt = dt.datetime.strptime(now, time_format)
                barToNow = (now_dt - currentbar_dt).seconds
                barToPrev = (currentbar_dt - prevbart_dt).seconds
                alerttxt = l[1] + '|' + str(barToNow) + '|' + str(barToPrev)+ '|' +str(l)
                prevbart_dt  = currentbar_dt
                
                recentlimit = read_vars()
                if barToNow < recentlimit:
                    onesig = l    
##                    Snaptfile = DataDown + today + '.' + sym + '.ticksnaps.csv'
                    RecentTickFile = DataDown + today + '.' + sym + '.RTticks.csv'
                    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
                    for f in tickline:                        
                        onesig.append(f)
                        onesig.append(barToNow)
##                    print onesig
##                    print len(onesig)
                    recentsigs.append(onesig)
    dur = ''
    if len(recentsigs) > 0:
        sigcount =0
        origsigf = 7
        for sig in recentsigs:
            sigcount+=1
            barToNow = sig[len(sig)-1]
            bid = (sig[origsigf +10]).replace('close=','')
            ask = bid#sig[origsigf +6]
            bsize = bid#sig[origsigf +1]
            asize = bid#sig[origsigf +5]
            #######
            action =sig[5]
            tside = 'BUY'
            if action == 'negcrossmcd':
                tside = 'SELL'
            sym =sig[1]
            dur = sig[2]
            decimalboost = float(dboostdict[sym])
            priceinsignal = float(sig[3]/decimalboost)
            sigid = sym + '.' + action + '.' + str(priceinsignal) +'.' + dur
            if sigid == prevsigid:
                pass
            else:        
                pricedrift = round(priceinsignal - float(ask),4)
                timedrift = barToNow                 
                print timedrift, pricedrift, sym, tside,dur, priceinsignal,bid,ask,bsize,asize,barToPrev
                ######  TRAD SENDING STARTS HERE
                if sigcount == len(recentsigs):
                    tranflag = False
                    if dur == '30 secs':
                        tfactor = float(0.5) 
                    else:
                        tfactor = float(1.0)
                    tfactor = float(0.5)
                    tsize = int(max(1,(int(tsizedict[sym]) * tfactor)))
    ##                print 'tsize',tsize
                    onetick = float(tickdict[sym])
                    roundfactor = int(roundfactordict[sym])
                    addamt = onetick * int(entrywiderdict[sym])
                    onetick = float(1/decimalboost)
                    tickrounder = roundfactor
                    if roundfactor == 0:
                        tickrounder = 0.25     
                    ## create contract here
                    techline = symlinedict[sym]
                    ## calculate roundie
                    roundieline = round(float(priceinsignal),roundfactor-2)
    ##                print 'WARNING ... line at: >> ',techline,'roundie = ',roundieline
                    symcontract = ibutiles.create_ticksym(14,sym)
                    ########  poll for a recent price
                    rpu_rp.WriteStringsToFile('pricenow','')
    ########                tws_conn.reqMktData(14,symcontract,'BID',True)
                    sleep(1)
                    for l in rpu_rp.CsvToLines('pricenow'):
                        pricebid =  float(l[0])
                    sleep(1) ## allows oderide to write to window remove later
                    order_id = get_orderid() 
                    if tickrounder != 0:
                        pricenow = round(float(ask),roundfactor)
                    ########################################################
                    sigprice = round(float(priceinsignal)/float(decimalboost),roundfactor)
                    ########################
                    flipsign = int(-1)
                    if tside == 'SELL':
                        flipsign = int(1)
                    entryprice = pricenow + (flipsign * addamt) 
                    orderstring = str(order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(entryprice)
    ##                print orderstring
                    entryorder = ibutiles.create_order('LMT', tsize, tside, entryprice,tranflag,entryprice,entryprice,'entry')        

                    print orderstring
                    prevsigid = sigid     
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now

#############
def create_report(Sigfile,sym,barsize):
    barfile = DataDown + today + '.'+sym+ '.'+ barsize +'both.csv'
    lines = rpu_rp.CsvToLines(barfile)
    numberBars = len(lines)   
    siglines = rpu_rp.CsvToLines(Sigfile)
    numsigs = len(siglines)
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
##    distance to last bar =
##    distance to last signal
##    how old am i in bars
##    average number of sigs in 30 bars  has it flipped alot
##    various modes which keep all sigs, keep last 2, keep last 1
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
########################     
