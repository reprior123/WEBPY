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
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DDarchive = DataDown +'dataarchive/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
states = sigarea + 'states/'
#######################################
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import  rpu_rp, rpInd, ibutiles, TicksUtile
from datetime import datetime
import datetime as dt
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
spaceYtime_format = " %Y-%m-%d %H:%M:%S"
time_format = "%H:%M:%S"
dateFormat = "%Y%m%d"
##############################
##import show_deflines_rpu
symlist=['ES']#, 'JPY']
for sym in symlist:
    filelist = glob.glob(DDarchive + '2*' + sym +'.*5se*both*')
    ##print filelist
    prevtimeepoch = prevdiff =0
    os.system('rm newtempf')
    for f in filelist:
        print f
        os.system('grep " 16:" ' + f + ' | tail -150000 > allticks ')
        os.system('cat allticks | grep -v " 16:0" | tail -580 > laterticks ')
##        os.system('head -1 laterticks > ltick1')
##        os.system('tail -1 laterticks >> ltick1')
##        print rpu_rp.CsvToLines('ltick1')

        
##        raw_input('ddd')
##        os.system('grep " 16:1" ' + f + ' | head -5 >> newtempf ')
##        os.system('grep " 16:2" ' + f + ' | head -5 >> newtempf ')
        bararrayin = rpu_rp.CsvToLines('allticks')
        laterticks = rpu_rp.CsvToLines('laterticks')
        for l in bararrayin:
            pass
##            print l
        print '====='
        filemode ='test'
        startmode = 'no merge'
        durinseconds = 300
        dur = '5 mins'
        today = 'bla'
        arrayout = TicksUtile.create_bars_from_bars(bararrayin,today,sym,dur,durinseconds,startmode,filemode)
    
##        os.system('grep pos  tempf | grep slopedn | tail -15 > newtempf ')
##        for item in sorted(arrayout):
##        print arrayout
        for item in arrayout:
##            print item
            if '16:05:' in str(item):
                low = float(item[4])
                high = item[3]
                date = item[1]
                sym = item[0]
##                print date,sym, high, low
        print 'xxxxx'

        # which happended first...violate the high or the low?
        tloflag =  thflag = 'open'
        for l in laterticks:
##            print '====='
            rtlow = float(l[4])
            rthigh = l[3]
            date = l[1]
            if rtlow < low and tloflag != 'tripped':
                tloflag = 'tripped'
                print 'first low under at ' , date
##                print l
                
            if rthigh > high and thflag != 'tripped':
                thflag = 'tripped'
                print 'first high over at ' , date
##                print l
                
##            print l, rtlow - low,rtlow, low, date
##            if rtlow < low:
##                print l
        





        
    ##sortedarray = array.sort
##    
##    g = rpu_rp.CsvToLines(f)
##    t = rpu_rp.head_array_to_array(g,10)
####    print t
##    print f, len(g)
##    for l in g:
##        if len(l) >2:
##            timeraw =  l[1]
##            timeepoch = int(time.mktime(time.strptime(timeraw, spaceYtime_format)))
