# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
localtag = '_RNR'
##################2##############
path = os.getcwd() + '/'
blapath = path.replace('EXE','|')
print blapath.split('|')[1]
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import HVARs, rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
outputarea = TMP
TS = 'C:/TS/'
linestrings = ''
#######################################
def TxtToLines(justfilename):
    lines = []
    try:
        with open(justfilename, 'r') as afile:
            linesnew = afile.readlines()
            for line in linesnew:
                lines.append(line.strip())
    except:
        print 'could not read ' + str(justfilename) + ' for TxtToLines in rputiles'
        pass
    return lines
##########################
uzipped =  TS + 'actant logs'
zips = uzipped + '/zipped logs'
listz = os.listdir(zips)
listu = os.listdir(uzipped)
for f in listu:
    if 'AQTOR' in f:
        hf = uzipped + '/' + f + '/Data/HyperFeedInstruments.txt'
        subdir = uzipped + '/' + f
        sublist = os.listdir(subdir)
        for filename in sublist:
            if 'screenshot' in filename:
                os.copy(subdir + filename, tgt + shortname + shortdate + filename
##        print hf
        shortname = f.split('_')[1]
        shortdate = (f.split('_')[2])[0:5]
        
##        print shortname, shortdate
        hstocks = TxtToLines(hf)
        for lineb in hstocks:
            if '//'  not in lineb:
                print shortname, shortdate, lineb
            







##
##
##    for u in listz:
##        if f in u:
##            print f,u
##print len(listz), len(listu)
