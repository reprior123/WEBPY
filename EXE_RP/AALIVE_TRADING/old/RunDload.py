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
##    print var
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
####################
import  glob, csv, datetime, shutil, subprocess, time
import rpu_rp, rpInd, ibutiles, TicksUtile
############################################
strikelist =['x']
expirylist =['x']
barlist = ['1min']
symlist = ['SPY']
barlist = barlist1min
rpu_rp.WriteArrayToCsvfile('symlist.csv',[symlist])
rpu_rp.WriteArrayToCsvfile('barlist.csv',[barlist])
execfile('HistoricalDataDloadFLEX.py')
##########
strikein = round(float(TicksUtile.recenttick('SPY','both')),0)
print strikein
################
symlist = ['SPYF1'] #symbol_list_opts
strikelist = [strikein]
expirylist = ['20151218']
rpu_rp.WriteArrayToCsvfile('symlist.csv',[symlist])
rpu_rp.WriteArrayToCsvfile('barlist.csv',[barlist])
rpu_rp.WriteArrayToCsvfile('strikelist.csv',[strikelist])
rpu_rp.WriteArrayToCsvfile('expirylist.csv',[expirylist])
execfile('HistoricalDataDloadFLEX.py')
#########
symlist = ['SPYF2'] #symbol_list_opts
expirylist = ['20151120']
rpu_rp.WriteArrayToCsvfile('symlist.csv',[symlist])
rpu_rp.WriteArrayToCsvfile('expirylist.csv',[expirylist])
execfile('HistoricalDataDloadFLEX.py')
##############

###################
## take spy price from 1 min dload file...use it to setup strikes
## take dload 5sec bars of option strikes for recent price
##setup the volatility request
##read the vola from reply file..compare vols

startmode = 'initialize'
##this needs to be run after dload to create both file, as there is no recent file
for sym in symbol_list_opts:
    print sym
    TicksUtile.prepare_tickfilesto5secBars(today,sym,startmode) ## merge the 5secddload with 5sec recents > 5sec boths
