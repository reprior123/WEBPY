################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
#############################
print symlistTicker
########################################
symTickerIddict ={}
contractdict ={}
symid=0
for sym in symlistTicker:
    linesleft = 4010
    fname1 = DataDown+ today + '.' + sym  +'.RTMktDepth.csv'
    fname3 = DataDown+ today + '.' + sym  +'.RTtickData.csv'
    fname2 = DataDown+ today + '.' + sym  +'.RTticks.csv' 
    fname4 = DataDown+ today + '.' + sym  +'.5secs.recent.csv' 
    TicksUtile.trimFile(fname1,linesleft)
    TicksUtile.trimFile(fname3,linesleft)
    linesleft = 8010
    TicksUtile.trimFile(fname4,linesleft)
    symid+=1
##rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTticks',[])
##rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTtickDOMs',[])
#################
