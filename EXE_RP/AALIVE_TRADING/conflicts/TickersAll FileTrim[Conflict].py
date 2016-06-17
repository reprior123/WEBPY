import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp, rpInd, ibutiles, TicksUtile
from time import sleep, strftime, localtime
from datetime import datetime

#############################
global today, sym, symbol_list, symdict, symbol_list2
symbol_list = symbol_list2
print symbol_list
########################################
symTickerIddict ={}
contractdict ={}
symid=0
for sym in symbol_list:
    linesleft = 9000
    fname1 = DataDown+ today + '.' + sym  +'.RTMktDepth.csv'
    fname3 = DataDown+ today + '.' + sym  +'.RTtickData.csv'
    fname2 = DataDown+ today + '.' + sym  +'.RTticks.csv'
    TicksUtile.trimFile(fname1,linesleft)
    TicksUtile.trimFile(fname3,linesleft)
    symid+=1
##rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTticks',[])
##rpu_rp.WriteArrayToCsvfile(TMP +'replys.RTtickDOMs',[])
#################
