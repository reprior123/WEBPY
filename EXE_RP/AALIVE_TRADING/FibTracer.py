import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    if 'indlist' in var:
        print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
################
print indlist_oscils
sym = 'ES'
dur = '5mins'
date = today
threshold = 0
newindlist = ['bars']
durlist = ['5secs']#'15mins']#, '5mins','15mins']

#################################################################
def fibtrace(top,bottom,mid):
    rangeval = (float(top)-float(bottom))
    midmove = mid-bottom
    retraceperc = round((midmove/rangeval),3)
    print retraceperc
    return retraceperc
#######
def fibbo_50retrace(low,high,sym,perc) :  # could also use a time range for a range of bars / add this to states per duration
    retraceval = (high-low)/(100/perc)
    return retraceval
################
def find_hi_low(array,scanvalue,style,cvalue):
    if cvalue < scanvalue:
        slicestartvalue = cvalue -1
    else:
        slicestartvalue  = cvalue-scanvalue
    arrayslice = array[slicestartvalue:cvalue]
    oldlow = 9999
    oldhigh = -9999           
    d = 0
    while d < len(arrayslice):                       
        newlow = arrayslice[d]
        newhigh = arrayslice[d]
        if newlow < oldlow:
            oldlow = newlow
        if newhigh > oldhigh:
            oldhigh = newhigh
        d+=1 
    if style == 'lowestlow':
        final  = round(oldlow,6)
    else:
        final  = round(oldhigh,6)
    return final
##################   
fibtrace(11000,8750,9850)
