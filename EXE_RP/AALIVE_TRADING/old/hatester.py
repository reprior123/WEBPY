import os, sys
path = os.getcwd() + '/'
EXEnoslash = ((path.replace('\\AALIVE_TRADING','|')).split('|'))[0]
rootpath = ((path.replace('EXE','|')).split('|'))[0]
sys.path[0:0] = EXEnoslash
localtag = ((EXEnoslash.replace('EXE','|')).split('|'))[1] #'_RP'
print localtag,'is local'
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
##    print var, nd[var]
    locals()[var] = nd[var]
##################
global recentlimit, time_format,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile,RulesEngine, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
import ctypes
global date
date =   today  ######## <<<<<<<
filen = DataDown +date +'.ES.5mins.both.HA.csv'
teststr = 'grnNnotailNbigbar' #'2016-02-19 21:'
closestr = 'grnNnotailN'
pos = netcost = 0
'''
add 5 bar moving average, vwap study, breakpoints assembler option
'''
def showlines(filen,buysell):
    lines = rpu_rp.CsvToLines(filen)
    newlines = []
    pnlsign = 1
    
    if buysell == 'sell':
        teststr = 'redNnotailNbigbar' #'2016-02-19 21:'
        closestr = 'redNnotailN'
        pnlsign = (-1)
        pass
    elif buysell == 'buy':
        teststr = 'grnNnotailNbigbar' #'2016-02-19 21:'
        closestr = 'grnNnotailN'
        pass
    else:
        teststr = 't'
        closestr = 'xxxxx'
    pos =  netcost = 0
    for l in lines:
        markprice = float(l[5])
        tdate = str(l[1])
        if teststr in str(l):  #if red signal sell one until..
            pos +=1
            netcost += (1 * markprice)
            avgcost = netcost / pos
            oneline = str(pos)+ ' | ' + str(netcost)+ ' | ' +  str(avgcost)+ ' | ' + tdate
            if buysell == 'all':
                newlines.append(l)
                pass
            else:
                newlines.append(oneline)
    ##        print l
        if closestr not in str(l):
            pnl = (netcost - (markprice * pos) )*pnlsign
            if pos != 0 :
                oneline =  str(pnl)+ ' | ' + str(markprice)+ ' | ' + 'closing'+ ' | ' + tdate
                newlines.append(oneline)
            netcost = 0
            pos = 0
    return newlines
#################
'''
b = showlines(filen,'buy')
print 'BUYS'
lenha = len(b)
c=0
climit = int(lenha * .8)
for lha in b:
    c+=1
    if c > climit:
        print lha
        #######
b = showlines(filen,'sell')
print 'SELLS'
lenha = len(b)
c=0
climit = int(lenha * .8)
for lha in b:
    c+=1
    if c > climit:
        print lha
########
b = showlines(filen,'all')
print 'all'
lenha = len(b)
c=0
climit = int(lenha * .8)
for lha in b:
    c+=1
    if c > climit:
        print lha

['ES', ' 2016-02-19 22:05:00', '1913.75', '1914.5', '1913.75', '1914.0', '8603.0', 'full', '300', '0.25', '0.5', '0.0', 'grnNnotailNshortbar']
['ES', ' 2016-02-19 22:10:00', '1914.0', '1915.0', '1914.0', '1914.25', '13845.0', 'full', '300', '0.25', '0.75', '0.0', 'grnNnotailNshortbar']
['ES', ' 2016-02-19 22:30:00', '1914.25', '1914.25', '1913.75', '1914.0', '471.0', 'full', '960', '-0.25', '0.0', '-0.25', 'redNnotailNshortbar']
'''
