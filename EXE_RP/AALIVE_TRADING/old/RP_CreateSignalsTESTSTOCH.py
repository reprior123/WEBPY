# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import os.path
from datetime import datetime
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
    locals()[var] = nd[var]
####################
global recentlimit, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
today =  rpu_rp.todaysdateunix()
today ='20150914'
from datetime import datetime
import datetime as dt
import ctypes 
#######################
##timedateFormat = "%Y%m%d %H:%M:%S"
##spaceYtime_format = " %Y-%m-%d %H:%M:%S"
##############################
cpfname = EXE + 'signalcontroller.txt'

symbol_list = symdict.keys()
##symbol_list = ['ES']
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
print barlist
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
#########################3

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
loopmax = 2
loop = 0
symbol_list = ['ES']
########################
threshold = 0.0
while loop < loopmax:
    if loop == 0:
        for sym in symbol_list:
            barlist = ['1day']
            print 'here'
            for dur in barlist :            
                indlist = ['STOCH']
                print sym, dur
                rpInd.create_states_files(sym,dur.replace(' ',''),today,threshold,indlist)              
    loop +=1
####################
