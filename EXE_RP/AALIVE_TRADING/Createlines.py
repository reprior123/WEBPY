################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open('importmodlist.txt').readlines()
for module in moduleNames:
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
import Mod_rpInd
style = ''
now = datetime.strftime(datetime.now(),spaceYtime_format)
current_time = datetime.now().time()
#######################
btmode = 'BACKTEST22222'
#########################
prevsigid = ''
##########################################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
def make_bars_no_5sec(date,startmode,symbol_list,barlist,hamode):  ## add modes no5sec,dayonly,just5sec
    for sym in symbol_list:
        for dur in ['1min'] : #barlist :
            if dur == '1min':
                basisdur = '5secs'
            else:
                basisdur  = '1min'
            Mod_TicksUtile.assemble_dur_bars(date,sym,dur,startmode,basisdur,hamode)
#################
def make_bars_dayonly(date,startmode,symbol_list,barlist):
    for sym in symbol_list:
        Mod_TicksUtile.assemble_dur_bars(date,sym,dur,startmode,basisdur)
#################
def make_bars_just_5sec(date,startmode,symbol_list):
    for sym in symbol_list:
        Mod_TicksUtile.prepare_tickfilesto5secBars(date,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
##################
def make_states(date,symbol_list,barlist,indlist):
    threshold = 0.0
    for sym in symbol_list:
        for dur in barlist :
            Mod_rpInd.create_states_files(sym,dur,date,threshold,indlist)
#################
def create_latest_state_array(btestmode,sym,barlist,indlist):
##    indlist = partindlist
    currentstates =[]
    for bar in barlist:
        dur = bar
        for ind in indlist:
##            print bar,ind,'creating latest statearrays'
            lastbar = Mod_rpInd.ShowIndBar(sym,dur,ind,'LastBar',1,1)
            currentstates.append(lastbar)
    return currentstates
#####################
def create_previous_state_array(btestmode,sym,barnum,backtestdur):
    durlist = barlist_Recent
    currentstates =[]
    last1minbar = Mod_rpInd.ShowABarofInd(sym,backtestdur,'mcross',barnum) ## was 1min ### this controls the backtester!!
    timeofbar = last1minbar[0]
    for dur in durlist:
        for ind in indlist:
            lastbar = Mod_rpInd.ShowIndBar(sym,dur,ind,'ByTime',1,timeofbar) #ShowABarofIndByTime(sym,dur,ind,timeofbar,barnum)
            currentstates.append(lastbar)
    return currentstates,timeofbar
##############################        
######def create_HAs(symbol_listin,date):
######    loopmax = 1
######    loop = 0
######    delaydupetime = 200
######    recentlimit = 5000000  # int(read_vars('TimeLimitRecentSigs',cpfname))
######    cycledelay = 4 #int(read_vars('CycleTime',cpfname))
######    prevcycledelay = 2
######    threshold = 0.0
######    now = datetime.strftime(datetime.now(),spaceYtime_format)
######    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))
######    if loop == 0 :
######        indlist = indlist_All
######        startmode = 'initialize'
######        if btmode != 'BACKTEST':
######            make_bars_just_5sec(date,startmode,symbol_listin)
######            barlist = ['1min', '3mins', '5mins','15mins', '1hour','1day']
######            make_bars_no_5sec(date,startmode,symbol_listin,barlist_All,'normal') #need this to creat both
########            make_bars_no_5sec(date,startmode,symbol_listin,barlist_All,'hamode')
######            print 'made bars'          
####################
def make_both_states(symbol_listin,date):
    make_states(date,['ES'],barlist_All,indlist_All) #make_states('fullist',date,['ES'])
    make_states(date,symbol_listin,barlist_All,indlist_All) #make_states('fullist',date,symbol_list)
    print 'made states'
