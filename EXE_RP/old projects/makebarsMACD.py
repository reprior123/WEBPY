# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_ACTANT/'
localtag = '_ACTANT'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles, rpu_rp
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
todayf = 'AQTOR_20150408_1.log'
todayf = 'bla'
##def grep_to_txtfile(infilename,greppattern,outfilename,fieldnum):
#######################################################
for f in  os.listdir(ActantDataNoSlash):   
    print f
##fblaw = raw_input('enter filename here:  ')
##rpu_rp.WriteStringsToFileAppend(ActantData + f,f)
##array = rpu_rp.grep_txtfile_to_array(ActantData + todayf,'Scr')
lines = rpu_rp.TxtToLines(ActantData + todayf)

barsize = 3
bartime = 6000

barhi = 0
barlo = 99999999
tickcount = tottickcount = 0
bararray =[]
prevtime = 0
timestart = 0

for line in lines:
    if '6E' in str(line):
        tickcount +=1
        tottickcount +=1   
        ##reset ticknum
        time = line.split()[1]
        hour = time[0:2]
        minute = time[2:4]
        second = time[4:6]
        secondstot = (int(hour) * 3600) + (int(minute) * 60) + (int(second)* 1)
        timediff = secondstot - timestart
    ##    print time,hour,minute,second,(int(hour) * 360),(int(minute) * 60),second  
        price = int(line.split(';')[3])
        prod =line.split(';')[1]    
        if price > barhi:
            barhi = price
        if price < barlo:
            barlo = price
        if tickcount == 1:
            baropen = price
        if tickcount == barsize or timediff > bartime :  ### reset the bar here
            timestart = secondstot
            elapsed = secondstot - prevtime
            barline =[]
            barclose = price
            midhilo = (barhi+barlo)/2
    ##        print barhi, barlo,baropen,barclose,time,secondstot,barsize,tickcount
            barline.append(time)
            barline.append(barhi)
            barline.append(barlo)
            barline.append(baropen)
            barline.append(barclose)
    ##        barline.append(time)
            barline.append(secondstot)
            barline.append(barsize)
            barline.append(tickcount)
            barline.append(elapsed)
            barline.append(midhilo)
           
            bararray.append(barline)
            tickcount=0
            barhi = 0
            barlo = 99999999
            prevtime = secondstot
            
##print bararray
prevhi =  prevlo = 0

#### flip the bar lines around in reverse sort
bs = []
for l in sorted(bararray,reverse=True):
##    print l
    midhilo = l[9]
    bs.append(l[9])
###############
#### run the bs bars through the macd routine
barnum = 0
smaNum = 26
numbars = len(bs)-smaNum
proper =[]
while barnum < numbars:
    c = 0  
    avgsum = 0
    while c < smaNum:
        avgsum += bs[c+barnum]
        diff=  bs[c]- bs[c-1]
        c +=1
    sma26 = avgsum/smaNum
    avgsum =0
    barnum +=1
    ##############
    smaNum = 12
    c = 0  
    avgsum = 0
    while c < smaNum:
        avgsum += bs[c+barnum]
##        print avgsum
        diff=  bs[c]- bs[c-1]
        c +=1
    sma12 = avgsum/smaNum
##    print barnum,sma5,sma34,sma5-sma34
    proper.append(sma12-sma26)
    avgsum =0
    barnum +=1
print len(proper)
print proper
#######################
################################
###########################
### mv avg of proper
##for lp in sorted(proper,reverse=True):
##    print lp
##    midhilo = lp[0]
##    print midhilo
##    proper.append(lp[0])
###############
##proper = []
barnum = 0
smaNum = 9
numbars = len(proper)-smaNum
signalseries =[]
while barnum < numbars:
    c = 0  
    avgsum = 0
    while c < smaNum:
        avgsum += proper[c+barnum]
        diff=  proper[c]- proper[c-1]
        c +=1
    sma9 = avgsum/smaNum
##    print barnum,sma9
    signalseries.append(sma9)
    diverg = sma9-proper[c]
    print diverg,barnum,sma9
    avgsum =0
    barnum +=1
    ##############

##print signalseries
##print proper
## need the diff between the twol.
    
##    print item ## these values now  need a moving average of 9 bars on them to become the signal
    ### then match the proper and average series and divergence value is proper - average
    
##AO =   5sma[mids]
##150408 151646552 F4C ScrNfo  6E      ;6E.JUN15; forced by timed midpoints mid = ;108665;
##150408 151656162 F4C ScrNfo  6E      ;6E.JUN15; forced by timed midpoints mid = ;108655;
