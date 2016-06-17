# -*- coding: utf-8 -*-
import os, sys
############################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_RP'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
########################
import rputiles
import glob, csv, subprocess, datetime, shutil, subprocess
##import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
PROFILES = rootpath + 'Profiles/SAY1/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
GS = DATA + 'GS/'
LOGAREA = PROFILES + '/QT/Log/'
###########################################
print '\n MENU of programs...choose one  \n\n #########'
proglist = ['show deflines rputiles',\
            'CleanFoldersRP', \
            'RT.tradepnl',\
            'dailychecks']
i=0
chdict = {}
while i < len(proglist):
    print i, proglist[i]
    chdict[str(i)] = proglist[i]
    i+=1
choice = raw_input('choose...: ')

print chdict.items()
print chdict[choice]
execfile(proglist[int(choice)] + '.py')
raw_input('click to finish..')

##tools needed:
##    1. WarnTurnedOff [needs to run on a cycle 5 minutes]
##    check if quoting is turned off and
##    profmult PE3 n PE4 level which are non 1
##    and fade flags wihch are on
##    PE31 for non empty
##    PET
##    underPI3 and under PI4
    ##################
    
