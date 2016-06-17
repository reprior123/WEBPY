# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import os.path
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
statearea = DataDown + 'Signals/states/'
DataDownNoSlash = 'C:/TS/TSIBData'
soundarea = path + 'sounds/'
#######################################
global recentlimit, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
from datetime import datetime
import datetime as dt
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
spaceYtime_format = " %Y-%m-%d %H:%M:%S"
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

tickvaluedict = rpu_rp.create_dict(libsyms,0,8)
tsizedict = rpu_rp.create_dict(libsyms,0,7)
showdecimaldict = rpu_rp.create_dict(libsyms,0,9)
entrywiderdict = rpu_rp.create_dict(libsyms,0,10)

libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)

libsymNEWS = EXE + 'library.symNEWSTIMES.csv'
symNEWSdict = rpu_rp.create_dict(libsymlines,0,2)
symbol_list = symdict.keys()
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
print barlist
##################
prevsigid = ''
today =  rpu_rp.todaysdateunix()
##today ='20150722'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
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
########################
def recenttick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    if os.path.isfile(RecentTickFile) :
        tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
        for f in tickline:
            if 'close' in str(f):                        
                lasttick = f.split('=')[1]
    else:
        lasttick =1
    return lasttick
#################
loopmax = 2000
loop = 0
global command
command = read_vars('Setting',cpfname)
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = int(read_vars('CycleTime',cpfname))
print 'recent limit is now.. ', recentlimit
########################
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def gatherline(sym,ind):
    dur = '1day'
    if ind == 'pivot':
        indfile = statearea + sym + '.' + dur + '.' + 'pivot.state.csv'
    elif  ind == 'R' :
        indfile = statearea + sym + '.' + dur + '.' + 'R.state.csv'
    elif  ind == 'R' :
        indfile = statearea + sym + '.' + dur + '.' + 'R2.state.csv'
    elif  ind == 'R' :
        indfile = statearea + sym + '.' + dur + '.' + 'S2.state.csv'
    else:
        indfile = statearea + sym + '.' + dur + '.' + 'S.state.csv'
    lineprice = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(indfile),1)[0]
    return lineprice
################################3
def look_for_dupe_sig(livesigid):
    if os.path.isfile(sigarea + today +'.recentsigs.csv'): 
        tradedsigs= rpu_rp.CsvToLines(sigarea + today +'.recentsigs.csv')
        showflag = 'show'
        for lin in tradedsigs:
            if len(lin) > 3:
                sigid = lin[7]
                if sigid == livesigid:
                    showflag = 'supress'
                    print 'dupe ignored...',sigid, now
    else:
        showflag = 'show'
    return showflag
#################################
def create_statesdaily():
    for sym in symbol_list:      
        for barsize in barlist :
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            dur = barsize
            TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds)  
            DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
            indlist = ['pivot', 'R', 'S', 'S2', 'R2']
            for indicator in indlist:
##                print sym
                indarr = rpInd.GetPivots(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
            indlist2 = ['kupper', 'klower', 'kmid']
            for indicator in indlist2:
    ##                print indicator
                indarr = rpInd.GetKupper(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
    ##                keltner_channel_upper(highs,lows,closes,mult)
            indlist3 = ['ema']
            for indicator in indlist3:
    ##                print indicator
                indarr = rpInd.GetEMA(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
###########################3
def create_lines(sym,clprice):
    linelist = ['R', 'Pivot', 'S', 'S2', 'R2']
    prevval = 99999
    for line in linelist:        
        newline = float(gatherline(sym,line)[1])
        newlinediff = float(clprice - newline)
        if abs(newlinediff)< prevval:
            prevval = abs(newlinediff)
            livetag = line
            activline = newline
    if newlinediff  < 0 :
        linestatus = 'below'
    else:
        linestatus = 'above'
    print livetag, activeline, newlinediff, linestatus, clprice
####################
def create_slicendice():
    #analyze
prevcycledelay = 2
########################
print 'got to loop'
while loop < loopmax:
    if loop == 0:
        create_statesdaily()
    if (round((loop/10),-1) - loop) == 0:
        print 'cycle ', loop
    fileage = check_for_CP_change(cpfname)
    if fileage < 50:
        command = read_vars('Setting',cpfname) 
        cycledelay  = int(read_vars('CycleTime',cpfname))
        recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
        print 'cycle delay changed to...',cycledelay
        # change to cycledelay later      
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))      
    now_dt = dt.datetime.strptime(now, spaceYtime_format)   
##    print 'ccreate sigs searching for sigs in last ',recentlimit
    ###############
    recentsigs =[]
##    symbol_list = ['ES']
    for sym in symbol_list:
##        print sym
        rpu_rp.WriteArrayToCsvfile(sigarea +sym+'.sigs.csv', []) # flush the file to keep all sigs
        TicksUtile.prepare_tickfilesto5secBars(today,sym) ## merge the 5secddload with 5sec recents > 5sec boths
        ####################################
        rpu_rp.WriteArrayToCsvfile(sigarea +sym+'.sigs.csv', [])

        for barsize in barlist :            
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            dur = barsize
            TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds)
            DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
            indlist = ['MACROSS', 'MCDiv', 'price']
            for indicator in indlist:  
                indarr = rpInd.GetStates(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
            indlist = ['klower', 'kmid', 'kupper']
            for indicator in indlist:  
                indarr = rpInd.GetKupper(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)          
####################
            macdTriggers = rpInd.Trigger_MACD(DurBoth,sym,barsize)
            maCrossTriggers = rpInd.Trigger_MACross(DurBoth,sym,barsize)
            for a in maCrossTriggers:
                macdTriggers.append(a)              
            state = 'seefile'
##            sigbart = ((lline[0])[0])
##            sigbart_epoch = int(time.mktime(time.strptime(sigbart, spaceYtime_format)))
##            barage = str(round((now_epoch - sigbart_epoch)/int(durinseconds),2))
            barage = 'need barage'
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', macdTriggers)
############################         
            prevt = 0
            numsigs = len(macdTriggers)
            signum =0                      
            prevbart_dt = now_dt
            prevbart_epoch = now_epoch
            for l in macdTriggers:
                bart =  l[0]
                bart_dt = dt.datetime.strptime(bart, spaceYtime_format)
                bart_epoch = int(time.mktime(time.strptime(bart, spaceYtime_format)))         
                barToNow = now_epoch - bart_epoch
                barToPrev =  bart_epoch - prevbart_epoch
                prevbart_epoch = bart_epoch   
                if barToNow < recentlimit:
                    onesig = l
                    sym =onesig[1]
                    lasttick = recenttick(sym)
                    onesig.append(barToNow)
                    onesig.append(barToPrev)
                    onesig.append(lasttick)
                    recentsigs.append(onesig)
    dur = ''
    if len(recentsigs) > 0:
##        macrossstate = statefile = sigarea +statename +'.MACROSS.state.csv'
        sigcount =0
        for sig in sorted(recentsigs):
            sigtime = sig[0]
            sym = sig[1]
            sigtype = sig[5]
            barToPrev=sig[len(sig)-2]
            barToNow = sig[len(sig)-3]
            bid = sig[len(sig)-1]
            action =sig[5]
            dur = sig[2]
            livesigid = sym+action+dur.replace(' ','')
            
            showflag = look_for_dupe_sig(livesigid)
                                 
            sigcount+=1
##            if sigcount == len(recentsigs):
            if showflag != 'supress':
                indlist = ['MACROSS']#, 'R', 'S']
##                indlist = ['MACROSS', 'MCDiv', 'price', 'kupper', 'kmid', 'klower', 'pivot', 'R', 'S']
                durstatelist =['1hour', '15mins' ]
##                durstatelist =['1hour', '15mins', '3mins']
                stateinfo = ''
                for durstate in durstatelist:
                    stateinfo += durstate #+ '\n'
                    for indicator in indlist:  
                        sfile = rpu_rp.CsvToLines(statearea +sym+'.' + durstate +'.'+ indicator +'.state.csv')
                        hline = (rpu_rp.tail_array_to_array(sfile,1))[0]
                        stateinfo += str(hline[1:4])+'\n'
    ##############################            
                tside = 'BUY'
                if 'negcrs' in action:
                    tside = 'SELL'
                if tside == 'SELL':
                    beep(soundarea+'sellStocks')
                else:
                    beep(soundarea+'buyStocks')
                beep(soundarea+sym)
                priceinsignal = float(sig[3]/1)
                pricedrift = round(priceinsignal - float(bid),4)
                timedrift = barToNow
                print '==============='
                
                print sym, tside, sigtype, dur, pricedrift, sigtime, now
                create_lines(sym,bid)
##                print symNEWSdict[sym]
##                print timedrift,sym, tside,dur, priceinsignal,barToPrev,sigtime,pricedrift,now
                print stateinfo
                ######################
                ttype = 'LIM'
                limitprice = bid
                tfactor = float(0.5)
                tsize = int(max(1,(int(tsizedict[sym]) * tfactor)))
                tickvalue = float(tickvaluedict[sym])
                showdecimal = int(showdecimaldict[sym])
                addamt = tickvalue * int(entrywiderdict[sym])

                frsigline=[]                                          
                frsigline.append(sym)
                frsigline.append(showdecimal)
                frsigline.append(tside)
                frsigline.append(tsize)
                frsigline.append(ttype)
                frsigline.append(limitprice)
                frsigline.append(addamt)
                frsigline.append(livesigid)
                frsigline.append(sigtime)
                frsigline.append(tickvalue)
                frsigline.append(now)
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigs.csv', [frsigline]) 
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigsexec.csv', [frsigline]) 
    loop +=1
####################
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
##    distance to last signal
##    how old am i in bars
##    average number of sigs in 30 bars  has it flipped alot
##    various modes which keep all sigs, keep last 2, keep last 1   
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#################
