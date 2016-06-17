

import os, sys
path = os.getcwd() + '/'
EXEnoslash = ((path.replace('\\AALIVE_TRADING','|')).split('|'))[0]
rootpath = ((path.replace('EXE','|')).split('|'))[0]
sys.path[0:0] = EXEnoslash
localtag = ((EXEnoslash.replace('EXE','|')).split('|'))[1] #'_RP'
print localtag,'is local'
#########################################
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var, nd[var]
    locals()[var] = nd[var]
##################
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
##btest = path.replace('EXE_RP','EXE_BTEST')
##print btest
##print EXE
flist = ['CreateSmain','RulesEngine','rpInd']
ext = '.py'
##f = 'CreateSmain.py'
for f in flist:
    print '####',f,'#####'
    ##f = 'RulesEngine.py'
    file1 = 'C:/Users/bob/Google Drive/EXE_RP/AALIVE_TRADING/'+f+ext
    file2 = file1.replace(f,f+'Conflict')
    print file2
    print file1

    mode = 'changes'
    ##mode = 'adds'
    bla = rpu_rp.diff2files(file1, file2, mode)
    for l in bla:
        print l

####raw_input('cont?')
