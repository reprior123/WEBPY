import os, sys
path = os.getcwd() + '/'
EXEnoslash = ((path.replace('\\AALIVE_TRADING','|')).split('|'))[0]
rootpath = ((path.replace('EXE','|')).split('|'))[0]
sys.path[0:0] = EXEnoslash
localtag = ((EXEnoslash.replace('EXE','|')).split('|'))[1] #'_RP'
print localtag,'is local'
#########################################
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
##    print var, nd[var]
    locals()[var] = nd[var]
##################
global recentlimit, time_format,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile,RulesEngine, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
import ctypes
global date
date = today # yesterday # today  ######## <<<<<<<
style = ''
now = datetime.strftime(datetime.now(),spaceYtime_format)
current_time = datetime.now().time()
#######################
btmode = 'bla'
if localtag == '_RPBTEST':    
    btmode = 'BACKTEST'
    date = yesterday
#########################
cpfname = EXE + 'signalcontroller.txt'
symbol_list = ['ES', 'CL', 'FDAX'] #symbol_list2
print symbol_list
prevsigid = ''
##########################################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def look_for_dupe_sig(livesigid,livesigtime,delay):
    showflag = 'show'
    livesigepoch = TicksUtile.time_to_epoch(livesigtime)
    if os.path.isfile(sigarea + date +'.recentsigs.csv'):
        tradedsigs= rpu_rp.CsvToLines(sigarea + date +'.recentsigs.csv')
        showflag = 'show'
        for lin in tradedsigs:
##            print lin
            if len(lin) > 3:
##                print lin
                sigid = lin[9]
                sigtime = lin[3]
##                print sigid,sigtime,livesigid,livesigtime
                sigtimeepoch = TicksUtile.time_to_epoch(sigtime)
                timediff = livesigepoch - sigtimeepoch
                if sigid == livesigid and timediff < delay:
                    showflag = 'supress'
    return showflag
#################################
def show_spots(sym,date,limit,spotfile):
    curprice = float(TicksUtile.recenttick(sym,'recent'))
    spotlines= rpu_rp.CsvToLines(spotfile)
    print 'RangeLineFader is  ',limit,' Handles on ',sym, ' Future'
    for l in spotlines:
        spotp = float(l[0])
        if len(l) > 1 :
##            print l
            spotid = l[1]
            pass
        else:
            spotid=''
        distance = abs(spotp-curprice)
        if (spotp-curprice) > 0:
            underover = 'under'
        else:
            underover = 'over'
        if distance < limit:
##            print curprice-spotp,spotp,curprice,sym,'spot prices',limit
            if underover == 'under':
                print ('SELL at %8.2f %s| %s | %4.2f | %8.2f  ...is this pass #1 or #2?' % (spotp,spotid,sym,distance,curprice))
##                print 'ready to SELL at ',spotp, 'how manypasses?',curprice,sym,distance
            else:
##                print 'ready TO BUY at ',spotp, 'how manypasses?',curprice,sym,distance
                print ('BUY  at %8.2f %s| %s | %4.2f | %8.2f  ...is this pass #1 or #2?' % (spotp,spotid,sym,distance,curprice))
#####################
def make_bars_no_5sec(date,startmode,symbol_list,barlist):
    for sym in symbol_list:
        for dur in barlist :
            if dur == '1min':
                basisdur = '5secs'
            else:
                basisdur  = '1min'
            TicksUtile.assemble_dur_bars(date,sym,dur,startmode,basisdur)
##            print 'creating bars',dur,basisdur,sym
#################
def make_bars_just_5sec(date,startmode,symbol_list):
    for sym in symbol_list:
##        print 'prepare_tickfilesto5secBars', date,startmode, symbol_list
        TicksUtile.prepare_tickfilesto5secBars(date,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
#################
def make_states(date,symbol_list,barlist,indlist):
    threshold = 0.0
    for sym in symbol_list:
        for dur in barlist :
            rpInd.create_states_files(sym,dur,date,threshold,indlist)
#################
def create_latest_state_array(btestmode,sym,barlist,indlist):
##    indlist = partindlist
    currentstates =[]
    for bar in barlist:
        for ind in indlist:
##            print bar,ind,'creating latest statearrays'
            lastbar = rpInd.ShowLastBarofInd(sym,bar,ind)
            currentstates.append(lastbar)
    return currentstates
#####################
def create_previous_state_array(btestmode,sym,barnum,backtestdur):
    durlist = barlist_Recent
    currentstates =[]
    last1minbar = rpInd.ShowABarofInd(sym,backtestdur,'mcross',barnum) ## was 1min ### this controls the backtester!!
    timeofbar = last1minbar[0]
    for dur in durlist:
        for ind in indlist:
            lastbar = rpInd.ShowABarofIndByTime(sym,dur,ind,timeofbar,barnum)
            currentstates.append(lastbar)
    return currentstates,timeofbar
#####################
def parse_signalsNEW(rulesetoutput):
##    [['result', 'SELL', 'stochkeasy1minSELL.rules.csv', ' 2015-09-23 08:16:05', 'CL', 46.36]]
    dur = ''
    if len(rulesetoutput) > 0:
        sigcount =0
        for sig in rulesetoutput:
            if len(sig) > 0  and sig[1] != 'nomatch':
                sig.append(now)
                sigtime = sig[3]
                nowepoch  =  TicksUtile.time_to_epoch(now)
##                print sig
                sigepoch  =  TicksUtile.time_to_epoch(sigtime)
                elapsed = nowepoch - sigepoch
##                print elapsed
##                print sig,'sigline',elapsed
                sigtime = sig[3]
                indvalue = 0.0 #float(sig[len(sig)-2])   <<<<<<<<<<<<<<<<<<
                sym = sig[4]
                sigtype = sig[2]
                priceinsignal = float(sig[5]) ### need to unboost the price...
                dboost = dboostdict[sym]
                newprice = priceinsignal / float(dboost)
                sig[5] = newprice
                tside =sig[1]
                dur = '0mins' # sig[8]   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                livesigid = sym+tside+dur+sigtype
                sig.append(livesigid)
                showflag = look_for_dupe_sig(livesigid,sigtime,delaydupetime)   #'notsupress'
                sigcount+=1
######                print sym,tside,sigtype,sigtime,elapsed,str(newprice)
##                if btmode == 'BACKTEST':
##                    soundarea = 'gg'
                if showflag != 'supress':
                    if tside == 'SELL':
####                        beep(soundarea+'sell')
                        print sig
####                        beep(soundarea+sym)
                        print '==============='
##                        Mbox('BuySignal', sig, style)
                    elif tside == 'BUY':
####                        beep(soundarea+'buy')
                        print sig
####                        beep(soundarea+sym)
                        print '==============='
##                        Mbox('BuySignal', sig, style)
                    else:
                        print 'supressing'
    ######                RP_Snapshot.snapshot_sym(sym,date)
                    frsigline=[]
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + date +'.recentsigs.csv', [sig])
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + date +'.recentsigsexec.csv', [sig])
####################
def linetagger(spotline,sym):
    print spotline, 'checking if tagged in last 5 minutes'
    ## am i under or over line at start of 5 mins?...under
    ##diff to spotline = spotline - recentprice
    ## if diff < 0:  then status = tagged print status, spotline, curprice
    ## followthru amount ?
#########################
if btmode == 'BACKTEST':
    loopmax = 1
else:
    loopmax = 20000
loop = 0
delaydupetime = 200
recentlimit = 5000000  # int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 9 #int(read_vars('CycleTime',cpfname))
print 'Signals within the last ',recentlimit, 'Seconds will be ignored'
prevcycledelay = 2
threshold = 0.0
barlist = barlist_All
print barlist
print symbol_list
backtestdur = '5mins'   #### <<<<<<
btestlimit = rpInd.ShowBarCountofInd(symbol_list[0],backtestdur,'mcross')   ### 1000
print btestlimit,'testlimit...'
########################
while loop < loopmax:
##    print "\n" * 50
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))
    if loop == 0 :
        indlist = indlist_All
        startmode = 'initialize'
        make_bars_just_5sec(date,startmode,symbol_list)  ## make_bars_just_5sec(date,startmode,symbol_list):
        barlist = barlist_All
        make_bars_no_5sec(date,startmode,symbol_list,barlist) #def make_bars_no_5sec(date,startmode,symbol_list,barlist)
        make_states(date,['ES'],barlist,indlist) #make_states('fullist',date,['ES'])
        make_states(date,symbol_list,barlist,indlist) #make_states('fullist',date,symbol_list)
        tanswer = raw_input('createtable? ')
        if tanswer == 'y':
            rpInd.CreateIndvalueTable(indlist_part1,['1min','5mins','15mins'],['ES','FDAX','CL'],libarea +'indlevels.csv')
        indlistnew = ['pivot'] #indlist_lines2
        for indline in indlistnew:
            lineval = rpInd.ShowLastBarofInd('ES','1day',indline)[1]
            print lineval,indline
            rpu_rp.WriteArrayToCsvfile(sigarea +'ES.daily.spotlines2.csv', [['1','']])            
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +'ES.daily.spotlines2.csv', [[lineval,indline]])
    factor = 1
    limitlines = 5.0
    if float(float(loop)/factor) == round((loop/factor),1):
        print 'cycle ', loop
        sym = 'ES'
        spotfile = libarea + 'spotlines.' + sym+ '.csv'
        show_spots(sym,date,limitlines,spotfile)
        spotfile = sigarea +'ES.daily.spotlines2.csv'
        show_spots(sym,date,limitlines,spotfile)
########        symd = 'FDAX'
########        limitlinesd = 10.0
########        show_spots(symd,date,limitlinesd)
  #####################
    if btmode != 'BACKTEST':
        make_bars_just_5sec(date,startmode,symbol_list)
        barlist =   barlist_All #barlist_Recent
        barlist = ['1min', '3mins', '5mins','15mins', '1hour']
        make_bars_no_5sec(date,startmode,symbol_list,barlist)
####        startmode = 'bartobar'
####        barlist = barlist_78
####        make_bars_no_5sec(date,startmode,symbol_list,barlist)
        barlist = barlist_All #barlist_Recent
        indlist = indlist_part
##        indlist = ['bbandlower']
        make_states(date,symbol_list,barlist,indlist)  #def make_states(date,symbol_list,barlist,indlist):
    ############################  end of bar creation, now run rules....
##    symbol_list = ['ES']
    for sym in symbol_list:
##        print sym
        curprice = float(TicksUtile.recenttick(sym,'recent')) * float((dboostdict[sym]))
        if btmode == 'BACKTEST':
            lbarnum = btestlimit
            while lbarnum > 0:
##                print lbarnum,sym
                lbarnum -=1
                currentstates = create_previous_state_array(btmode,sym,lbarnum,backtestdur)[0]
                timeloop =      create_previous_state_array(btmode,sym,lbarnum,backtestdur)[1]
                print timeloop,lbarnum
##                for b in currentstates:
##                    print b
                rulesetoutput = RulesEngine.run_rulesets(sym,currentstates,now,curprice)
##                print rulesetoutput
                for r in rulesetoutput:
                    if r[1] != 'nomatch':
                        print r
                parse_signalsNEW(rulesetoutput)
        else:  ## if not backtest, just take the most recent line and ruletest
            barlist = barlist_All
            indlist = indlist_All  #['mcross','AO','AOAcc'] #indlist_All  beware this needs to open up for more rules
            currentstates = create_latest_state_array(btmode,sym,barlist,indlist)#create_latest_state_array(btestmode,sym,barlist,indlist) need multiple rulesests
##            print currentstates
            rulesetoutput = RulesEngine.run_rulesets(sym,currentstates,now,curprice)
##            print rulesetoutput
            parse_signalsNEW(rulesetoutput)
##            RP_Snapshot.snapshot_sym(sym,date,barlist_All)
####################
    loop +=1
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
##Rules EW
##Wave 3 must never be the shortest impulsive wave.
##Wave 2 can never retrace 100% of wave 1.
##Wave 4 cant overlap wave 1.
##Guidelines
##Wave 3 is generally the longest impulse wave of the 5 wave sequence.
##Wave 4 is generally a flat to sideways choppy move that tends to correct in time as opposed to price.
##Wave 2 is generally a sharp decline or a zig zag correction.
##Fibonacci Guidelines
##Wave 3 is usually a 1.618 or 2.618 extension of wave 1
##Wave 4 generally retraces between 38.2% of wave 3 if it's a 1.618 extension or 23.6% if a 2.618 extension or in between.
##Wave 5 is usually a .618 of wave 1 or equal to wave 1.
##Wave 2 will generally retrace between 50% and 78.6% of wave 1.
##So let's take those rules and guidelines to the last chart and see how many we can tick of the list.

##stochK,reverse,8020,slopenormal,####ind,pos=buy,maxboundries,slopeup=buy
##pivot,isline,8020,slopenormal
##R,isline,8020,slopenormal
##S,isline,8020,slopenormal
##
##diffvES,normal,0,slopenormal
##RSI,reverse,8020,slopenormal
##StochK,reverse,8020,slopenormal
##Stoch_CROSS,reverse,0,slopenormal
##StochD,reverse,8020,slopenormal
##mcross,normal,0,slopenormal
##ind, dur,  midpoint value, max abs value, normal OR reverse,,,,,\
##tside [negative[lLT midpoint=BUY],normal OR reverse tside slope[slopedn = SELL],,,,,
############
