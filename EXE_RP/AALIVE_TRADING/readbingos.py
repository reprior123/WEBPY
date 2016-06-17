################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
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
for module in moduleNames:
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
downloads = 'C:/Users/bob/Downloads/'
fname = 'bingos py - Sheet1.csv'
fname =  'BINGO RPADV - Sheet1.csv'
fname =  'bingorpinv - Sheet1.csv'
f= downloads + fname

for b in rpu_rp.TxtToLines(f):
    if 'UE' in  b:
        print b
dictbingos = rpu_rp.create_dict(f,0,1)
##print dictbingos.items()

keys = raw_input('enterkeys here with . separator...  ')
##key1 = '155'
##key2 = '134'

key1=keys.split('.')[0]
key2=keys.split('.')[1]

fullkey = dictbingos[key1] + dictbingos[key2] + ' '
##print 'here is the key...\n'
rpu_rp.WriteStringsToFile('bingoforahk',fullkey)
print fullkey

batfile = 'C:/Users/bob/Google Drive/EXE_RP/copybingos.bat'
##print batfile
ahkfile = 'C:/Users/bob/Google Drive/EXE_RP/copybingos.ahk'

##os.system(batfile) ##does not work!!!
from subprocess import Popen
Popen(batfile)


