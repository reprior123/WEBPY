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
    if module != titleself:
        my_module = importlib.import_module(module.strip())
######################
##############################
symbol_list = symdict.keys()
##symbol_list =['ES','EUR.USD']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
##########################################
prevcycledelay = 2
########################
##print 'currrent stateNage  | lastcrosstime | '
def make_dur_state(sym,dur,threshold,indlist):
##    print sym,dur
    rpInd.create_states_filesWboost(sym,dur,today,threshold,indlist)
    for ind in indlist:
        mode = 'boost'
        state = rpInd.ShowRecentState(sym,dur,ind,mode)
        stateAge = rpInd.ShowRecentAge(sym,dur,ind,mode)
        val = rpInd.ShowRecentStateValue(sym,dur,ind,mode)
        crxtime = rpInd.ShowRecentCRXTime(sym,dur,ind,mode)
        price = rpInd.ShowRecentClPrice(sym,dur,ind,mode)
        
        print  state, stateAge,val,ind, crxtime,price , sym, dur, threshold
##############################
def snapshot_sym(sym,today,durslist):
##    print 'got her'
    text = []
    barlist = ['1min', '3mins', '5mins', '15mins', '1hour']
    basisfile = DataDown +today+'.'+sym+'.'+'5secs'+'.both.csv'
    TicksUtile.assemble_dur_bars(today,sym,'1hour','initial',basisfile)
    posstate = rpInd.ShowRecentPositionState(sym)
    text.append(posstate + sym )
    threshold =0.0
    indlist = ['mcross','kupper']
##    print posstate,sym,'recentstate age val | lastcrosstime| name USING THRESH ', threshold
    textline = 'recentstate age val name USING THRESH ' + str(threshold)
    text.append(textline)
    for dur in barlist :
##        print dur
        threshold = 0.0
        if dur == '1min':
            threshold = 0.1
##        print sym,dur
##        make_dur_state(sym,dur,threshold,indlist)
        basisdur = '5secs'
        startmode ='initialize'
        basisfile = DataDown +today+'.'+sym+'.'+basisdur+'.both.csv'
        TicksUtile.assemble_dur_bars(today,sym,dur,startmode,basisfile)
### this relys on the sig creator to assemble each time
        rpInd.create_states_files(sym,dur,today,threshold,indlist)
        indlist = ['mcross']
        for ind in indlist:
            mode = 'noboost'     
            state = rpInd.ShowRecentState(sym,dur,ind,mode)
            stateAge = rpInd.ShowRecentAge(sym,dur,ind,mode)
            val = rpInd.ShowRecentStateValue(sym,dur,ind,mode)
            crxtime = rpInd.ShowRecentCRXTime(sym,dur,ind,mode)
            price = rpInd.ShowRecentClPrice(sym,dur,ind,mode)
            if ind == 'mcross':
                textline = []
                tlist = [state, dur, stateAge,val, price, crxtime, threshold, sym, ind]
                for t in tlist:       
                    textline.append(str(t))
                text.append(str(textline))

                print  state, dur, stateAge,val, price, crxtime, threshold, sym, ind
##        Triggers = rpInd.Trigger_from_states(sym,dur,'kupper')
##        lasttwo = rpu_rp.tail_array_to_array(Triggers,2)
##        for l in lasttwo:
##            print l[0],l[1],l[7],l[5],l[8],l[11],'kupperflips'
    print recenttick(sym)
    print '======================='
    return text
###########################
def show_one_bar(sym,dur,bartime,date):
    stem = '.'+dur +'.both.csv'
    datehyphen = rpu_rp.todaysdatehypens(date)
    if dur == 'RTicks':
        stem = '.RTticks.csv'
    barfile =  DataDown + date + '.' + sym + stem
    bars = rpu_rp.CsvToLines(barfile)
    lines = rpu_rp.grep_array_to_array(bars,datehyphen +bartime)
    l=[]
##    for l in lines:
##        print l
    return l
####################
##['ES', ' 2015-09-03 16:05:05', '1958.75', '1962.5', '1958.25', '1962.0', 'full', '300'] is bar
##['ES', ' 2015-09-03 16:10:05', '1962.0', '1962.5', '1960.75', '1961.25', 'partial', '135'] 
###########################
def show_bar_range(sym,dur,startbartime,endbartime,date):
    datehyphen = rpu_rp.todaysdatehypens(date)
    startbartime = TicksUtile.time_to_epoch(datehyphen + startbartime)
    endbartime = TicksUtile.time_to_epoch(datehyphen + endbartime)
    stem = '.'+dur +'.both.csv'
    if dur == 'RTicks':
        stem = '.RTticks.csv'
    barfile =  DataDown + date + '.' + sym + stem
    bars = rpu_rp.CsvToLines(barfile)
    newbars =[]
    for bar in bars:
        if len(bar) > 2:
##            print bar,'is bar'
            curbartime = TicksUtile.time_to_epoch(bar[1])
            if curbartime > startbartime and curbartime < endbartime:
                newbars.append(bar)
##    for b in newbars:
##        print b
    return newbars
####################
def show_hi_lo_bar_range(sym,dur,startbartime,endbartime,date):
    hilow = []
    prevloprice =99999
    prevhiprice = 0.0
    lowtime = hitime = closetime ='na'
    clsprice =0.0

    newbars = show_bar_range(sym,dur,startbartime,endbartime,date)
    for bar in newbars:
        if len(bar) > 2:
            curbartime = TicksUtile.time_to_epoch(bar[1])
            lowprice = float(bar[4])
            hiprice = float(bar[3])
            clsprice = float(bar[5])
            closetime = bar[1]
            lowtime = hitime ='na'
            if lowprice < prevloprice:
                prevloprice = lowprice
                lowtime = bar[1]
            if hiprice > prevhiprice:
                prevhiprice = hiprice
                hitime = bar[1]
    hilow.append(prevloprice)
    hilow.append(prevhiprice)
    hilow.append(lowtime)
    hilow.append(hitime)
    hilow.append(clsprice)
    hilow.append(closetime)
    if len(newbars) == 0:
        hilow = ['na','na','na','na','na','na']
    return hilow
####################
##show_one_bar('ES','1min','btime')
def create_report(Sigfile,sym,barsize):
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
    print 'if i am 20 bars old in signal, start with trail stop depends on dur...shotrt dur = short age'
##    average number of sigs in 30 bars  has it flipped alot
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#################
    
'''
if we have a position then use the 1 min cross
if no position, use the 3 or 5 min
if fast market, strong trend [value on 1 min is > 2 or x bars strength]
then use the 1 min on the switch, it is prob sgnificant

look for the lines and identify first pass so as to fade

identify upper K to see if good in the range for a sell...
probably will not be if the 1 min has just swung

'''
