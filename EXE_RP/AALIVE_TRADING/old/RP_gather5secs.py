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
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
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
archivearea = DataDown + 'dataarchive/' 
filelist = glob.glob(archivearea + '*ES*.RTticks.csv')
print filelist
prevtimeepoch = prevdiff =0

for f in filelist:
    g = rpu_rp.CsvToLines(f)
    t = rpu_rp.head_array_to_array(g,10)
    print t
    print f, len(g)

def seek_times(arrayin):
    for l in g:
        if len(l) >2:
            timerawepoch =  float(l[1].replace('time=',' '))
            timedate = datetime.fromtimestamp(float(timerawepoch)).strftime(spaceYtime_format)
            if 'close=' in str(l) and '12:1' in timedate:
                
                print timedate,l[5]


############################################################
###########
def get_size(start_path = EXEnoslash):
    total_size = 0
    allines =[]
    for dirpath, dirnames, filenames in os.walk(start_path):
##        print dirpath
        subdirsize = 0
        oneline =[]
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            subdirsize += os.path.getsize(fp)
##        print subdirsize, dirpath
        oneline.append(subdirsize)
        oneline.append(dirpath)
        allines.append(oneline)
    return sorted(allines)

##for l in get_size():
##    print l
