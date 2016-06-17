import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
#########################################
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
##    print var
    locals()[var] = nd[var]
####################
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
import ctypes 
print 'entry copier'
####################
cpfname = EXE + 'entrycontroller.txt'
##############################
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
slibarea = sigarea + 'orderlib/'
print slibarea
sym = 'FDAX'
side = 'SELL'
sellfile = slibarea  +'nodate.recentsigsexecHARD.' + side + '.' +sym+'.csv'
siglistfile = sigarea + today +'.recentsigsexecHARD.csv'
shutil.copy(sellfile,siglistfile)
######
######    if os.path.isfile(siglistfile):
######        recentsigs =  rpu_rp.CsvToLines(siglistfile)
######        print recentsigs
######        sigfileage = check_for_CP_change(siglistfile)
######        if sigfileage < (cycledelay + agelimit) :
########            rpu_rp.beep(soundarea + 'OrderFilled')
######            pass
#############
