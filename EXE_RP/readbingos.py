import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
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
import rpu_rp

downloads = 'C:/Users/bob/Downloads/'
fname = 'bingos py - Sheet1.csv'
fname =  'BINGO RPADV - Sheet1.csv'
f= EXE + fname

for b in rpu_rp.TxtToLines(f):
    if 'UT' in  b:
        print b
dictbingos = rpu_rp.create_dict(f,0,1)
##print dictbingos.items()

keys = raw_input('enterkeys here with . separator...  ')
##key1 = '155'
##key2 = '134'

key1=keys.split('.')[0]
key2=keys.split('.')[1]

fullkey = dictbingos[key1] + dictbingos[key2]
print 'here is the key...\n'

##print fullkey
os.system('echo ' + fullkey + ' > '+AS + 'tempkey.txt')
##from subprocess import call
##call('C:/TS/copybingos.ahk')
stream = os.popen(AS + 'copybingos.ahk')






