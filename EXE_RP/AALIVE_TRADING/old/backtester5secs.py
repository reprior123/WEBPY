# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import os.path
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
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
statearea = DataDown + 'Signals/states/'
DataDownNoSlash = 'C:/TS/TSIBData'
soundarea = path + 'sounds/'
#######################################
global recentlimit, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
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
libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)
libsymNEWS = EXE + 'library.symNEWSTIMES.csv'
symNEWSdict = rpu_rp.create_dict(libsymlines,0,2)
symbol_list = symdict.keys()
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if b == '5 mins':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
print barlist
##################
prevsigid = ''
today =  rpu_rp.todaysdateunix()
today ='20150818'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
def recenttick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickvalue = float(tickvaluedict[sym])
    if os.path.isfile(RecentTickFile) :
        tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
        for f in tickline:
            if 'close' in str(f):                        
                lasttick = rounderrp(float(f.split('=')[1]),tickvalue)
    else:
        lasttick =1
    return lasttick
#################
def pnl(tside,tprice,starttime,sym,exitpnl,stoppnl,tickvalue):   
    dur = '1min'
    estarttime = TicksUtile.time_to_epoch(starttime)
    barcount =0
    sidesign = 1
    if tside == 'BUY':
        sidesign = (-1)
    DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
    triggertime = 'open'
    maxpnl = -99999
    minpnl = 999999
    profittrigger =  stoptrigger = endflag ='o'
    for line in DurBoth:
        if len(line) > 2:
            rtpricelow = float(line[4])
            rtpricehigh = float(line[3])
            rangegap = rtpricehigh - rtpricelow
            time = line[1]
            baretime = TicksUtile.time_to_epoch(time)
##        else:
##            rtpricelow = rtpricehigh = 0.0
##            baretime = TicksUtile.time_to_epoch(' 2015-08-18 01:54:05')
##            time = ' 2015-08-18 01:54:05'
##            print estarttime, baretime
            if estarttime  > baretime:
                triggertime = 'tripped'
                barcount =0
            
            if triggertime == 'tripped':
                barcount +=1
                if tside == 'BUY':
                    priceused = rtpricelow
                else:
                    priceused = rtpricehigh
                pnl = ((tprice -priceused)/ tickvalue)*sidesign
                maxpnl = max(pnl,maxpnl)
                minpnl = min(pnl,minpnl)
                if maxpnl > exitpnl:
                    profittrigger = 't'
                    pass
                if minpnl < stoppnl:
                    stoptrigger ='t'
                if profittrigger == 't' and stoptrigger == 'o' and endflag != 't':
                    print 'exited for profit'
                    print sym, time, tprice, tside, pnl,maxpnl,minpnl,priceused,rangegap,barcount,starttime
                    endflag ='t'
                if stoptrigger == 't' and profittrigger == 'o' and endflag != 't':
                    print 'exited for loss'
                    endflag ='t'
                    print sym, time, tprice, tside, pnl,maxpnl,minpnl,priceused,rangegap,barcount,starttime
##                print sym, time, tprice, tside, pnl,maxpnl,minpnl,priceused,rangegap,barcount,starttime

    ####################
##USD.JPY,2,SELL,50000,LIM,124.38,0.0,USD.JPYnegcrxx3minsmcross, 2015-08-18 21:12:05,0.01, 2015-08-18 21:15:37
##CL,3,SELL,1,LIM,42.4,0.0,CLnegcrxx5minsmcross, 2015-08-18 21:15:05,0.01, 2015-08-18 21:17:48
##USD.JPY,2,SELL,50000,LIM,124.37,0.0,USD.JPYnegcrxx5minsmcross, 2015-08-18 21:20:05,0.01, 2015-08-18 21:22:10
    ## read the signal time and side and price from file and then run btest
sigfile= sigarea +'20150818.recentsigs.csv'
blalist = rpu_rp.CsvToLines(sigfile)
for bla in blalist:
    print bla
    sym = bla[0]
    ttime = bla[8]
    tside = bla[2]
    tprice = float(bla[5])
    tick = float(tickvaluedict[sym])
    print tick,ttime
    ##    pnl(tside,tprice,starttime,sym)
    exitpnl= 3.0
    stoppnl = -6.0
    pnl(tside,tprice,ttime,sym,exitpnl,stoppnl,tick)
    ##pnl('SELL',2098.0,' 2015-08-18 16:45:05',sym,exitpnl,stoppnl)
