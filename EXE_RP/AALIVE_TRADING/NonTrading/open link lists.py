import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
################
global recentlimit, time_format,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile,RulesEngine, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
import urllib
date =   today  ######## <<<<<<<

array = rpu_rp.CsvToLines(DataDown+'20160302.ES.5mins.both.csv')
##rpu_rp.WriteArrayToCsvfileNEW('fla.txt',array)
import numpy
numpy.savetxt('numpybla.txt',array,delimiter = ',', fmt='%s')

import webbrowser
##listl = rpu_rp.CsvToLines(projectarea +'linkslistxx.txt')
flist = glob.glob(projectarea + '*mvdlist.txt')
f= flist[0]
listl = rpu_rp.CsvToLines(f)
numlines =  len(listl)
part1 = numlines /3
part2 = numlines - part1

print part1,numlines,part2
c=0
lowlimit = part2 -1
uplimit =  numlines +1 #part2

for l in listl:
    c+=1
    link = l[0]
    if c < uplimit and  c > lowlimit:
        print link,c
    ##    urllib.urlopen(link)
        webbrowser.open_new(link)

##webbrowser.open_new(url) 
