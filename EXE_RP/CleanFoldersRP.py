# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
############################
blasym = ' €'
localtag = '_RP'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
userroot = ((path.replace('GDRIVE','|')).split('|'))[0]
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import  rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
projectarea = EXE + 'PROJECT.SageFlash/'
#######################################
Docs = userroot + 'Documents'
DocsSlash = Docs + '/'
####################
##rpfile = EXE + 'rputiles.py'
##r = open(rpfile, 'r')
##for line in r.readlines():
##    if 'def' in line:
##        print line.strip()
##r.close()

##show folders
print Docs
rputiles.ShowDirList(Docs)


mainfolder = ''
