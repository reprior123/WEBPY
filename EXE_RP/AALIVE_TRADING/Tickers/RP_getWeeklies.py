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
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################
from time import sleep
import  rpu_rp, rpInd, TicksUtile

import ctypes 
##############################
symbol_list = symdict.keys()
##symbol_list =['ES','EUR.USD']
barlistall = bardict.keys()  ##
barlist =[]
barlist = ['1 Week']
##########################################
date =  rpu_rp.todaysdateunix()
date = '20150905'
datehyphen = rpu_rp.todaysdatehypens(date)
##########################
import RP_Snapshot
sym = 'SPX'
##RP_Snapshot.snapshot_sym(sym,date)
basisdur = '1day'
TicksUtile.assemble_dur_bars(date,sym,'1day','initialize','5secs')
TicksUtile.assemble_bars_1min_basis(date,sym,'1Week','bartobar',basisdur)
indlist = ['mcross','pivot','R','R2','S','S2']
threshold = 0.0
rpInd.create_states_files(sym,'1Week',date,threshold,indlist)
rpInd.create_states_files(sym,'1day',date,threshold,indlist)

'''
def fibbo_50retrace(low,high,sym,perc) :  # could also use a time range for a range of bars / add this to states per duration
    retraceval = (high-low)/(100/perc)
    return retraceval

def check_lines(linesfile,curprice,tolerance):
    for l in linesfile:
        diff = curprice - l[0]
        if diff < tolerance:
            lines.append(l[0])
            pass
        pass
    return lines
###################
if line detected, give audio

def show_spots(sym,date,curprice):
    print symlinedict
    pass
    
    filein = DataDown + today + '.' + sym + '.5mins.both.csv'
    lines = rpu_rp.CsvToLines(filein)
##    oneline = grep '16:05:00' filein
    onelinearray = rpu_rp.grep_array_to_array(lines,'16:05:00')
    print onelinearray
#####################3
    pivot = rpInd.gatherline(sym,'pivot')
    R1 = rpInd.gatherline(sym,'R1')
    S1 = rpInd.gatherline(sym,'S1')
    ##do the same for weekly by adding dur to variables and create a weekly  from dailys..
##    find pivots, find fibbo retraces on recnt moves[rangebars,hi,lo]
##    read spots from file
##    calculate two roundies
##    calculate 10 handles off high of day,lowday,openday,yestclose,prevhourhilow
#############################################

def detect_sliceDice(lineprice,start,end):
    grab_range(start,end)
    startprice = float(head(bars)[6])
    if startprice <  lineprice :
        position = 'below'
        pass
    else:
        position = 'above'
        pass
    sflag = 'untagged'
    for bar in bars:
        currprice = bar[6]
        if position == 'below':
            if currprice > lineprice:
                sflag='firsttag'
                pass
            if sflag == 'firsttag':               
        
detect_sliceDice(lineprice,start,end)
first pass did not bounce 4 ticks, went 6 ticks [noise] beyond before bounce or retag
bar low v kupper, barhi vs klower, barage, older the worse? what is max?
##########raw_input('click')

####thrust and slope of current bar
## averages of:
# of sigs per period
# average distance between

is it a cross or a bounce....one touch and threw...1st pass, 2nd pass, thru
identify wedges...50/50 chance

stop distances...3x for bigger moves
grab trade data from action forex
use action forex for wide lines 4hour

def create_report(Sigfile,sym,barsize):
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
    print 'if i am 20 bars old in signal, start with trail stop depends on dur...shotrt dur = short age'
##    average number of sigs in 30 bars  has it flipped alot
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#################
  
'''
