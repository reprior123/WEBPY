################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.py','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################   
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open('importmodlist.txt').readlines()
print moduleNames
for module in moduleNames:
    if module != titleself:
        my_module = importlib.import_module(module.strip())
######################
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
########################################
date = today
symbol_list = symlistTicker
now = datetime.strftime(datetime.now(),spaceYtime_format)
today =  rpu_rp.todaysdateunix()
todaysigs = sigarea + today+ '.recentsigs.csv'
todaypos = sigarea + today +'.positionstate.csv'
currentpos = rpu_rp.CsvToLines(todaypos)
addon = rpu_rp.CsvToLines(todaysigs)
rpu_rp.WriteArrayToCsvfileAppend(todaypos,addon)

os.system('cat ' + todaysigs + ' >> ' + todaysigs + 'bu')
filelist = glob.glob(sigarea + '*recent*')
for f in filelist:
    print f
    if os.path.isfile(f):
        os.remove(f)
filelist = glob.glob(TMP + '*')
for f in filelist:
    print f
    if os.path.isfile(f):
        os.remove(f)
os.system('echo " " > ' + todaypos)
##os.system('notepad.exe ' + todaypos)    
