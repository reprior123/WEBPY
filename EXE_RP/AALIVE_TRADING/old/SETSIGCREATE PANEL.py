# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash + '/'
TMPnoslash = rootpath + 'TMP' + localtag
TMP = TMPnoslash + '/'
sys.path[0:0] = [EXEnoslash]
########################
sigarea = EXE + 'IbPy-master/Signals/'
timeFormat = "%Y%m%d %H:%M:%S"
dateFormat = "%Y%m%d"
#################
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
from time import sleep, strftime, localtime  
#############################
import  rpu_rp, rpInd#, ibutiles  #########remove after test

filename = TMP + 'signalcontroller.txt'
## rewrite control file
answer = raw_input('how many secs?..')
rpu_rp.WriteStringsToFile(filename,'TimeLimitRecentSigs,' +answer+',\nSignalsToShow,allsigs,\nDurationToShow,alldurs,')

sym = 'USD.JPY' #'EUR.USD'
##Sigfile = sigarea+ sym +'.sigs.csv'
rpu_rp.cattxt(filename)

##TimeLimitRecentSigs,50,
##SignalsToShow,allsigs,
##DurationToShow,alldurs,
