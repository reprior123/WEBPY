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
fibR = .382
anchor = 2001
peak = 2023
trend = 'up'

symb = 'ES'
durb = '5mins' #'1day'
lastbar = rpInd.ShowABarofBars(symb,durb,1)
print lastbar
anchor = float(lastbar[3])
peak = float(lastbar[4])
print peak, anchor
if (peak - anchor) > 0:
    trend='up'
else:
    trend = 'dn'
fibspot=TicksUtile.fibbo(fibR,anchor,peak,trend)[0]
movehandles=TicksUtile.fibbo(fibR,anchor,peak,trend)[1]
fibhandles=TicksUtile.fibbo(fibR,anchor,peak,trend)[2]
print fibspot, movehandles, fibhandles

ind = 'ATR'
ATR5min =  rpInd.ShowLastBarofInd(symb,durb,ind)
print ATR5min
##############################################
##def ShowLastBarofInd(sym,dur,ind):
#####################################
##def ShowABarofInd(sym,dur,ind,barnum):
#####################################
##def ShowABarofBars(sym,dur,barnum):
#####################################
##def ShowABarofIndByTime(sym,dur,ind,bartime,barfnumlimit):
###################################
