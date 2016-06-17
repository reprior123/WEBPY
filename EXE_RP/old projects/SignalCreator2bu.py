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
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
symdict = rpu_rp.create_dict(libsyms,0,1)
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday':
        barlist.append(b)
##barlist = ['15 mins','1 min', '1 hour', '5 mins']
##########################
symbol_list = rpsymdict.keys()  ##['GBP.USD', 'EUR.USD', 'USD.JPY', 'AUD.USD', 'NQ', 'ES']
print symbol_list
print barlist
global recentlimit
#########################################
mode = 'livescan'
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
from time import sleep, strftime, localtime
from datetime import datetime
##############################
mode = 'loop'
if mode == 'report':
    loopmax = 1
    pass
else:
    loopmax = 3000
    
loop = 0
########################################
##read variables from the control panel file
cpfile = TMP + 'signalcontroller.txt'
paramlines = rpu_rp.CsvToLines(cpfile)
varstrings = ['TimeLimitRecentSigs','SignalsToShow','DurationToShow']
var = {}
for varstring in varstrings:
    for line in paramlines:
        if len(line) > 0:
            if line[0] == varstring:
                var[varstring] = line[1]
###########################################               
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
            htickfile = (rpInd.snapticks_to_snapbarsfile(sym,barsize,barsizeNtimeframe))[0]
            lines = rpInd.createlines(htickfile)
            ma = rpInd.process_ticks(lines,decimalboost,barsize)
            rpu_rp.WriteArrayToCsvfileAppend(sigarea +sym+'.sigs.csv', ma)    
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
##                print l
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
                if barToNow < recentlimit:
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea +today +'.sigs.csv',ma)
                    onesig = ma[len(ma)-1]
                    need to add here one sig added to full list, full list of this sym dur sent to file as a whole....
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
    loop += 1
    sleep(5)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
