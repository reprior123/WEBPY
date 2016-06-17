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
##symbol_list = ['USD.JPY']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':
        barlist.append(b)
##barlist = ['5 mins']
print barlist
##################
prevsigid = ''
mode = 'livescan'
today =  rpu_rp.todaysdateunix()
yesterday ='20150609'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
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
    return int(var['TimeLimitRecentSigs'])
############################
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile(TMP +'pricenow',str(float(msg.price)) +',')
##        print 'writing realtime price to pricenow file'
##    print "Server Response: %s, %s" % (msg.typeName, msg)
    rpu_rp.WriteStringsToFileAppend(TMP + 'replys',str(msg))
####################
global tws_conn
tws_conn = Connection.create(port=7496, clientId=66)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(localreply_handler)
###################
def get_orderid():
################    tws_conn.reqIds(100)
    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
##        order_id = 122
    return order_id
###################################
recentlimit = read_vars()
print 'recent limit is now.. ', recentlimit
##################     
loopmax = 2000
loop = 0
global command
command = 'STOP-RUN-setting'
sigs = rpu_rp.CsvToLines(sigarea + today +'.sigs.csv')
########################
controlfname = TMP + 'CreateNSendcontroller.txt'
cycledelay = int(20)
import winsound, sys
def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
beep('buyStocks.wav')
prevcycledelay =2
while loop < loopmax:
    command = (rpu_rp.CsvToLines(controlfname)[0])[0]
    cycledelay = int((rpu_rp.CsvToLines(controlfname)[0])[1])
    controlflag = True
    if command == 'QUIT-setting':
        controlflag = False   
        print 'got the order to exit program....!!! <<<'   
        loopmax = 1
    ###############
    if cycledelay != prevcycledelay:
        print 'cycle delay changed to...',cycledelay
    prevcycledelay = cycledelay
    loop +=1
    sleep(cycledelay)
    now = datetime.strftime(datetime.now(),time_format)
##    print command,'com setting timedrift..pricedrift',now
    recentsigs =[]
    for sym in symbol_list:
        rpu_rp.WriteArrayToCsvfile(sigarea +today+'.sigs.csv', '') # flush the file to keep all sigs
        rpu_rp.WriteArrayToCsvfile(sigarea +sym+'.sigs.csv', '') # flush the file to keep all sigs
        for barsize in barlist:
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            decimalboost = dboostdict[sym]
            dur = barsize
                ##        RTticks > RTbars[5secBars]
            RTticksFile = DataDown +today+'.'+sym+ '.RTticks.csv'
            RTBarsin = rpu_rp.CsvToLines(RTticksFile)
            
            import datetime as dt
            june1= dt.datetime.strptime(' 2015-06-01 12:12:12', ' %Y-%m-%d %H:%M:%S')
            RTBars5Sec=TicksUtile.create_bars_from_barsAll(RTBarsin,today,sym,'5 secs',1,june1,'RTbars')

    ##        5Sec.BarsHist rcvd
            HistBars5SecFile = DataDown +today+'.'+sym+ '.5 secs' + '.BarsHist.csv'
            HistBars5Sec = rpu_rp.CsvToLines(HistBars5SecFile)
            
    ##        HistBars5Sec + RTBars5Sec > 5SecBars.Both
            BothBars5Sec = []
            for a in HistBars5Sec:
                BothBars5Sec.append(a)
            for b in RTBars5Sec:
                BothBars5Sec.append(b)
            BothBars5SecClean= TicksUtile.CleanBarOverlap(BothBars5Sec)
            
    ##        5SecBars.Both > [dur].recentBars via create bars with bars
            #### this will write the recent[dur]files to be used by the next merging
            ##   of Histdur files to recent
            lastHistBartime = TicksUtile.time_of_last_histbar(today,sym,dur,'newformat')
            TicksUtile.create_bars_from_barsAll(BothBars5SecClean,today,sym,dur,durinseconds,lastHistBartime,'normal')
            
            ##        [dur].recentBars + [dur]HistBars = [dur].both [overlapping solved buy cutofftime above
            # this creates bars to sym.bars file and uses the recent file
            filetomerge = DataDown +today+'.'+sym+'.'+barsize+'.ddload.csv'
            lines = TicksUtile.merge_bar_files(filetomerge)
            
##            rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+'.'+barsize+ '.recent5Sec.csv',BothBars5SecClean)
##            recent5SecBars = TicksUtile.create_bars_fromRTBars(RTBarsin,today,sym,barsize,timecutoff) ##<<<<
            ##write the recent bars to a file here
##            rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+'.'+barsize+ '.recent5Sec.csv',recentBars)
##            merge_bar_files_withtimecutoff(filename1,filename2,outfile)
            
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
                    ## now take this list for all scanned syms and execute the last one in the list
                    ## if the last one in  the list keeps repeating, the dupe signal will stop it
                    ## if the last signal keeps alternating, the dupe will execute repeatedly                
                    RecentTickFile = DataDown + today + '.' + sym + '.RTticks.csv'
                    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
                    for f in tickline:
##                        print f
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
            beep('buyStocks.wav')
            sigcount+=1
            barToNow = sig[len(sig)-1]
            bid = (sig[origsigf +10]).replace('close=','')
            ask = bid
            bsize =bid
            asize = bid
            #######
            action =sig[5]
            tside = 'BUY'
            if action == 'negcrossmcd':
                tside = 'SELL'
            sym =sig[1]
            dur = sig[2]
            decimalboost = float(dboostdict[sym])
            priceinsignal = float(sig[3]/decimalboost)
            sigid = sym + '.' + action + '.'  +'.' + dur
            pricedrift = round(priceinsignal - float(ask),4)
            timedrift = barToNow                 
            print timedrift, pricedrift, sym, tside,dur, priceinsignal,bid,ask,bsize,asize,barToPrev
            ######  TRAD SENDING STARTS HERE
            if sigcount == len(recentsigs):
                tranflag = False
                if command != 'NOTRANSMIT-setting':
                    tranflag = True   
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
                print 'WARNING ... line at: >> ',techline,'roundie = ',roundieline, command,now
                symcontract = ibutiles.create_ticksym(14,sym)
                ########  poll for a recent price
                rpu_rp.WriteStringsToFile('pricenow','')
                tws_conn.reqMktData(14,symcontract,'BID',True)
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
                if command == 'DONOTPLACE-setting':
##                    print 'flag said do not place!!!!!'
                    pass
                else:
                    if sigid == prevsigid:
                        print 'dupe signal,  no place'
                    else:
##                        tws_conn.placeOrder(order_id, symcontract, entryorder)
                        rpu_rp.WriteStringsToFileAppend(TMP +'Entry.orders.Sent.csv',orderstring)
                        print 'placing order'
                        print orderstring
                prevsigid = sigid     
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
print 'disconnecting.. done..'
tws_conn.disconnect()
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
