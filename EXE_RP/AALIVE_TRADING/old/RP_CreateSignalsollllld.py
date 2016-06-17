# -*- coding: utf-8 -*-
import os, sys,os.path
#########################################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
####################
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
import ctypes 
today =  rpu_rp.todaysdateunix()
##today ='20150918'
date = today
#######################
cpfname = EXE + 'signalcontroller.txt'
symbol_list = symdict.keys()
##symbol_list = ['EUR.USD']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
##print barlist
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
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def look_for_dupe_sig(livesigid,livesigtime):
    showflag = 'show'
    livesigepoch = TicksUtile.time_to_epoch(livesigtime)
    if os.path.isfile(sigarea + today +'.recentsigs.csv'): 
        tradedsigs= rpu_rp.CsvToLines(sigarea + today +'.recentsigs.csv')
        showflag = 'show'     
        for lin in tradedsigs:
##            print lin
            if len(lin) > 3:
                sigid = lin[7]
                sigtime = lin[3]
                sigtimeepoch = TicksUtile.time_to_epoch(sigtime)
                timediff = livesigepoch - sigtimeepoch
                if sigid == livesigid and timediff < 100:
                    showflag = 'supress'
    return showflag
#################################
def show_spots(sym,date,limit):
    barfile = DataDown +date +'.' +sym +'.RTtickslastquote.csv'
    rpu_rp.CsvToLines(barfile)
    curprice = float((rpu_rp.CsvToLines(barfile)[0])[5])
##    print curprice
    spotfile = EXE +'es.lines.new.csv'
##    print symlinedict
    filein = DataDown + date + '.' + sym + '.5mins.both.csv'
    lines = rpu_rp.CsvToLines(filein)
    spotlines= rpu_rp.CsvToLines(spotfile)
    for l in spotlines:
        spotp = float(l[0])
        if abs(spotp-curprice) < limit:
            print curprice-spotp,spotp,curprice,sym,'spot prices',limit
#####################
def analyze_1bar_state(sym):
    valStochK = float(rpInd.ShowRecentIndValue(sym,'5mins','StochK',1))
    crosssign = rpInd.ShowRecentIndValue(sym,'5mins','Stoch_CROSS',2)
#######################
def show_bar8_range(start,end,sym,date):
    print 'this is the bar8 range of lines',start,end
    after5lines = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    linecount =0
    trigger = 'inactive'
    for line in after5lines:
        bartime = line[1]
        linecount +=1
##        print line
        if linecount ==1:
            starthi = line[3]
            startlo = line[4]
            print '>>>> BAR 8 HILO = <<<<<', starthi, startlo, bartime
            pass
        curbarhi = line[3]
        curbarlo = line[4]
        if curbarhi < startlo and trigger != 'active':
            print 'going down',line
            trigger = 'active'
        elif curbarlo > starthi and trigger != 'active':
            print 'going up',line
            trigger = 'active'
        else:
            pass
    print '======================'
######################
def make_bars_no_5sec(startmode,durmode):
    for sym in symbol_list:
        if durmode == 'alldurs':
            barlist =  ['1min','3mins', '5mins', '15mins', '1hour', '1day']
            pass
        else:
            barlist = ['1min', '3mins', '5mins', '15mins']##,'78mins']
        for dur in barlist :
##            print dur
            if dur == '1min':
                basisdur = '5secs'
            else:
                basisdur  = '1min'
            TicksUtile.assemble_dur_bars(today,sym,dur,startmode,basisdur)
#################
def make_bars_just_5sec(startmode):
    for sym in symbol_list:
        TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
#################
def make_states(smode,date,symbollist):
    threshold = 0.0
    if smode == 'fullist':
        indlist = ['pivot', 'ATR','R', 'S', 'S2', 'R2','kupper', 'klower','kmid','ema','diffvES','RSI','StochK','Stoch_CROSS','StochD']
    else:
        indlist = ['mcross','mcd','kupper','StochK','Stoch_CROSS','StochD','RSI']
    barlist = ['1min', '3mins', '5mins', '15mins']##,'78mins']

    for sym in symbollist:
        for dur in barlist :
            rpInd.create_states_files(sym,dur,date,threshold,indlist)
#################
def run_8s(sym): 
    if sym == 'ES' and 'bla' == 'bla':
##            show_bar8_range('04:00:00','7:00:00',sym,date) #asia
        show_bar8_range('09:35:00','12:25:00',sym,date) #europe
        show_bar8_range('16:00:10','18:25:00',sym,date) #usa 
###################
def create_latest_state_array(sym):
    indlist = ['mcross','stochD','kupper']
    durlist = ['1min', '3mins', '5mins', '15mins']
    currentstates =[]
    for dur in durlist:
        for ind in indlist:
            lastbar = rpInd.ShowLastBarofInd(sym,dur,ind)
            currentstates.append(lastbar)
    return currentstates
#####################
def create_previous_state_array(sym,barnum):
    indlist = ['mcross','stochD','kupper']
    durlist = ['1min', '3mins', '5mins', '15mins']
    currentstates =[]
    last1minbar = rpInd.ShowABarofInd(sym,'1min','mcross',barnum)
##    print last1minbar
    timeofbar = last1minbar[0]
    print timeofbar    
    for dur in durlist:
        for ind in indlist:
            lastbar = rpInd.ShowABarofIndByTime(sym,dur,ind,timeofbar)
            currentstates.append(lastbar)
    return currentstates
#####################
def rule_tester(currentstates,rule,curprice):
##    print currentstates, 'arrayin' [' 2015-09-18', '17.3051', 'pos', '8.3948', 'slopeup',
##    rule = ['mcross','5mins','stringtest','neg',fnum,maxval,minval,'SELL']
    flag = 'nomatch'
##    print rule
    rind = rule[0]
    rdur = rule[1]
    rtype = rule[2]
    rmin = float(rule[5])
    rmax = float(rule[6])
    rstring = rule[3]
    fnum = int(rule[4])
    raction= rule[7]
    rulename = rind+rdur+rtype+str(rmin)+str(rmax)+rstring+raction
    for l in currentstates:
        sind = l[5]
        sdur = l[8]
        sval = l[fnum]
        if sind == rind and sdur == rdur :
            print rule
            print l
            if rtype == 'stringtest':
                if sval == rstring:
                    flag = raction
                elif rtype == 'priceCompareGT':
                    if float(sval) <  float(curprice):
                        flag = raction
                elif rtype == 'priceCompareLT':
                    if float(sval)  >  float(curprice):
                        flag = raction
                else :
                    if float(sval) > rmin and float(sval) < rmax:
                        flag = raction
        return flag,rulename
#######################
def ruleslist():
    rule1 = 'mcross on all but 1 min'
    rule2 = 'stochd under over 20 80 and sloping and crossing K'
    rule3 = 'threshold use for crosses'
    rule4 = 'if position and mcross opposite dir, close, maybe not revers'
    rule5 ='mcd 15min'
    rule6 = 'rsi'
    indlist = ['mcross','mcd','RSI','StochK','Stoch_CROSS','StochD']
###########################
def parse_signalsNEW(recentsigs):
##    recentsigs = ['ES', 'SELL', 'testname', '1945.75', 'idstr', ' 2015-09-18 21:45:05']
    dur = ''
    if len(recentsigs) > 0:
        sigcount =0
        for sig in sorted(recentsigs):
            sig.append(now)
            print sig
            sigtime = sig[3]
            indvalue = 0.0 #float(sig[len(sig)-2])   <<<<<<<<<<<<<<<<<<
            sym = sig[4]
            sigtype = sig[2]
            priceinsignal = float(sig[5])
            tside =sig[1]
            dur = '5mins' # sig[8]   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            livesigid = sym+tside+dur+sigtype
            sig.append(livesigid)
            showflag =  look_for_dupe_sig(livesigid,sigtime)   #'notsupress'                              
            sigcount+=1
            if showflag != 'supress':
                if tside == 'SELL':
                    beep(soundarea+'sell')
                    print sig
                    beep(soundarea+sym)
##                    beep(soundarea+dur)
                    print '==============='
                elif tside == 'BUY':
                    beep(soundarea+'buy')
                    print sig
                    beep(soundarea+sym)
##                    beep(soundarea+dur)
                    print '==============='
                else:
                    pass
######                RP_Snapshot.snapshot_sym(sym,today)               
                frsigline=[]
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigs.csv', [sig]) 
                rpu_rp.WriteArrayToCsvfileAppend(sigarea + today +'.recentsigsexec.csv', [sig])   
############
def run_rulesets(sym,currentstates,sigtime,curprice):
    c=0
    rulesets =glob.glob('*.rules.csv')
    results=[]
    for rulefile in rulesets:
        ruleset = rpu_rp.CsvToLines(rulefile) # create list based on .rules.
        for rule in ruleset:
            resultboth = rule_tester(currentstates,rule,curprice)
######            print resultboth
            result = resultboth[0]
            c+=1
            if c==1:
                prevresult = result
            if result == prevresult:
                fullmatch = result
                prevresult = result
            else:
                fullmatch = 'failed'
                prevresult = 'failed'
##        print 'finalresult ruleset',fullmatch,rulefile,sigtime
        resultline=[]
        resultline.append('result')
        resultline.append(fullmatch)
        resultline.append(rulefile)
        resultline.append(sigtime)
        resultline.append(sym)
        resultline.append(curprice)
        results.append(resultline)
    return results
    #########################
loopmax = 20000
loop = 0
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 5 #int(read_vars('CycleTime',cpfname))
print 'recent limit is now.. ', recentlimit
prevcycledelay = 2
threshold = 0.0
########################
while loop < loopmax:
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format))) 
    if loop == 0:        
        make_bars_just_5sec('initialize')
        make_bars_no_5sec('initialize','alldurs')
        make_states('fullist',date,['ES'])
##        loop_one_prepareES()
        make_states('fullist',date,symbol_list)
###############       
    factor = 1
    if float(float(loop)/factor) == round((loop/factor),1):
        print 'cycle ', loop
  #####################      
    make_bars_just_5sec('initialize')
    make_bars_no_5sec('initialize','partdurs')
    make_states('part',date,symbol_list)
    ############################  end of bar creation, now run rules....
    for sym in symbol_list:
        curprice = float(RP_Snapshot.recenttick(sym)) * float((dboostdict[sym]))
        currentstates = create_latest_state_array(sym)# need multiple rulesests
#######################   
        recentsigs = run_rulesets(sym,currentstates,now,curprice)
######        run_8s(sym)
        show_spots(sym,date,9.0)
        parse_signalsNEW(recentsigs)
####################      
    loop +=1
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
