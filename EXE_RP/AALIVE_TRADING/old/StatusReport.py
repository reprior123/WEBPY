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
#######################################
today =  rpu_rp.todaysdateunix()  ##today ='20150605'
##############################################
##        from datetime import timedelta
##        date_format = "%d-%m-%Y"
from datetime import datetime
current_time = datetime.now().time()
print current_time.isoformat()
##############################
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
barlist = bardict.keys()  ##
barlist = ['15 mins', '15 secs', '1 min', '1 hour', '5 mins']
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
loopmax = 400 ##<<<<<<<<<<<<<
recentlimit = 60
###############################
def createlines(fname):
    recentfile = fname.replace('.csv','.recent.csv')
    rpInd.prepare_tick_files(fname,fname.replace('.csv','both.csv'),recentfile)
    lines = rpu_rp.CsvToLines(fname.replace('.csv','both.csv'))
    return lines
###############################
global decimalboost
##########################################
import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
########################
rpu_rp.WriteArrayToCsvfileAppend(sym+'.sigs.csv', ma) 

from time import sleep, strftime, localtime  
##############################
time_format = "%H:%M:%S"
import datetime as dt
from datetime import datetime
current_time = datetime.now()
current_time_dt = dt.datetime.strptime(current_time, time_format)
print current_time
prevt = 0
numsigs = len(ma)
signum =0
for symbol in symbol_list:
    for tf in barlist:
        bardur = bardict[tf]
        totalsecs = secdict[tf]
        dur = bardur + tf
        htickfile =  DataDown+ today + '.'+symbol+'.' + dur + '.csv') #[date 5 mins.2 D.GBP.csv
        Snaptickfile = DataDown + today + '.' + symbol + '.ticksnaps.csv'
        SnapBarsFname = DataDown + today + '.' +dur + '.' + symbol + '.SnapBars.csv'
        Sigfile = symbol+'.sigs.csv'
        snaplines = rpu_rp.CsvToLines(DataDown + today + '.' + sym + '.ticksnaps.csv')
##########
        lastline = rpu_rp.tail_to_txtfile(htickfile,2,'outfile') ## get last line of historical file for time check
        lastlineof_hticks = rpu_rp.catstring('outfile') ## this is the last line
        try:
            timeofbar = (lastlineof_hticks.split(',')[1]).split()[1]
        except:
            timeofbar ='23:59:58'
        time_of_last_hbar_dt = dt.datetime.strptime(timeofbar, time_format)
        snapbars = rpInd.create_bars(ticklines,50000,timebarforsnaps,'fullbar','snapshot', sym,time_of_last_hbar_dt,SnapBarsFname)# also creates a file   
        rpu_rp.WriteArrayToCsvfile(DataDown+today + '.' + sym + '.'+ dur + '.recent.csv',newbars)
        lines = createlines(htickfile)
        decimalboost = dboostdict[sym]
        create_report(sigfile,lines,decimalboost,tf)

'''
create a report on all distances.....
##############################
1day = buy,6 bars ago, 9 positive ticks ago, starting to roll, nearing a daily pivot
124.81,13:17:22,124.8075,124.8275,124.7975,124.8125,50000,904,124.8125
ES, 2015-06-02 00:00:00, 2111.0, 2111.5, 2110.75, 2111.25, -1

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
Mbox('Your title', 'Your text', 1)

'''
