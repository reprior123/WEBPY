################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
#######################
date =  today #'20160219' #yesterday # today  ######## <<<<<<<
style = ''
now = datetime.strftime(datetime.now(),spaceYtime_format)
current_time = datetime.now().time()
#######################
btmode = 'BACKTEST22222'
if  btmode == 'BACKTEST':
    date = '20160133' #yesterday #'20151133' #yesterday
#########################
cpfname = EXE + 'signalcontroller.txt'
symbol_list = ['ES', 'FDAX'] #symbol_list2
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
#################################
def show_spots(sym,date,limit,spotfile):
    curprice = float(TicksUtile.recenttick(sym,'recent'))
    spotlines= rpu_rp.CsvToLines(spotfile)
    print 'LINEFADES...################'
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
            if underover == 'under':
                sflag = 'SELL'
            else:
                sflag = 'BUY'
            print ('>>%4s at %8.2f %s|%s |%4.2f |%8.2f > pass#? range=%d' % (sflag,spotp,spotid,sym,distance,curprice,limit))
#####################
def make_bars_no_5sec(date,startmode,symbol_list,barlist,hamode):
    for sym in symbol_list:
        for dur in barlist :
            if dur == '1min':
                basisdur = '5secs'
            else:
                basisdur  = '1min'
            TicksUtile.assemble_dur_bars(date,sym,dur,startmode,basisdur,hamode)
##            print 'creating bars',dur,basisdur,sym
#################
def make_bars_dayonly(date,startmode,symbol_list,barlist):
    for sym in symbol_list:
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

##############################
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
cycledelay = 4 #int(read_vars('CycleTime',cpfname))
print 'Signals within the last ',recentlimit, 'Seconds will be ignored'
prevcycledelay = 2
threshold = 0.0
print barlist_All, ' is barlist all'
print symbol_list, 'is symlist'
backtestdur = '5mins' #'1hour' #'1min'   #### <<<<<<
btestlimit = rpInd.ShowBarCountofInd(symbol_list[0],backtestdur,'mcross')   ### 1000
print btestlimit,'testlimit...'
btestTag = 'btestrun_'+date+backtestdur
ranswer =  raw_input('rules? ')
##import hatester
########################
while loop < loopmax:
##    print "\n" * 50
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))
    if loop == 0 :
        indlist = indlist_All
        startmode = 'initialize'
        if btmode != 'BACKTEST':
            make_bars_just_5sec(date,startmode,symbol_list)  ## make_bars_just_5sec(date,startmode,symbol_list):
##        canswer =  'y' # raw_input('createnewstates? ')
##        if canswer == 'y':
            make_bars_no_5sec(date,startmode,symbol_list,barlist_All,'normal') #def make_bars_no_5sec(date,startmode,symbol_list,barlist)
            make_states(date,['ES'],barlist_All,indlist_All) #make_states('fullist',date,['ES'])
            make_states(date,symbol_list,barlist_All,indlist_All) #make_states('fullist',date,symbol_list)

        tanswer = 'n' # raw_input('createtable? ')
##        problem !!!!! you have already read this table in envdicts
        if tanswer == 'y':
            tablelist = indlist_All
            tabledurlist = barlist_All
            rpInd.CreateIndvalueTable(tablelist,tabledurlist,['ES','FDAX','CL'],libarea +'indlevels.csv')
            
        indlistnew = ['pivot'] #indlist_lines2
        for indline in indlistnew:
            lineval = rpInd.ShowLastBarofInd('ES','1day',indline)[1]
            print lineval,indline
            rpu_rp.WriteArrayToCsvfile(libarea +'ES.daily.spotlines2.csv', [['1','']])            
            rpu_rp.WriteArrayToCsvfileAppend(libarea +'ES.daily.spotlines2.csv', [[lineval,indline]])

##        ask which statesarea lable to use by glob.glob(states area labels...choose one or default to main
##                =================
    ### here ends the first loop tasks ###
            ##################
            ###############
            ##########
    factor = 1
    
    
    daxcurprice = float(TicksUtile.recenttick('FDAX','recent'))
    escurprice = float(TicksUtile.recenttick('ES','recent'))
    sym = 'ES'
    limitlines = 5.0
    print '###### LINEFADES #### ',curprice ,sym
    spotfiles = ['Full.','WBDaily.','Roundies.','AutoPivot.']
    for tag in spotfiles:
        spotfile = libarea + 'Spots' +tag + sym+'.txt'           
        show_spots(sym,date,limitlines,spotfile)    
    sym = 'FDAX'
    limitlines = 15.0

    print '###### LINEFADES #### ',curprice ,sym
    spotfiles = ['Full.','WBDaily.','Roundies.','AutoPivot.']
    for tag in spotfiles:
        spotfile = libarea + 'Spots' +tag + sym+'.txt'           
        show_spots(sym,date,limitlines,spotfile)
               
    if float(float(loop)/factor) == round((loop/factor),1):
        print 'cycle ', loop, escurprice,daxcurprice

#### symd = 'FDAX'      limitlinesd = 10.0    show_spots(symd,date,limitlinesd)
#####################
    if btmode != 'BACKTEST':
        make_bars_just_5sec(date,startmode,symbol_list)
        barlist = ['1min', '3mins', '5mins','15mins', '1hour']
        make_bars_no_5sec(date,startmode,symbol_list,barlist_All,'normal')
##        make_bars_no_5sec(date,startmode,symbol_list,barlist_All,'hamode')
        print 'made bars'
####        startmode = 'bartobar' barlist = barlist_78  make_bars_no_5sec(date,startmode,symbol_list,barlist)
        make_states(date,symbol_list,barlist_All,indlist_All)  #def make_states(date,symbol_list,barlist,indlist):
    ############################  end of bar creation, now run rules....
    for sym in symbol_list:
        curprice = float(TicksUtile.recenttick(sym,'recent')) * float((dboostdict[sym]))
        if btmode == 'BACKTEST':
            lbarnum = btestlimit # use this for testing short runs...full limit for real runs
            while lbarnum > 1:
                lbarnum -=1
####                if it is backtest, swap out the STATES folder with the premade one to save time
                currentstates = create_previous_state_array(btmode,sym,lbarnum,backtestdur)[0]
                timeloop =      create_previous_state_array(btmode,sym,lbarnum,backtestdur)[1]
                print timeloop,lbarnum, sym
                rulesetoutput = RulesEngine.run_rulesets(sym,currentstates,now,curprice)
##                print rulesetoutput
                RulesEngine.parse_signalsNEW(rulesetoutput,btmode,date)

        else:  ## if not backtest, just take the most recent line and ruletest
            filen = DataDown +date +'.' + sym + '.5mins.both.HA.csv'
##            barlist = barlist_All
##            indlist = indlist_All  #['mcross','AO','AOAcc'] #indlist_All  beware this needs to open up for more rules
            if ranswer == 'y':
                currentstates = create_latest_state_array(btmode,sym,barlist_All,indlist_All)#create_latest_state_array(btestmode,sym,barlist,indlist) need multiple rulesests
                rulesetoutput = RulesEngine.run_rulesets(sym,currentstates,now,curprice)
                RulesEngine.parse_signalsNEW(rulesetoutput,btmode,date)           
##            RP_Snapshot.snapshot_sym(sym,date,barlist_All)
####################
    loop +=1
    sleep(cycledelay)
    ##            copy the states directory and save with testlabel
    if btmode == 'BACKTEST':
        btestsavedir = AS + 'BACKTESTS/' +btestTag +'/'
        ruleslocal = RulesArea
        stateslocal = statearea
        sigfilelocal = sigarea + date +'.recentsigs.csv'
        indfilelocal = libarea + 'indlevels.csv'
        shutil.copytree(stateslocal,btestsavedir+'statesnew')
        shutil.copytree(ruleslocal,btestsavedir+'rulessnew')
        shutil.copy(indfilelocal,btestsavedir+'indfile.csv')
        shutil.copy(sigfilelocal,btestsavedir+'sigfile.csv')
##            copy the rules directory and save with testlabel
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
