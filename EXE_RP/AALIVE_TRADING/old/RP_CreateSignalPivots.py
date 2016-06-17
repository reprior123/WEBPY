# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
from datetime import datetime
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
statearea = DataDown + 'Signals/states/'

DataDownNoSlash = 'C:/TS/TSIBData'
soundarea = path + 'sounds/'
#######################################
global recentlimit, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
from datetime import datetime
import datetime as dt
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
spaceYtime_format = " %Y-%m-%d %H:%M:%S"
##############################
cpfname = EXE + 'signalcontroller.txt'
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)

libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
modedict = rpu_rp.create_dict(libbars,0,5)

symdict = rpu_rp.create_dict(libsyms,0,1)

tickvaluedict = rpu_rp.create_dict(libsyms,0,8)
tsizedict = rpu_rp.create_dict(libsyms,0,7)
showdecimaldict = rpu_rp.create_dict(libsyms,0,9)
entrywiderdict = rpu_rp.create_dict(libsyms,0,10)

libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)

libsymNEWS = EXE + 'library.symNEWSTIMES.csv'
symNEWSdict = rpu_rp.create_dict(libsymlines,0,2)


symbol_list = symdict.keys()
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
        barlist.append(b)
print barlist
##################
prevsigid = ''
today =  rpu_rp.todaysdateunix()
##today = '20150702'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def read_varlist(cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    lista =[]
    for line in paramlines:    
        varstring = line[0]
        lista.append(varstring)
    return lista
#########################3
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
def read_vars(varstringin,cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    for line in paramlines:
##        print line
        varstring = line[0]
        if len(line) > 1 and varstring == varstringin:
            varvalue =line[1]
    return varvalue
########################
def recenttick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
    for f in tickline:
        if 'close' in str(f):                        
            lasttick = f.split('=')[1]
    return lasttick
#################
loopmax = 2
loop = 0
global command
command = read_vars('Setting',cpfname)
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 3
print 'recent limit is now.. ', recentlimit
sigs = rpu_rp.CsvToLines(sigarea + today +'.sigs.csv')
########################
import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
###############
def look_for_dupe_sig(livesigid):
    tradedsigs= rpu_rp.CsvToLines(sigarea + today +'.recentsigs.csv')
    showflag = 'show'
    for lin in tradedsigs:
        if len(lin) > 3:
            sigid = lin[7]
            if sigid == livesigid:
                showflag = 'supress'
    return showflag
#################################
while loop < loopmax:     
    now = datetime.strftime(datetime.now(),spaceYtime_format)
    now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))      
    now_dt = dt.datetime.strptime(now, spaceYtime_format)   
    print 'cycle heartbeat...searching for sigs in last ',recentlimit
    recentsigs =[]
    for sym in symbol_list:      
        ####################################
        for barsize in barlist :
            timeframe = bardict[barsize]
            durinseconds = secdict[barsize]
            barsizeNtimeframe = timeframe + barsize
            dur = barsize       
##            TicksUtile.assemble_dur_bars(today,sym,dur,durinseconds)  
            DurBoth = rpu_rp.CsvToLines( DataDown+ today + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
            indlist = ['pivot', 'R']
            for indicator in indlist:
                print sym
                indarr = rpInd.GetPivots(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
            indlist2 = ['kupper', 'klower', 'kmid']
            for indicator in indlist2:
##                print indicator
                indarr = rpInd.GetKupper(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)
##                keltner_channel_upper(highs,lows,closes,mult)
            indlist3 = ['ema']
            for indicator in indlist3:
##                print indicator
                indarr = rpInd.GetEMA(DurBoth,sym,indicator)
                statename = sym+'.'+dur.replace(' ','')+'.'
                statefile = statearea +statename + indicator  + '.state.csv'
                rpu_rp.WriteArrayToCsvfile(statefile, indarr)                
####################
##            macdTriggers = rpInd.Trigger_MACD(DurBoth,sym,barsize)               
    ##############################            
    loop +=1
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
