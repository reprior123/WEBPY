import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
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
import  glob, csv, datetime, shutil, subprocess, time
import rpu_rp, rpInd, ibutiles, HistoricalDataDload, TicksUtile
############################################
##symbol_list = symdict.keys()
##symbol_list_opts = ['SPY']
startmode = 'initialize'
strike= 200
HistoricalDataDload.dload_listNEW(symbol_list_opts,'alll',strike)
##HistoricalDataDload.dload_list(symbol_list_opts,'alll')

for sym in symbol_list_opts:
    print sym
    TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
