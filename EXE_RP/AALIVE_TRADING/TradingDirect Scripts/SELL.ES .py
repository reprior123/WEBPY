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
################
slibarea = sigarea # + 'orderlib/'
print slibarea
print today
sym = 'ES'
##sym = 'FDAX'
side = 'SELL'
sellfile = slibarea  +'nodate.recentsigsexecHARD.'+side+'.' + sym + '.csv'
##sellfile = slibarea  +'nodate.recentsigsexecHARD.BUY.ES.csv'
siglistfile = sigarea + today +'.recentsigsexecHARD.csv'
shutil.copy(sellfile,siglistfile)

