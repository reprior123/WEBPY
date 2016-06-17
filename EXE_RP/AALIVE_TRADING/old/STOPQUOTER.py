# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash + '/'
TMP = rootpath + 'TMP' + localtag + '/'
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
controlfname = TMP + 'QUOTEcontroller.txt'
rpu_rp.WriteStringsToFile(controlfname,'QUIT-setting,')
print  controlfname
rpu_rp.cattxt(controlfname)
sleep(10)
rpu_rp.WriteStringsToFile(controlfname,'RUN-setting,')
sleep(1)

