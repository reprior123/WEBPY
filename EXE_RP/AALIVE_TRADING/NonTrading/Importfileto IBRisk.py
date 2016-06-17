# -*- coding: cp1252 -*-
import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE_RP'
sys.path[0:0] = [rootpath + 'EXE_RP']
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
####################
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
from time import sleep
import  rpu_rp, rpInd, TicksUtile,BarUtiles
import ctypes
yesterday = '20151218'
date =  yesterday # today
#####################3
##########    pivot = rpInd.gatherline(sym,'pivot')###    R1 = rpInd.gatherline(sym,'R1')#####    S1 = rpInd.gatherline(sym,'S1')
######    print S1,R1,pivot
    ##do the same for weekly by adding dur to variables and create a weekly  from dailys..
##    find pivots, find fibbo retraces on recnt moves[rangebars,hi,lo]
##    read spots from file
##    calculate two roundies
##    calculate 10 handles off high of day,lowday,openday,yestclose,prevhourhilow
#############################################
import RP_Snapshot 
###############
def prepare_imp_file(filein,fileout):
    newlines =[]
    lines = rpu_rp.CsvToLines(filein)
    headerline =['Action', 'Quantity', 'Symbol', 'TimeInForce', 'SecType', 'OrderType', 'LmtPrice', 'Exchange', 'Currency', 'CUSIP', 'ISIN', '']
##    itemlist = [Action, Quantity, Symbol, TimeInForce, SecType, OrderType, LmtPrice, Exchange, Currency, CUSIP, ISIN]

    newlines.append(headerline)
    for l in lines:
        newline =[]
        print l
        isin = l[6]
        action = l[0]
        title = l[3]
        qty = l[5]
        price = l[2]
        c=0
        for i in headerline: # itemlist:   
##            print i
##            newline.append(i)
            newline.append(l[c])
            c+=1
        newlines.append(newline)
    rpu_rp.WriteArrayToCsvfile(fileout,newlines)
prepare_imp_file(documents+'bla.csv',documents +'fileout.csv')
