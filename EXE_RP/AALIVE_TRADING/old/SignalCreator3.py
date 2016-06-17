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
#####################
import  rpu_rp, rpInd
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
#######################################
today =  rpu_rp.todaysdateunix()  ##
yesterday ='20150609'
##############################################
##        from datetime import timedelta
from datetime import datetime
current_time = datetime.now().time()
print current_time.isoformat()
##############################
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
modedict = rpu_rp.create_dict(libbars,0,5)
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':
        barlist.append(b)
##barlist = ['15 mins','1 min', '1 hour', '5 mins']
##########################
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()  ##['GBP.USD', 'EUR.USD', 'USD.JPY', 'AUD.USD', 'NQ', 'ES']
print symbol_list
print barlist
global recentlimit
recentlimit = 90 ## <<<<<<<<<<<<<############<<<<<<<
#########################################
mode = 'livescan'
def createlines(fname):
    recentfile = fname.replace('.csv','.recent.csv')
    rpInd.prepare_tick_files(fname,fname.replace('.csv','both.csv'),recentfile)
    lines = rpu_rp.CsvToLines(fname.replace('.csv','both.csv'))
    return lines
###############################
global decimalboost
global time_format
time_format = "%H:%M:%S"
##########################################
import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############
def create_report(Sigfile,sym,barsize):
    barfile = DataDown + today + '.'+sym+ '.'+ barsize +'both.csv'
##    20150611.EUR.USD.1 hourboth
    lines = rpu_rp.CsvToLines(barfile)
    numberBars = len(lines)   
    siglines = rpu_rp.CsvToLines(Sigfile)
    numsigs = len(siglines)
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
########################
def ticks_to(lines,decimalboost,dur):
def process_ticks(lines,decimalboost,dur):
    ################
    ##read variables from the control panel file
    cpfile = EXE + 'signalcreator.controlpanel.csv'
    paramlines = rpu_rp.CsvToLines(cpfile)
    varstrings = ['TimeLimitRecentSigs','SignalsToShow','DurationToShow']
    var = {}
    for varstring in varstrings:
        for line in paramlines:
            if len(line) > 0:
                if line[0] == varstring:
                    var[varstring] = line[1]    
    bs = rpInd.strip1float(lines,5,decimalboost) ##raw close price
    bshighs = rpInd.strip1float(lines,3,decimalboost)
    bslows = rpInd.strip1float(lines,4,decimalboost)
    timestamparray = rpInd.strip1string(lines,1)
    symarray = rpInd.strip1string(lines,0)
    sym = symarray[1]
    durarray = []
    for b in symarray:
        durarray.append(dur) 
### create pivots rs and ss ###
    piv = rpInd.pivotpoint(bs,bshighs,bslows)
    R1 = rpInd.R1(piv,bshighs)
########################################
    signbs = rpInd.show_sign(bs,'price')
    slopebs = rpInd.show_slope(bs,'price')
    ##### MA Cross ##
    macrossval = rpInd.difftwoarrays(rpInd.EMAmvavgToArray(bs,9),rpInd.EMAmvavgToArray(bs,21))
    signmcd = rpInd.show_sign(macrossval,'mcd') 
    crossesmcd = rpInd.show_crossover(signmcd,'mcd')
    slopemcd = rpInd.show_slope(macrossval,'mcd')
    MDarray = rpInd.makearrayJust2(timestamparray,symarray,durarray,bs,macrossval,crossesmcd,signmcd)
    ma = rpu_rp.grep_array_to_array(MDarray,'cross')
    rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', ma)    
##############################
    from datetime import datetime
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
##        print l
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
        
        recentlimit = int(var['TimeLimitRecentSigs'])
        
        if barToNow < recentlimit and signum == numsigs:
            rpu_rp.WriteArrayToCsvfile(sigarea +'sigs.csv',ma)
            onesig = ma[len(ma)-1]
            Snaptickfile = DataDown + today + '.' + sym + '.ticksnaps.csv'
            rpu_rp.tail_to_txtfile(Snaptickfile,2,'lasttick')
            a5 = rpu_rp.CsvToLines('lasttick')
            a6= a5[0]
            bid = a6[1]
            ask = a6[3]
            bsize = a6[2]
            asize = a6[4]
            side =onesig[5]
            rside = 'BUY'
            if side == 'negcrossmcd':
                rside = 'SELL'
            sym =onesig[1]
            sigdur =onesig[2]
            pricedrift = round((sigprice / float(decimalboost)) - float(ask),4)
            timedrift = barToNow
##            print  barToPrev,'second lastsig..bid/ask',bid, ask,a6[2],'X',a6[4],
            print timedrift, pricedrift, sym, rside,sigdur, sigprice,bid,ask,bsize,asize,barToPrev
            print '=========='
##            create_report(sigarea +'sigs.csv',sym,sigdur)
## end of process ticks def   ################################################

################################            
def assemble_lines(sym,barsize,barsizeNtimeframe):
##    print sym, barsize,barsizeNtimeframe
    totalsecs = secdict[barsize]
    timebarforsnaps = barsize
    import datetime as dt
    htickfile =  DataDown+ today + '.'+sym+'.' + barsize + '.csv' #[date 5 mins.2 D.GBP.csv
    Snaptickfile = DataDown + today + '.' + sym + '.ticksnaps.csv'
    SnapBarsFname = DataDown + today + '.' + barsize + '.' + sym + '.SnapBars.csv'
    Sigfile = sigarea + sym +'.sigs.csv'
    snaplines = rpu_rp.CsvToLines(Snaptickfile)
    lline = 'ES, 2015-06-10 00:22:00, 2080.25, 2080.5, 2080.25, 2080.5, -1'
    try:
        lastline = rpu_rp.tail_to_txtfile(htickfile,2,'outfile') ## get last line of historical file for time check
        pass
    except:
        lastline = lline
    lastlineof_hticks = rpu_rp.catstring('outfile') ## this is the last line
    try:
        timeofbar = (lastlineof_hticks.split(',')[1]).split()[1]
    except:
        timeofbar ='23:59:58'
    time_of_last_hbar_dt = dt.datetime.strptime(timeofbar, time_format)
    snapbars = rpInd.create_bars(snaplines,50000,totalsecs,'fullbar','snapshot', sym,time_of_last_hbar_dt,SnapBarsFname)# also creates a file   
    rpu_rp.WriteArrayToCsvfile(DataDown+today + '.' + sym + '.'+ barsize + '.recent.csv',snapbars)
    lines = createlines(htickfile)
    decimalboost = dboostdict[sym]
    return lines
#####################
from time import sleep, strftime, localtime  
##############################
if mode == 'report':
    loopmax = 1
    pass
else:
    loopmax = 3000
loop = 0
from datetime import datetime 
while loop < loopmax:
    now = datetime.strftime(datetime.now(),time_format)
    print 'timedrift..pricedrift..sym..side..sigprice..bid.ask..bsize..asize..lastsig',now
##    print  barToPrev,'second lastsig..bid/ask',bid, ask,a6[2],'X',a6[4],timedrift, ' = timedrift' ,pricedrift, ' = pricedrift'
    for sym in symbol_list:
        rpu_rp.WriteArrayToCsvfile(sigarea +sym+'.sigs.csv', '') # flush the file to keep all sigs
        for barsize in barlist:
            timeframe = bardict[barsize]
            totalsecs = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            decimalboost = dboostdict[sym]
            lines = assemble_lines(sym,barsize,barsizeNtimeframe)
            process_ticks(lines,decimalboost,barsize)
    loop += 1
    sleep(5)
print 'finished all ',loopmax,' loops lookin for signals by Signal Creator...dead since..',
   
'''
create a report on all distances.....
##############################
1day = buy,6 bars ago, 9 positive ticks ago, starting to roll, nearing a daily pivot
124.81,13:17:22,124.8075,124.8275,124.7975,124.8125,50000,904,124.8125
ES, 2015-06-02 00:00:00, 2111.0, 2111.5, 2110.75, 2111.25, -1
'''
