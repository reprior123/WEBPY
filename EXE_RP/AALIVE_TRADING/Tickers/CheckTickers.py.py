import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    if 'Tick' in var:
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
date =  today #'20160219' #yesterday # today  ######## <<<<<<<

style = ''
symlist = ['ES','FDAX']
##symlist = ['ES']#,'FDAX']
for sym in symlist:
    print sym,'========'
    bla =  TicksUtile.recenttick(sym,'recent')
    print bla,' is latest tick'
    flist = [sym+'.RTticks.csv',sym+'.5mins.both.csv']
    for f in flist:
        print f,'===='
        tickfile5 = DataDown + date +'.'+f
        l = rpu_rp.CsvToLines(tickfile5)
        lastlines = rpu_rp.tail_array_to_array(l,5)
        for e in lastlines:
            print e[0],e[1]
##print lastlines

raw_input('close...')

