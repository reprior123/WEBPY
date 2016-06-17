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
date = today
def create_dailypivots(sym):
    pivot = round(float(rpInd.gatherline(sym,'pivot')[1]),1)
    R1 = round(float(rpInd.gatherline(sym,'R1')[1]),1)
    S1 = round(float(rpInd.gatherline(sym,'S1')[1]),1)
    S2 = round(float(rpInd.gatherline(sym,'S2')[1]),1)
    R2 = round(float(rpInd.gatherline(sym,'R2')[1]),1)
##    print S1,R1,pivot
    ##do the same for weekly by adding dur to variables and create a weekly  from dailys..
##    find pivots, find fibbo retraces on recnt moves[rangebars,hi,lo]
##    calculate 10 handles off high of day,lowday,openday,yestclose,prevhourhilow
    outfile = libarea +'spotlinesAutopivot.' + sym +'.csv'
    itemlist = [pivot,R1,S1,S2,R2]
    itemlisttags = ['pivotRP','R1rp','S1rp','S2rp','R2rp']
    lines=[]
    c=0
    for item in itemlist:
        tag = itemlisttags[c]
        c+=1
        line=[]
        line.append(item)
        line.append(tag)
        lines.append(line)      
    for line in lines:
        print line
    rpu_rp.WriteArrayToCsvfile(outfile,lines)
##############
create_dailypivots('ES')
create_dailypivots('FDAX')
###########################
def create_roundie(centerprice,increment,loopnum,sym):
    outfile = libarea +'spotlinesRoundies.' + sym +'.csv'
##    print outfile
    i=0
    lines=[]
    while i < 10:
        i+=1
        line=[]
        up = centerprice + (i*increment)
        down = centerprice - (i*increment)
    ##    print centerprice,up,down
        line.append(up)
        line.append('roundie')
        lines.append(line)
        line=[]
        line.append(down)
        line.append('roundie')
        lines.append(line)
    for line in lines:
        print line
    rpu_rp.WriteArrayToCsvfile(outfile,lines)
##############
centerprice = 2000
increment = 10
loopnum = 10
sym = 'ES'
create_roundie(centerprice,increment,loopnum,sym)
###############
centerprice = 9750
increment = 50
loopnum = 10
sym = 'FDAX'
create_roundie(centerprice,increment,loopnum,sym)
############
start = '01:00:05'
end   = '20:58:05'
