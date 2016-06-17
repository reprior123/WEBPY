# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash + '/'
TMPnoslash = rootpath + 'TMP' + localtag
TMP = EXE #TMPnoslash + '/'
sys.path[0:0] = [EXEnoslash]
########################
sigarea = EXE + 'IbPy-master/Signals/'
timeFormat = "%Y%m%d %H:%M:%S"
dateFormat = "%Y%m%d"
#################
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles
###############################3
##current data
SignalCP = TMP + 'entrycontroller.txt'
TraderCP = ''
###########
sigtimelimit =60
signalstoshow = 5
durationtoshow = '5 mins'
cycletime = 11
setting = 'NOTRANSMIT-setting,'
### nwo read existing ###
def read_varlist(): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(SignalCP)
    lista =[]
    for line in paramlines:    
        varstring = line[0]
        lista.append(varstring)
    return lista
#########################3
print read_varlist()
#######################
def read_vars(inputstring): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(SignalCP)
    for line in paramlines:    
        varstring = line[0]
        varvalue =line[1]
##        print varstring, varvalue
        var = {}
        if len(line) > 1 and inputstring == varstring:
            return varvalue
#########################3
def rewrite_param_file(varToChange,newvarval):
    paramlines = rpu_rp.CsvToLines(SignalCP)
    arrayout =[]
    for line in paramlines:    
        varstring = line[0]
        arrayline =[]
        varvalue = read_vars('varstring')
##        print varstring,varToChange
        if varstring == varToChange:
            print 'found a change'
            varvalue = newvarval
            arrayline.append(varstring)
            arrayline.append(varvalue)
            arrayout.append(arrayline)
        else:
            arrayout.append(line)
    rpu_rp.WriteArrayToCsvfile(SignalCP,arrayout)
########################3
##variable = {}
##for c in read_varlist():
##    variable[c] = read_vars(c)
##    print variable[c]
########################3
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
check_for_CP_change(TMP + 'signalcontroller.txt')

print '1. NO TRANSMIT setting'
print '2. AUTOTRADE'
print '3. DON\'T PLACE ORDERS'
print '4. QUIT THE TRADER FUNCTION'
print '5. SET TIME FOR RECENT SIGNAL HUNT IN SECONDS'
print '6. SET Cycle Delay'
print '7. no change'
answer = raw_input('choose: ')
if answer == '1':
    a = 'Setting'
    b =  'NOTRANSMIT-setting'
if answer == '2':
    a = 'Setting'
    b=  'AUTOTRADE-setting'
if answer == '3':
    a = 'Setting'
    b =  'DONOTPLACE-setting'
if answer == '4':
    a = 'Setting'
    b =  'QUIT-setting'
if answer == '5':
    a = 'TimeLimitRecentSigs'
    b = raw_input('enter in scanner range seconds: ')
if answer == '6':
    a = 'CycleTime'
    b = raw_input('enter in cycle delay seconds: ')
if answer == '7':
    rpu_rp.cattxt(SignalCP)
    bla = raw_input('click to continue')
    a = 'bla'
    b = 'bla'
rewrite_param_file(a,b)
rpu_rp.cattxt(SignalCP)
