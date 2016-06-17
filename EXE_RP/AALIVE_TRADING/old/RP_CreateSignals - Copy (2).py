# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import os.path
from datetime import datetime
#########################################
#########################################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#####################
    
##path = os.getcwd() + '/'
##rootpath = ((path.replace('EXE','|')).split('|'))[0]
##localtagSLASH = '_RP/'
##localtag = '_RP'
##EXEnoslash = rootpath + 'EXE' + localtag
##sys.path[0:0] = [EXEnoslash]
##EXE = EXEnoslash + '/'
##DATA = rootpath + 'DATA' + localtagSLASH
##TMP = rootpath + 'TMP' + localtagSLASH
##DataDown = 'C:/TS/TSIBData/'
##DataDownNoSlash = 'C:/TS/TSIBData'
##sigarea = DataDown + 'Signals/'
##statearea = DataDown + 'Signals/states/'
##DataDownNoSlash = 'C:/TS/TSIBData'
##soundarea = path + 'sounds/'
#######################################
global recentlimit, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
today =  rpu_rp.todaysdateunix()
##today ='20150817'
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
ticktypedict = rpu_rp.create_dict(libsyms,0,11)

libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)
libsymNEWS = EXE + 'library.symNEWSTIMES.csv'
symNEWSdict = rpu_rp.create_dict(libsymlines,0,2)
symbol_list = symdict.keys()
##symbol_list = ['ES']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
print barlist
##################
prevsigid = ''
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
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
def recenttick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickvalue = float(tickvaluedict[sym])
    if os.path.isfile(RecentTickFile) :
        tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
        lasttick = rounderrp(float(tickline[5]),tickvalue)
    else:
        lasttick = 9999
    return lasttick
#################
loopmax = 20000
loop = 0
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 5 #int(read_vars('CycleTime',cpfname))
print 'recent limit is now.. ', recentlimit
########################
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def look_for_dupe_sig(livesigid):
    if os.path.isfile(sigarea + today +'.recentsigs.csv'): 
        tradedsigs= rpu_rp.CsvToLines(sigarea + today +'.recentsigs.csv')
        showflag = 'show'
        for lin in tradedsigs:
            if len(lin) > 3:
                sigid = lin[3]
                if sigid == livesigid:
                    showflag = 'supress'
                    print 'dupe ignored...',sigid, now
    else:
        showflag = 'show'
    return showflag
#################################
def create_slicendice():
    print 'slicedice'
    #analyze
prevcycledelay = 2
import RP_Snapshot
########################
print 'got to loop'
while loop < loopmax:
    if loop == 0:
        for sym in symbol_list:
            startmode = 'initialize'
            TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
            barlist = ['1min','3mins', '15mins', '1hour', '1day']
            for dur in barlist :            
                durinseconds = secdict[dur]
                basisdur = '5secs'
                basisfile = DataDown +today+'.'+sym+'.'+basisdur+'.both.csv'
                TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds,startmode,basisfile)
                threshold = 0.0
                indlist = ['pivot', 'R', 'S', 'S2', 'R2','kupper', 'klower', 'kmid','ema','mcross', 'mcd']
                rpInd.create_states_files(sym,dur.replace(' ',''),today,threshold,indlist)
    ####################################
    if float(float(loop)/10) == round((loop/10),1):
        print 'cycle ', loop   
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))      
    now_dt = dt.datetime.strptime(now, spaceYtime_format)   
    ###############
    recentsigs =[]
    startmode = 'bothfile'
    startmode = 'initialize'
    for sym in symbol_list:
        TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
        ####################################
        barlist = ['1min', '3mins', '5mins', '15mins']
        for dur in barlist :
            if dur == '1min':
                basisdur = '5secs'
                pass
            else:
                basisdur  = '1min'           
            durinseconds = secdict[dur]
            basisfile = DataDown +today+'.'+sym+'.'+basisdur+'.both.csv'
            TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds,startmode,basisfile)
##            DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
            threshold = 0.0
##            indlist = ['pivot', 'R', 'S', 'S2', 'R2','kupper', 'klower', 'kmid','ema','mcross', 'mcd']
##            indlist = ['pivot', 'R', 'S', 'S2', 'R2','mcross']
##            indlist = ['pivot', 'mcross','mcd']
            indlist = ['mcross','mcd']
            rpInd.create_states_files(sym,dur,today,threshold,indlist)        
####################
        state15 = rpInd.ShowRecentState(sym,'15mins','mcross','noboost')
        stateAge15 = rpInd.ShowRecentAge(sym,'15mins','mcross','noboost')
##        state5 = rpInd.ShowRecentState(sym,'5mins','mcross')
##        stateAge5 = rpInd.ShowRecentAge(sym,'5mins','mcross')        
        barlist = ['1min', '3mins', '5mins', '15mins']

        for dur in barlist :
            threshold = 0.0
            ALLTriggers=[]
            lasttwo = []

            if dur != '1111min':
                Triggers = rpInd.Trigger_from_states(sym,dur,'mcross')
                lasttwo = rpu_rp.tail_array_to_array(Triggers,1)
            for a in lasttwo:
                ALLTriggers.append(a)
            Triggers = rpInd.Trigger_from_states(sym,'15mins','mcd')
            lasttwo = rpu_rp.tail_array_to_array(Triggers,1)
            for a in lasttwo:
                ALLTriggers.append(a)                
##            threshold = float(-0.20)
##            maCrossNEARTriggers = rpInd.Trigger_MACross(DurBoth,sym,dur,threshold,'manearcross')
##            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', ALLTriggers)
############################         
            prevt = 0
            numsigs = len(ALLTriggers)
            signum =0                      
            prevbart_dt = now_dt
            prevbart_epoch = now_epoch
##            2015-08-24 17:35:05,0.0245,pos,0.0646,slopeup,kupper,USD.JPY,poscrxx,1min,118.43,118.36,118.36,5            
            for onesig in ALLTriggers:
                bart =  onesig[0]
                action =onesig[7]
                bart_dt = dt.datetime.strptime(bart, spaceYtime_format)
                bart_epoch = int(time.mktime(time.strptime(bart, spaceYtime_format)))         
                barToNow = now_epoch - bart_epoch
##                barToPrev =  bart_epoch - prevbart_epoch
##                prevbart_epoch = bart_epoch
##                print bart_epoch, barToNow, barToPrev, bart
                if barToNow < recentlimit :
                    tflag = 'nopass'
##                    print 'recent15 min state and age:', state15, stateAge15,sym
                    posstate = rpInd.ShowRecentPositionState(sym)
                    if action == 'negcrxx' and state15 == 'neg' and dur != '1min':
##                        print 'is a sell'
                        tflag = 'passedtest'
                    elif action == 'poscrxx' and state15 == 'pos' and dur != '1min':
##                        print 'is a buy'
                        tflag = 'passedtest'
                        pass
                    elif action == 'poscrxx' and posstate == 'SELL':
                        tflag = 'passedtest'
                        pass
                    elif action == 'negcrxx' and posstate == 'BUY':
                        tflag = 'passedtest'
                        pass
                    else:
##                        print action, ' signal failed on ... ',dur,sym
                        pass
                    if tflag == 'passedtest':
                        lasttick = recenttick(sym)
                        onesig.append(barToNow)
                        onesig.append('xx')
                        onesig.append(lasttick)
                        recentsigs.append(onesig)
    dur = ''
    if len(recentsigs) > 0:
        sigcount =0
        for sig in sorted(recentsigs):
            sigtime = sig[0]
            sym = sig[6]
            sigtype = sig[5]
##            barToPrev=sig[len(sig)-2]
##            barToNow = sig[len(sig)-3]
            priceinsignal = float(sig[len(sig)-1])
            action =sig[7]
            dur = sig[8]
            livesigid = sym+action+dur.replace(' ','')  + sigtype          
            showflag =  look_for_dupe_sig(livesigid)    #'notsupress'                              
            sigcount+=1
            if showflag != 'supress':
                indlist = ['mcross']#, 'R', 'S'] #'1hour',
                stateinfo = ''
                durstatelist = ['15mins', '1hour', '1day']
                tside = 'BUY'
                if 'negcrxx' in action:
                    tside = 'SELL'
                if tside == 'SELL':
                    beep(soundarea+'sellStocks')
                else:
                    beep(soundarea+'buyStocks')
                beep(soundarea+sym)

                print '==============='
                RP_Snapshot.snapshot_sym(sym)               
                print '==============='
                print sym, tside, sigtype, dur, sigtime, now, priceinsignal
########                rpInd.create_lines(sym,bid)
##                print symNEWSdict[sym]
                frsigline=[]                                          
                frsigline.append(sym)
                frsigline.append(tside)
                frsigline.append(priceinsignal)
                frsigline.append(livesigid)
                frsigline.append(sigtime)
                frsigline.append(now)
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigs.csv', [frsigline]) 
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigsexec.csv', [frsigline]) 
    loop +=1
####################
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
def create_report(Sigfile,sym,barsize):
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
    print 'if i am 20 bars old in signal, start with trail stop depends on dur...shotrt dur = short age'
##    average number of sigs in 30 bars  has it flipped alot
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#################
