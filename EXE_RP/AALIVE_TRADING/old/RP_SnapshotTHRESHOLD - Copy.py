# -*- coding: utf-8 -*-
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
###############
import os, glob, csv, subprocess, datetime, shutil, subprocess, time
import os.path
from datetime import datetime
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile
import ctypes
#######################
today =  rpu_rp.todaysdateunix()
####timedateFormat = "%Y%m%d %H:%M:%S"
####spaceYtime_format = " %Y-%m-%d %H:%M:%S"
##################################
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

libsymlines = EXE + 'library.symlines.csv'
symlinedict = rpu_rp.create_dict(libsymlines,0,1)

symbol_list = symdict.keys()
barlistall = bardict.keys()  ##
barlist =[]
for b in barlistall:
    if modedict[b] == 'intraday'  and b != '5 secs':
##    if modedict[b] == 'daily'  and b != '5 secs':
        barlist.append(b)
print barlist
##################
prevsigid = ''
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
########################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
def recenttick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickvalue = float(tickvaluedict[sym])
    if os.path.isfile(RecentTickFile) :
        tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
        lasttick = rounderrp(float(tickline[5]),tickvalue)
    else:
        lasttick = 9999
    return lasttick

import winsound, sys
def beep(sound):
    pass
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
##################
def create_slicendice():
    print 'slicedice'
    #analyze
prevcycledelay = 2
########################
def make_dur_state(sym,dur,threshold,indlist):
##    print sym,dur, crxcode
    rpInd.create_states_files(sym,dur,today,threshold,indlist)
    for ind in indlist:
        state = rpInd.ShowRecentState(sym,dur,ind)
        stateAge = rpInd.ShowRecentAge(sym,dur,ind)
        val = rpInd.ShowRecentStateValue(sym,dur,ind)
        crxtime = rpInd.ShowRecentCRXTime(sym,dur,ind)
        crxcode = rpInd.ShowRecentCRXCode(sym,dur,ind)
        price = rpInd.ShowRecentClPrice(sym,dur,ind)
        
        
##        print  state, stateAge,val,ind, crxtime,price , sym, dur, threshold, crxcode
        print crxcode,sym
#######################    
def snapshot_sym(sym):
    barlist = ['1min', '3mins', '5mins', '15mins', '1hour']
    barlist = ['1min' ]#, '3mins', '5mins', '15mins', '1hour']
    posstate = rpInd.ShowRecentPositionState(sym)
    print posstate,sym
    indlist = ['mcross']#,'kupper']
    print 'recentstate age val name'
    for dur in barlist :
        threshold = 0.0

        if dur == '1min':
            threshold = 0.0
        make_dur_state(sym,dur,threshold,indlist)
##        Triggers = rpInd.Trigger_from_states(sym,dur,'kupper')
##        lasttwo = rpu_rp.tail_array_to_array(Triggers,2)
##        for l in lasttwo:
##            print l[0],l[1],l[7],l[5],l[8],l[11]
    print '======================='
###########################
def run_menu():
    c=0
    symnumdict={}
    for sym in symbol_list:
        c+=1
##        print sym, c
        symnumdict[str(c)] = sym
##        symnum = raw_input('chooose')
##        sym = symnumdict[symnum]
        snapshot_sym(sym)
    sleep(8)
run_menu()
'''                    if action == 'negcrxx' and state15 == 'neg':
                        print 'is a sell'
                        tflag = 'passedtest'
                    elif action == 'poscrxx' and state15 == 'pos':
                        print 'is a buy'
                        tflag = 'passedtest'
                        pass
                    elif action == 'poscrxx' and posstate == 'SELL':
                        tflag = 'passedtest'
                        pass
                    elif action == 'negcrxx' and posstate == 'BUY':
                        tflag = 'passedtest'
                        pass
                    else:
                        print action, ' signal failed on ... ',dur,sym
                    if tflag == 'passedtest':
                        lasttick = recenttick(sym)
                        onesig.append(barToNow)
                        onesig.append(barToPrev)
                        onesig.append(lasttick)
                        recentsigs.append(onesig)

    sleep(cycledelay)
print 'finished ',loopmax,' loops  by Signal Creator...dead since..',now
#############
def create_report(Sigfile,sym,barsize):
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
    print 'if i am 20 bars old in signal, start with trail stop depends on dur...shotrt dur = short age'
##    average number of sigs in 30 bars  has it flipped alot
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#################
'''
