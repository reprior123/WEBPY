# -*- coding: utf-8 -*-
import os, sys
############################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_RNR'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
########################
import rputiles
import glob, csv, subprocess, datetime, shutil, subprocess
##import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
GS = DATA + 'GS/'
###########################################
outputarea = TMP
#######################################
fname = DATA + 'etfs.sorted.txt'

tradefile = GS + 'GBLACTIVITY20140619090047C132482.csv'
patternINheader = 'Account Number'
trades = rputiles.CsvToLines(tradefile)
stktrades =[]
count = 0
for trade in trades:
        count +=1
        if count ==1:
                header = trade
                print header
                stktrades.append(trade)
##        print trade
        if 'P1Q'  in trade:
                print trade
                
                stktrades.append(trade)
fnameout = TMP +'stocktrades.csv'
rputiles.WriteArrayToCsvfile(fnameout,stktrades)
import rputilesPIV # just by importing, will run it if hard coded in module
##pivotpivot_final_print(vlookup1, vlookup2, hlookup1,sum_field,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname)
##pivottablerp              
##########   Run all DETAILS first at both BASE and CHF CURRENCY    ########
fname = fnameout
sumcatH = 'Trade Date' #'Symbol/Description'
fheader1 = 'Account Number'
fpattern1 = '3FF61209'
fheader2 =  fheader1
fpattern2 = fpattern1
fheader3 = fheader2
fpattern3 = fpattern2
sumcat1 = 'Symbol/Description'#'Trade Date'    
sumcat2 = sumcat1#'Symbol/Description'
sumvalue = 'Quantity'
##########################################
rputilesPIV.pivotloop(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader)

