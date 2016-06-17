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
#####################
import  rpu_rp, rpInd
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
#######################################
today =  rpu_rp.todaysdateunix()  ##today ='20150605'
##############################################
##        from datetime import timedelta
##        date_format = "%d-%m-%Y"
from datetime import datetime
current_time = datetime.now().time()
print current_time.isoformat()
##############################
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
barlist = bardict.keys()  ##
barlist = ['15 mins', '15 secs', '1 min', '1 hour', '5 mins']
##########################
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()  ##['GBP.USD', 'EUR.USD', 'USD.JPY', 'AUD.USD', 'NQ', 'ES']
print symbol_list
print barlist
loopmax = 400 ##<<<<<<<<<<<<<
recentlimit = 60
###############################
def createlines(fname):
    recentfile = fname.replace('.csv','.recent.csv')
    rpInd.prepare_tick_files(inputfile,'tempbars.csv',recentfile)
    lines = rpu_rp.CsvToLines('tempbars.csv')
    return lines
###############################
global decimalboost
##########################################
import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
########################
def process_ticks(lines,decimalboost,dur):
    ################
    bs = rpInd.strip1float(lines,5,decimalboost) ##raw close price
    bshighs = rpInd.strip1float(lines,3,decimalboost)
    bslows = rpInd.strip1float(lines,4,decimalboost)
    timestamparray = rpInd.strip1string(lines,1)
    symarray = rpInd.strip1string(lines,0)
    sym = symarray[1]
    durarray = []
    for b in symarray:
        durarray.append(dur) 
    ########################
##    sma21 = rpInd.mvavgToArray(bs,21)
    ######################
    ### create pivots rs and ss ###
##    def pivotpoint(a1,a2,a3):
##        c=0
##        arrayout =[]
##        arrayout.append(a1[0])
##        while c < len(a1):
##            c+=1
##            piv = a1[c-1] + a2[c-1] + a3[c-1]
##            arrayout.append(piv)
##        return arrayout
######################
##    piv = pivotpoint(bs,bshighs,bslows)
##    ######################
##    def R1(a1,a2):  ## S1 is the same but with lows
##        c=0
##        arrayout =[]
##        arrayout.append(a1[0])
##        while c < len(a1): #a1 is pivotpoint array
##            c+=1
##            S1 = (2*a1[c]) -  a2[c-1]#prevhiarray
##            arrayout.append(S1)
##        return arrayout
######################
##    R1 = R1(piv,bshighs)
####    ppoint = (prevbarHi + prevbarlo +prevclose)/3
########################################
    signbs = rpInd.show_sign(bs,'price')
    slopebs = rpInd.show_slope(bs,'price')
    ##### MA Cross ##
    macrossval = rpInd.difftwoarrays(rpInd.EMAmvavgToArray(bs,9),rpInd.EMAmvavgToArray(bs,21))
    signmcd = rpInd.show_sign(macrossval,'mcd') 
    crossesmcd = rpInd.show_crossover(signmcd,'mcd')
    slopemcd = rpInd.show_slope(macrossval,'mcd')
    MDarray = rpInd.makearrayJust2(timestamparray,symarray,durarray,bs,macrossval,crossesmcd,signmcd)
    ma = rpu_rp.grep_array_to_array(MDarray,'cross')
    rpu_rp.WriteArrayToCsvfileAppend(sym+'.sigs.csv', ma)    
##############################
    from datetime import datetime
    current_time = datetime.now()##    timenow = float(current_time.isoformat().replace(':',''))
    prevt = 0
    numsigs = len(ma)
    signum =0
    timex = current_time.isoformat()
    import datetime as dt
    time_format = "%H:%M:%S"
    now = datetime.strftime(current_time,time_format)
    now_dt = dt.datetime.strptime(now, time_format)
    prevbart_dt = now_dt
    for l in ma:
        signum +=1
        if len(l[0].split()) == 2:  ##            time = l[0].split()[1].replace(':','')
            currentbar =  l[0].split()[1]
        else:
            currentbar = (l[0].split()[0])
        htime_format = '%H'    
        currentbar_dt = dt.datetime.strptime(currentbar, time_format)
        hour = dt.datetime.strftime(currentbar_dt, htime_format)
        now_dt = dt.datetime.strptime(now, time_format)
##        print now,currentbar
        barToNow = (now_dt - currentbar_dt).seconds
        barToPrev = (currentbar_dt - prevbart_dt).seconds
        alerttxt = l[1] + '|' + str(barToNow) + '|' + str(barToPrev)+ '|' +str(l)
        prevbart_dt  = currentbar_dt
##        print signum,numsigs,barToNow,'signum,numsigs,barToNow,'
##['21:52:21', 'USD.JPY', '30 secs', 125.6075, 0.00011005009737630189, 'poscrossmcd', 'posposmcd'
        if barToNow < recentlimit and signum == numsigs:
            rpu_rp.WriteArrayToCsvfile('sigs.csv',ma)
##            Mbox('Trade Alert', alerttxt, 1)
            rpInd.format_lines(ma,1)  #tailamount
    ## end of process ticks def   ################################################
t=0
from time import sleep, strftime, localtime  
##############################
while t < loopmax:
    t+=1     
    for symbol in symbol_list:
        rpu_rp.WriteArrayToCsvfile(symbol+'.sigs.csv', '') # flush the file to keep all sigs
        for tf in barlist:
            bardur = bardict[tf]
            totalsecs = secdict[tf]
            dur = bardur + tf
            files =  glob.glob(DataDown+ today + '.'+symbol+'.' + dur + '.csv') #[date 5 mins.2 D.GBP.csv 
            for inputfile in files:
                fsplit = inputfile.split('.')
                if len(fsplit) == 4:
                    sym = inputfile.split('.')[1]
                else:
                    sym = inputfile.split('.')[1] + '.' + inputfile.split('.')[2]
                ticklines = rpu_rp.CsvToLines(DataDown + today + '.' + sym + '.ticksnaps.csv')
                lastline = rpu_rp.tail_to_txtfile(inputfile,2,'outfile') ## get last line of historical file for time check
                strings= rpu_rp.catstring('outfile') ## this is the last line
                fulldatetime = strings.split(',')[1] #figure out the time
                try:
                    time = fulldatetime.split()[1]
                    pass
                except:
                    time ='23:59:58'
                hourmincutoff = time.split(':')[0] + time.split(':')[1] ## this the cutoff time
                timebarforsnaps = totalsecs
                newbars = rpInd.create_bars(ticklines,50000,timebarforsnaps,'fullbar','snapshot', sym,hourmincutoff) #field three is timesize in seconds
                rpu_rp.WriteArrayToCsvfile(DataDown+today + '.' + sym + '.'+ dur + '.recent.csv',newbars)
                lines = createlines(inputfile)
                decimalboost = dboostdict[sym]
                process_ticks(lines,decimalboost,tf)
    sleep(9)
print 'finished all ',loopmax,' loops lookin for signals by Signal Creator...dead since..',

'''
create a report on all distances.....
##############################
1day = buy,6 bars ago, 9 positive ticks ago, starting to roll, nearing a daily pivot
124.81,13:17:22,124.8075,124.8275,124.7975,124.8125,50000,904,124.8125
ES, 2015-06-02 00:00:00, 2111.0, 2111.5, 2110.75, 2111.25, -1

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
Mbox('Your title', 'Your text', 1)
Note the styles are as follows:

##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | No 
##  6 : Cancel | Try Again | Continue

-POLL FOR POSITION TO POSITION FILE EVERY 15 SECONDS
-ATTACH BRACKET ORDER
-RUN ON THE DAX 
-IDENTIFY THRUST
-IDETIFY WEDGE...BE CAREFUL OF WEDGES, THEY CAN GO EITHER WAY
-IDENTIFY LINES AS S OR R AND NEVER BUY UNDER AN R LINE ETC...
- USE 3X STOP DISTANCE FOR BIG MOVE PLAYS
- USE 1/3x STOP FOR SMALL MOVERS SARDINES
- GRAB TRADE DATA FROM ACTION FOREX
- IDENTIFY ACTION FOREX BROAD SIGNAL DIRECTION AND DRAW THE WIDE LINES

        ## NEED TO ADD DAILY AND HOURLY AND 4HOURLY TEST AT LEAST ONCE PER HOUR....
        ## ADD ALL THE HITS UP AND GIVE IT A STRENGTH RATING...
        ## 4 HOURS IS 6 POINTS...DEPENDING ON WHERE IN THE CYCLE WE ARE AND DISTANCE TO 21ma
        ## IF AT EDGE, REDUCE POINTS...RELATIVE RECENT 4HOUR SIG = MORE POINTS
##        identify doji bars and shooting stars using open close hilo..hisection - lowsection size of hsect size of body
##
##        hi low of bar relative to 21 bar line
##        price now relative to 21bar
##        most recent run up and down ...what happened.
##        number of bars between sigs...#bars to collect....
##        wedge  patterns of higher highs and lower highs or barrier at resistence wedge..
##        sigs are better away from lines or selling under lines
##        bars till the last sig
##        1 minute wears off after x bars, unless there is thrust.....
##        plot and store the lines in a file...lines can stop a sig!!!
##        several sigs in 1 and 5 mns = chop
##        trend is # bars old...new = better..
##        what does it mean if the 5 min never crossed
##        calculate the pivot and r lines using
##        ppoint = (prevbarHi + prevbarlo +prevclose)/3
##        r1 = 2*ppoint)-prevlow
##        s1 = 2*ppoint)-prevlow
##        what is the closest it has been since the last sig, what is the slope [danger of rollover?]
##        how did it behave the last time it got  a near brush
##        how did it behave the last time it was close to a line...
##        manually insert the lines and then add line logic....

##        near cross is a bounce and is cross with flat slope and the next bar is a crossback!

      
'''
