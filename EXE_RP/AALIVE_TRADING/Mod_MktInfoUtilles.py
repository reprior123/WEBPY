# -*- coding: cp1252 -*-
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
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from datetime import datetime
import ctypes
######################
date =   yesterday # today
############
####list of modules in here to give mkt info:
####get_info  -  get all critical levels on todays trade
###################
def notsure():
    tag_listall = tagsdict.values()
    tag_list = []
    print tag_listall
    for a in tag_listall:
        f = 'absent'
        c=0
        while c < len(tag_list):
            if a == tag_list[c]:
                f = 'found'
            c+=1
        if f == 'absent':
            tag_list.append(a)
    ##tag_list = ['RTH','LastHour']
    print todaydash
    bla =str(todaydash)
notsure()
########################
def get_info(date):
    print 'DAILY PIVOT = 2000.2   |  WEEKLY = 2046.6'
    todayhyphen = rpu_rp.todaysdatehypens(date)
##    RP_Snapshot.snapshot_sym(sym,date,['5mins']) ## need this to create good both bars ## 
    btime = '15:30:0'
    RP_Snapshot.show_one_bar('ES','1min',btime,date)
    ###############
    regionlist = ['USA','EUROPE','ASIA']
    for r in regionlist:
        finfostring = '%9s %9s %9s %9s %9s %9s %9s %9s %9s %9s'
        aheader = ['r','tag','LOW','HIGH','CLOSE','LOWTIME','HIGHTIME','startbt','endb','OPEN']
##        print ', '.join(aheader)
        print (finfostring % ('r','tag','LOW','HIGH','CLOSE','LOWTIME','HIGHTIME','startbt','endb','OPEN'))
##        print (finfostring % (str(aheader).strip('[]')))
##        ', '.join(mylist)        
        for tag in tag_list:
            ctag = r+tag
            startbartime = tagsstartdict[ctag]
            endbartime = tagsenddict[ctag]
##            print r,tag,ctag,startbartime,endbartime #test
            rangehilos = BarUtiles.show_hi_lo_bar_range(sym,'5mins',startbartime,endbartime,date)
            print rangehilos
            LOW = rangehilos[0]
            HIGH = rangehilos[1]
            HIGHTIME = (rangehilos[3].replace(bla,'')).replace(' ','')
            LOWTIME = (rangehilos[2].replace(bla,'')).replace(' ','')
            CLOSE = rangehilos[4]
            OPEN = rangehilos[6] ## closetime is in 5
            CLOSETIME = rangehilos[5] ## closetime is in 5
            print(finfostring % (r,tag,LOW,HIGH,CLOSE,LOWTIME,HIGHTIME,startbartime,endbartime,OPEN))
#####################
def scan_bars_for_tag(bars,price,sym,start,end,date):
    bars = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    for bar in bars:
        print bar
        ## check if line price has been tagged
#############################
def detect_sliceDice(lineprice,start,end,ndate):
    sym = 'ES'
    line = float(lineprice)
    bars = RP_Snapshot.show_bar_range(sym,'1min',start,end,ndate)
    topline = bars[0]
    print topline
    tolamt = 0
    startprice = float(topline[5])
    sflag = 'move1'
    move1low =  move2low =  99999
    move1high = move2high = 0
    move1diff = move2diff = 0
    if startprice <  float(lineprice) :
        start1position = 'belowline'
        c1pricenum = 3 #highs
        c2pricenum = 4 #low
        c3pricenum = 3 #highs
        sign = 1
    else :
        start1position = 'aboveline'
        c1pricenum = 4 #lows
        c2pricenum = 3 #highs
        c3pricenum = 4 #lows
        sign = -1
        
    for bar in bars:
        if startprice <  float(lineprice) :
            start1position = 'belowline'
            move1cprice = move1high
            move2cprice = move2high
        else:
            start1position = 'aboveline'
            move1cprice = move1low * (-1)
            move2cprice = move2low * (-1)
        
        currprice = float(bar[5])
        currlow = float(bar[4])
        currhigh = float(bar[3])
        currtime = bar[1]
        c1price = float(bar[c1pricenum])
        c1diff = c1price - line * sign
        
        c2price = float(bar[c2pricenum])
        c2diff = c2price - line * sign

        c3price = float(bar[c3pricenum])
        c3diff = c3price - line * sign
        
        fade1minimum = -1
        toleranceretag = 2.75
##        print sflag,c1diff, c1price, c2diff,c2price,c3diff,c3price
        if sflag == 'move1' and c1diff >= 0:
            sflag='move1done'
            print 'tagged1', line,bar
        if sflag == 'move1done' and c2diff <= fade1minimum:
            sflag='move2done'
            print 'tagged2',line,bar
        if sflag == 'move2done' and c3diff >= toleranceretag:
            sflag='move3done'
            print 'noslice',line,bar
        if sflag == 'move3done':
            pass
        print ('%9s %10s  %4.2f %4.2f %4.2f %s' %(sflag,start1position,c2diff,c3diff,currprice, currtime))

##            print 'noslicedice', bar
'''
Firstpass and SLICE AND DICE - the very first time rejects the direction of the move and
takes price 1 handle minimum away from the SPOT If this does not occur and
price moves to 2.75 handles isSLICED AND DICED.Most SLICED AND DICED SPOTS are recovered on the same day 
BACK THROUGH AND PERMISSION TO LEAVE -Once price goes through a SPOT it often returns one more time within exact SPOT
to .75 from SPOT and then resumes the directional move this is the PERMISSION TO
LEAVE BAR, a successful TEST of the SPOT.can use range hi and lows for  showing swings and linefades and compression ranges....
first pass did not bounce 4 ticks, went 6 ticks [noise] beyond before bounce or retag
'''
######################
def show_bar8_range(start,end,sym,date):
    print 'this is the bar8 range of lines',start,end
    after5lines = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    linecount =0
    trigger = 'inactive'
    for line in after5lines:
        bartime = line[1]
        linecount +=1
##        print line
        if linecount ==1:
            starthi = line[3]
            startlo = line[4]
            print '>>>> BAR 8 HILO = <<<<<', starthi, startlo, bartime
            pass
        curbarhi = line[3]
        curbarlo = line[4]
        if curbarhi < startlo and trigger != 'active':
            print 'going down',line
            trigger = 'active'
        elif curbarlo > starthi and trigger != 'active':
            print 'going up',line
            trigger = 'active'
        else:
            pass
    print '======================'
##############################
def run_8s(sym): 
    if sym == 'ES' and 'bla' == 'bla':
##        show_bar8_range('04:00:00','7:00:00',sym,date) #asia
        show_bar8_range('09:30:00','12:25:00',sym,date) #europe
        show_bar8_range('16:00:10','18:25:00',sym,date) #usa
###############################
def getonesliceonly(bars,slicesize,slicenum):
    oneslice = bars[slicenum:slicenum+slicesize]
    return oneslice
#########    
def find_swing_point_in_oneslice(slicesize,slicebars,mode):
    if mode == 'CLOSEPRICE ':
        highnum = 5
        lownum = 5
        pass
    else:
        highnum = 3
        lownum = 4
    c=0
    barnum =0
    slicehi = 0
    slicelow = 99999
    barlownum = barhinum = 0
    for bar in slicebars:
        ##first, locate the hi lo
        barhigh = float(bar[highnum])
        barlow = float(bar[lownum])
        if barhigh > slicehi:
            slicehi = barhigh
            barhinum = c
        if barlow < slicelow:
            slicelow = barlow
            barlownum = c
        c+=1
    ## now we have slicehi          
    ##make sure slice is not an endbar
    arrayfinal =[]
    activebar = []
    barhi = slicebars[barhinum]
    barlow = slicebars[barlownum]
    bar1 = slicebars[0]
    barlast = slicebars[slicesize-1]
    bar1high = float(bar1[highnum])
    barlasthigh = float(barlast[highnum])
    bar1low = float(bar1[lownum])
    barlastlow = float(barlast[lownum])
    ## start tagging the bars
    tag = 'noswing'
##    print slicehi,slicelow,bar1[highnum],barlast[highnum] 
    if bar1high != slicehi and barlasthigh != slicehi:
        tag = 'swinghi'
        activebar = barhi
        swingpr = slicehi
    if bar1low != slicelow and barlastlow != slicelow:
        tag ='swinglo'
        activebar = barlow
        swingpr = slicelow
    if tag != 'noswing':
        timenow = activebar[1]
##        print activebar
        oneline =[timenow,tag,swingpr]
    else:
        oneline= ['notime','notaswing',9999.0]
    return oneline
##################################       
factor = 10
sym = 'ES'
run_8s(sym)
barsize = '5mins'##barsize = '1hour'     
start = '00:00:05'
end   = '22:58:05'
########getslices(sym,barsize,start,end,date,slicesize)
lineprice = 2011.50 #2068.50
##detect_sliceDice(lineprice,start,end,date)
print 'low high close lowtime,hitime,startrange,endrange'
##########get_info(date)
##raw_input()
def find_swings(): # this runs through the series of slices
    bars = RP_Snapshot.show_bar_range(sym,barsize,start,end,date)
    lenbars =len(bars)
    slicesize = 5  
    #####
    c=0
    climit =(lenbars - slicesize + 1 )##    climit = 40
    while c < climit:
        slicenum = c
        oneslice = getonesliceonly(bars,slicesize,slicenum)
        mode= 'CLOSEPRICE '
        bla = find_swing_point_in_oneslice(slicesize,oneslice,mode)
        if len(bla) > 0:
            print c, bla
        c+=1    
##find_swings()
raw_input('ccc')
