# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
############################
blasym = ' €'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_' + (((path.replace('EXE_','|')).split('|'))[1]).replace('/','')
print localtag
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
dlTS = 'C:/TS/downloadsTS/'
converted = dlTS + 'GSconverted/'
###########################################
projectarea = EXE + 'PROJECT.SageFlash/'
config = projectarea + 'config_sage/'
nasarea =  rootpath 
#######################################
### convert xls to csv
####################
rnrStocklist = ['WMB', 'GILD', 'GMCR', 'ARES']
flist = glob.glob(dlTS +'*.xls')
for f in flist:
    print f
    fnew = f.replace('xls','csv')
##    if fnew in glob.glob(dlTS +'*Alloca*.xls')
    rputiles.convertXLStoCSV(f)
    fnew = f.replace('xls','csv')
    if 'Potentials' in f:
        ftag = 'Potentials'
    elif 'Allocations' in f:        
        ftag = 'Allocations'
    elif 'Executions' in f:
        ftag = 'Executions'        
    elif 'Exposure' in f:
        ftag = 'Exposure'
    else:
        ftag = 'need'
        
    lines = rputiles.CsvToLines(fnew)
    for l in lines:
        print ftag, l[1]
        if ftag == 'Exposure':
            print l

    for l in lines:
        for s in rnrStocklist:
            if s in str(l):
                print ' >>>>>>>>>>>>>>>>ATTENTION!!!! ',ftag, l[1]

        
    
    

    
