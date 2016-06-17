# -*- coding: utf-8 -*-
import os, sys
##from datetime import datetime
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
import glob, csv, subprocess, datetime, shutil, subprocess, time, os.path
import  rpu_rp, rpInd, TicksUtile, ctypes 
##############################
#StochK,1min,valtest,poscrxx,1,0,21,BUY,stochkLT20
ind =  'mcross' #'StochK' #'Stoch_CROSS' #'StochK'
fnameind = 'mcrosssimple'
dur = '3mins'
test = 'stringtest' # 'stringtest'
##test = 'valtest' # 'stringtest'
text = 'slopeup' # 'neg'
text = 'poscrxx'
position ='8'  ## 4 is slope,,1 is ind val, 
minval = 0
maxval = 20
side = 'BUY'
rulename = ind+dur+text+str(minval)+'x'+str(maxval)+side
fnametag = 'mcrosssimple'
ilist = [ind,dur,test,text,position,minval,maxval,side,rulename]
outfile =  fnameind+'.'+dur+'.'+side+'.'+fnametag +'.rules.csv'
lines = []
ruleline = []
for i in ilist:
    ruleline.append(i)
lines.append(ruleline)
print ruleline
rpu_rp.WriteArrayToCsvfileAppend(outfile,lines)
##########

side = 'SELL'
text = 'slopedn'
text = 'negcrxx'
minval = 80
maxval =10100
lines = []
ruleline = []
rulename = ind+dur+text+str(minval)+'x'+str(maxval)+side
ilist = [ind,dur,test,text,position,minval,maxval,side,rulename]
outfile =  fnameind+'.'+dur+'.'+side+'.'+fnametag +'.rules.csv'
for i in ilist:
    ruleline.append(i)
lines.append(ruleline)
print ruleline
rpu_rp.WriteArrayToCsvfileAppend(outfile,lines)





##########################################
####def show_spots(sym,date):
####    barfile = DataDown +'20150918.' +sym +'.RTtickslastquote.csv'
####    rpu_rp.CsvToLines(barfile)
####    curprice = float((rpu_rp.CsvToLines(barfile)[0])[5])
####    print curprice
####    spotfile = EXE +'es.lines.new.csv'
######    print symlinedict
####    filein = DataDown + date + '.' + sym + '.5mins.both.csv'
####    lines = rpu_rp.CsvToLines(filein)
####    spotlines= rpu_rp.CsvToLines(spotfile)
####    for l in spotlines:
####        spotp = float(l[0])
####        if abs(spotp-curprice) < 15.00:
####            print curprice-spotp,spotp,curprice
######    oneline = grep '16:05:00' filein
######    onelinearray = rpu_rp.grep_array_to_array(lines,'16:05:00')
######    print onelinearray
#####################3
##########    pivot = rpInd.gatherline(sym,'pivot')
##########    R1 = rpInd.gatherline(sym,'R1')      
##check_for_lines(sym)
###############
##def create_roundies(sym):
##    curprice = 2100 #need to read froma bar ranger
##    take curr price
##    factor = price / 100
##    using factor, calculate 3 roundies up and 3 down
##    write them to roundie file
##    create combined lines file with adding lines to roundies
    ##############
