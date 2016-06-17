# -*- coding: utf-8 -*-
#########################################
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile

path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
Cpath = 'C:/'
################
##############localtag = '_RP'
##############import ENVvars
##############nd={}
##############nd = ENVvars.ENVvars(localtag)
################resolve vardict back to normal variables
##############for var in nd.keys():
##############    locals()[var] = nd[var]
import stat,md5

import rpu_rp
from datetime import datetime
import datetime as dt
################################
##EXEnoslash
def show_filesinfolder_size(folder):
    size =0
    filelist = glob.glob(folder+'/*')
    for f in filelist: 
        if  os.path.isfile(f):
            size = size + (os.stat(f)[stat.ST_SIZE])/100000
    return size
##############################
################################
def walkfolder(foldername):
    size =0
    for root, dirs, files in os.walk(foldername, topdown=True):
        for name in dirs:
            size += show_filesinfolder_size((os.path.join(root, name)))
##            print(os.path.join(root, name))
##    print size, foldername
    return size
################################
##walkfolder(EXEnoslash)
###########################
def show_subfolders(folder):
    size =0
    folds =[]
    filelist = glob.glob(folder+'/*')
    for f in filelist: 
        if  not os.path.isfile(f):
            folds.append(f)
    return folds
#######################
users = 'C:/Users/bob/Desktop/goo sage reports/pics taken out of trash dupes on gdrive poss'
users = 'C:/Users/bob/'

##show_filesinfolder_size(EXEnoslash)
subfolders = show_subfolders(users)
for fold in subfolders:
    subfoldersnew = show_subfolders(fold)
    size = walkfolder(fold)
    print '%8d %s' % (size,fold)
    for folda in subfoldersnew:
##        subfoldersnew = show_subfolders(fold)
        size = walkfolder(folda)
        print '%8d %s' % (size,folda)
'''  
filelist = glob.glob(rootpath+'*')
##print filelist
for fd in filelist:
    if  os.path.isfile(fd):
        size = os.stat(fd)[stat.ST_SIZE]
        print fd, size
        pass
    else:
        print fd,'is directory'
    
    listb = rpu_rp.ShowDirList(fd)
    for f in listb:
        if 'waterski' in str(f):
            print f
##            flist.append(fd)
'''
