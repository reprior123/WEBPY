import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
localtag = '_RP'
import ENVvars
nd={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#############
import rpu_rp

downloads = 'C:/Users/bob/Downloads/'
fname = 'bingos py - Sheet1.csv'
fname = 'BINGO RPADV - Sheet1.csv'
f= downloads + fname

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

print fullkey
print'\nclick to exit'
raw_input('click to exit\n')




