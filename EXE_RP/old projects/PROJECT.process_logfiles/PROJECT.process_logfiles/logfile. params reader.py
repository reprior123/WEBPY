# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
############################
blasym = ' €'
localtag = '_RNR'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import HVARs, rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
projectarea = EXE + 'PROJECT.SageFlash/'
config = projectarea + 'config_sage/'
nasarea =  rootpath 
SAGE_EXPORTS = TMP
outputarea = TMP
#######################################

## list other arguments here like logfile repos, agelimit etic.

logfile_repos = 'C:/TS/actant logs/'
##zipfname = 'AQTOR_20140203_1'
##unziparea = logfile_repos + zipfname + '/' 
alllines =''
for f in (os.listdir(logfile_repos)):
    if '.zip' not in f and '.log' not in f:
##        print f
        fbase = logfile_repos + '/' + f 
        for f1 in (os.listdir(fbase)):
##            print fbase
            if 'Data' in f1:
                fbase2 = fbase +'/' + f1             
##                print fbase2
                for f2 in  (os.listdir(fbase2)):
                    print f2
                    if 'ParametersChanged' in f2 and 'bck' not in f2:
                        newf = open(fbase2 + '/' + f2, 'r')
                        for line in newf.readlines():
                            if 'V:QuoteEngine' in str(line):
##                                print line
                                alllines += line
##                        print f2, fbase2
                        newf.close()
                        newarray = rputiles.uniq(alllines)
##        rawname = f.replace('.zip', '')
##        zipfullfname = logfile_repos + rawname + '.zip'
##        unziparea = logfile_repos + rawname + '/' 
##        outfile = open(logfile_repos + 'target.log.txt', 'w')
##        bla = zipfile.ZipFile(zipfullfname, "r")
##        bla2 = bla.extractall(unziparea)
##        file = zipfile.ZipFile(zipfullfname, "r")
# list filenames


##for name in file.namelist():
####    if '.log' in name:
##    print name
##    data = file.read(name)
##    print name, len(data), repr(data[:10])
##    outfile.write(data)
##  
### list file information
##for info in file.infolist():
####    if '.log' in info.filename:
##    print info.filename, info.date_time, info.file_size
