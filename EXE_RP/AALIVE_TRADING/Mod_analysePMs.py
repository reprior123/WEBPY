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
durlist = barlistall
###################
def show_spots(sym,date,curprice):
    print symlinedict
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
date =  rpu_rp.todaysdateunix()
##date = '20150910'
datehyphen = rpu_rp.todaysdatehypens(date)
##########################
import RP_Snapshot
sym = 'ES'
print 'TODAY <<<<<<'
def get_info(date):
    todayhyphen = rpu_rp.todaysdatehypens(date)
##    RP_Snapshot.snapshot_sym(sym,date,['5mins']) ## need this to create good both bars ##
    
##    btime = '15:30:0'
##    RP_Snapshot.show_one_bar('ES','1min',btime,date)
    ###############
    pmLines = RP_Snapshot.show_bar_range(sym,'5mins','21:20:00','22:05:00',date)
    for line in pmLines:
        print line
#####################
dur = '1min'
##dlist=['20150910','20150909','20150908','20150907','20150904','20150903','20150902','20150901','20150831','20150830']
flist = glob.glob(DataDown + '2015*' + '.' + sym + '.'+dur +'.both.csv')

for f in flist:
    date=f.replace(DataDown,'').split('.')[0]
    print 'TODAY <<<<<<'
    print date
##    get_info(date)

######################
##sym = 'ES'
##dur = '1min'
for sym in symbol_list:
    for dur in barlistall:
        makebars = TicksUtile.createMultiDay_bar_files(sym,dur,'.both.csv')
