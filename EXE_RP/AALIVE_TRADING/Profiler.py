import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE_RP'
sys.path[0:0] = [rootpath + 'EXE_RP']
#########################################
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
####################
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time
from datetime import datetime
from time import sleep
import  rpu_rp, rpInd, TicksUtile,BarUtiles
import ctypes
######today = yesterday
date = today
#####################3
import RP_Snapshot
print '   '
sym = 'ES'      
start = '15:30:00'
start = '09:30:00'
end   = '23:58:05'
barsdaily =[]
bars = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
blines = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(DataDown +'20151105.ES.1day.both.csv'),3000)
for l in blines:
##    print l
    if len(l) > 2 :
        barsdaily.append(l)
##bars = barsdaily
##roundfactor = -1
##incr = 5.0
roundfactor = 2
incr = 0.25 #5.0 #0.25
barid =0
farray =[]
lastbar = len(bars)
for bar in bars:
    barid = barid +1
    if barid > (lastbar -3):
        print bar
    highraw = float(bar[3])
    high = round(highraw,roundfactor)
    lowraw = float(bar[4])
    low = round(lowraw,roundfactor)
    volumeraw = bar[6]
    bartime = bar[1]
##    print bartime,low,high
    pricerange = float(high)-float(low)
##    print pricerange
    prevpnew = low
    pnew = low
    while pnew <= high:
        linearray =[]
        pnew = prevpnew + incr
##        print pnew,barid
        prevpnew = float(pnew)
        linearray.append(pnew)
        linearray.append(barid)
        linearray.append(volumeraw)
        farray.append(linearray)
plist =[]
varray =[]
for p in farray:
    plist.append(p[0])
pricelist = rpu_rp.uniq(plist)
for price in pricelist:
    vlarray=[]
    vlarray.append(price)
    volumer = ''
    totalhits =0
    totalvolume =0
    for l in farray:        
        if l[0] == price:
            mark = l[1]
            mark = '1'
            if len(l) > 1:
                volumer = str(l[2]).replace(' ','')
                if volumer == 'full':
                    volumer = '100'
                totalhits+=1
                volume = int(volumer)
                totalvolume +=volume
##            vlarray.append(mark)
    multiplier = totalhits
    multiplier = totalvolume / 10000
    vlarray.append(multiplier)
##            print l[1]
    varray.append(vlarray)
for p in  varray:
    print p[0],p[1]*'l'
        ## check if line price has been tagged


def find_swing_points(sym,barsize,start,end):
    arrayin = [['ES', ' 2015-10-20 22:58:05',2019.5,2020.25,2019.5,2019.75,'full','60'],['ES', ' 2015-10-20 22:58:05',2019.5,2020.25,2019.5,2019.75,'full','60']]
    bs = strip1float(arrayin,5,sym) ##raw close price
    symES = 'ES'
##    date =  rpu_rp.todaysdateunix()  ##
    EsFile = rpu_rp.CsvToLines( DataDown+ date + '.'+symES+'.' + dur.replace(' ','') + '.both.csv')
    DurBothBoostedES = boost_pricearray(EsFile,symES)
    bsES = strip1float(DurBothBoostedES,5,'ES')
##    print sym,dur,Indtitle
    bsopen = strip1float(arrayin,2,sym) ##raw open price
    bshighs = strip1float(arrayin,3,sym)
    bslows = strip1float(arrayin,4,sym)
    bsbardiff = difftwoarrays(bs,bsopen)
    barrange = difftwoarrays(bshighs,bslows)
    timestamparray = strip1string(arrayin,1)
    stochval = 14
    stochval2 = 3
    rvival = 4
    rvival2 = 10
    comparebs = rpu_rp.tail_array_to_array(bs,100)
    compareES = rpu_rp.tail_array_to_array(bsES,100)
    comparetimes = rpu_rp.tail_array_to_array(timestamparray,100)
    bars = get_bars(today,sym,barsize,start,end)
##    for bar in bars:
##        if barhigh > previous 3 bars highs and
##        barhigh > 3 bars later, thatisa swing
##        price now = bar[c-3]
##        is price now greater than bar[c]? flag = stillhigh
##        is price greater than bar[c-4] and bar[c-5]
##        bar
#################################                
'''##########################                
######detect_sliceDice(lineprice,start,end)
first pass did not bounce 4 ticks, went 6 ticks [noise] beyond before bounce or retag

bar low v kupper, barhi vs klower, barage, older the worse? what is max?
##########raw_input('click')
####thrust and slope of current bar
## averages of:
# of sigs per period
# average distance between
is it a cross or a bounce....one touch and threw...1st pass, 2nd pass, thru
identify wedges...50/50 chance

stop distances...3x for bigger moves
grab trade data from action forex
use action forex for wide lines 4hour
def create_report(Sigfile,sym,barsize):
    print barsize,sym,'number bars studied=',numberBars,numsigs,'=numsigs'
    print 'if i am 20 bars old in signal, start with trail stop depends on dur...shotrt dur = short age'
##    average number of sigs in 30 bars  has it flipped alot
##    test the ticker perfomance by time delta
##    avg number of ticks should be cycle time...if not issue a warning
##    avg number of bars per hour should match duration/hour
#########
'''
