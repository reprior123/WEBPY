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
DataDownNoSlash = 'C:/TS/TSIBData'
soundarea = path + 'sounds/'
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
import datetime as dt
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
spaceYtime_format = " %Y-%m-%d %H:%M:%S"
time_format = "%H:%M:%S"
dateFormat = "%Y%m%d"
##############################
cpfname = EXE + 'signalcontroller.txt'
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
##symbol_list = ['NQ']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':
        barlist.append(b)
print barlist
##################
prevsigid = ''
mode = 'livescan'
today =  rpu_rp.todaysdateunix()
yesterday ='20150626'
##today = yesterday
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
def read_varlist(cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    lista =[]
    for line in paramlines:    
        varstring = line[0]
        lista.append(varstring)
    return lista
#########################3
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
def read_vars(varstringin,cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    for line in paramlines:
##        print line
        varstring = line[0]
        if len(line) > 1 and varstring == varstringin:
            varvalue =line[1]
    return varvalue
#########################3
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile(TMP +'pricenow',str(float(msg.pricerpu_rp.WriteStringsToFileAppend(TMP + 'replys',str(msg)))))
#########################3    
loopmax = 2000
loop = 0
global command
command = read_vars('Setting',cpfname)
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = int(read_vars('CycleTime',cpfname))
print 'recent limit is now.. ', recentlimit
sigs = rpu_rp.CsvToLines(sigarea + today +'.sigs.csv')
########################
import winsound, sys
def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
##beep('buyStocks')
###############
prevcycledelay = 2
while loop < loopmax:
    fileage = check_for_CP_change(cpfname)
    if fileage < 30:
        command = read_vars('Setting',cpfname) 
        cycledelay  = int(read_vars('CycleTime',cpfname))
        recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
        print 'cycle delay changed to...',cycledelay
        # change to cycledelay later
        
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))      
    now_dt = dt.datetime.strptime(now, spaceYtime_format)
    
    print 'cycle heartbeat...searching for sigs in last ',recentlimit

    controlflag = True
    if command == 'QUIT-setting':
        controlflag = False   
        print 'got the order to exit program....!!! <<<'   
        loopmax = 1
    ###############
    recentsigs =[]
    rpu_rp.WriteArrayToCsvfile(sigarea +today+'.sigs.csv', []) # flush the file to keep all sigs
    for sym in symbol_list:      
        rpu_rp.WriteArrayToCsvfile(sigarea +sym+'.sigs.csv', []) # flush the file to keep all sigs
        TicksUtile.prepare_tickfilesto5secBars(today,sym) ## merge the 5secddload with 5sec recents > 5sec boths
        ####################################
        for barsize in barlist :
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            decimalboost = dboostdict[sym]
            dur = barsize         
            TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds)        
            DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
            indicator = 'MACROSS'
            TicksUtile.create_state_files(today,sym,dur,indicator)
            indicator = 'MCDiv'
            TicksUtile.create_state_files(today,sym,dur,indicator)
            indicator = 'price'
            TicksUtile.create_state_files(today,sym,dur,indicator)
####################
            macross = rpInd.process_ticks(DurBoth,sym,barsize)
            macdTriggers = rpInd.Trigger_MACD(DurBoth,sym,barsize)
            macd = macdTriggers
            
            lline = rpu_rp.tail_array_to_array(macross,1)
##            print lline
##            statearray =[]
            state = ((lline[0])[5])
            sigbart = ((lline[0])[0])
            sigbart_epoch = int(time.mktime(time.strptime(sigbart, spaceYtime_format)))
            barage = str(round((now_epoch - sigbart_epoch)/int(durinseconds),2))
##            statearray.append(state)
##            print statearray
##            set the state for each sym
            statename = sym+dur.replace(' ','')
            statefile = sigarea +statename +'.MACROSS.state.csv'
            rpu_rp.WriteStringsToFile(statefile, state+dur.replace(' ','')+'since_bars'+barage+',')
            
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigsma.csv', macross)
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', macd)     
##############################         
            prevt = 0
            numsigs = len(macd)
            signum =0
                      
            prevbart_dt = now_dt
            prevbart_epoch = now_epoch
            for l in macd:                
                bart =  l[0]
                bart_dt = dt.datetime.strptime(bart, spaceYtime_format)
                bart_epoch = int(time.mktime(time.strptime(bart, spaceYtime_format)))
                
                barToNow = now_epoch - bart_epoch
                barToPrev =  bart_epoch - prevbart_epoch
                prevbart_epoch = bart_epoch   
##                alerttxt = l[1] + '|' + str(barToNow) + '|' + str(barToPrev)+ '|' +str(l)                   
                if barToNow < recentlimit:
                    onesig = l
                    sym =onesig[1]
                    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
                    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
                    for f in tickline:
##                        print f
                        if 'close' in str(f):                        
                            lasttick = f.split('=')[1]
##                            print 'found'
                    onesig.append(barToNow)
                    onesig.append(barToPrev)
                    onesig.append(lasttick)
                    recentsigs.append(onesig)                 
    dur = ''
    if len(recentsigs) > 0:
        macrossstate = statefile = sigarea +statename +'.MACROSS.state.csv'
        sigcount =0

##        rpu_rp.WriteArrayToCsvfile(sigarea + today +'.recentsigs.csv', []) # flush the file to keep all sigs

        for sig in sorted(recentsigs):
            sym = sig[1]          
            allsigs = rpu_rp.CsvToLines(sigarea +sym+'.sigs.csv')
            hsigs = rpu_rp.grep_array_to_array(allsigs,'1 hour')
            hline = (rpu_rp.tail_array_to_array(hsigs,1))[0]
            hstate = hline[5] +'1hour' + hline[0]
##            print hstate
            sigcount+=1
            offset = 11
##            print sig
            sigtime = sig[0]
            barToPrev=sig[len(sig)-2]
            barToNow = sig[len(sig)-3]
            bid = sig[len(sig)-1]
            ask = bid
            bsize =bid
            asize = bid
            action =sig[5]
            tside = 'BUY'
            if action == 'negcrossmcd':
                tside = 'SELL'
            if tside == 'SELL':
                beep(soundarea+'sellStocks')
            else:
                beep(soundarea+'buyStocks')
            beep(soundarea+sym)
            sym =sig[1]
            dur = sig[2]
            statefile = sigarea +statename +'.MACROSS.state.csv'
            macrossstate = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(statefile),1)
            decimalboost = float(dboostdict[sym])
            priceinsignal = float(sig[3]/decimalboost)
            sigid = sym + '.' + action + '.'  +'.' + dur
            pricedrift = round(priceinsignal - float(ask),4)
            timedrift = barToNow                 
            print timedrift, pricedrift, sym, tside,dur, priceinsignal,bid,barToPrev,sigtime,hstate,macrossstate
            ######################
            ttype = 'LIM'
            limitprice = bid
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
            ########3####
            frsigline=[]
                                                            
            frsigline.append(sym)
            frsigline.append(roundfactor)
            frsigline.append(tside)
            frsigline.append(tsize)
            frsigline.append(ttype)
            frsigline.append(limitprice)
            frsigline.append(addamt)
##            print frsigline
##            frsigs.append(frsigline)
            ####change the append below to write just the latest sig...
            rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigs.csv', [frsigline]) # flush the file to keep all sigs
    loop +=1
    sleep(cycledelay)
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
