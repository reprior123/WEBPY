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
date = yesterday
#####################3
##########    pivot = rpInd.gatherline(sym,'pivot')
##########    R1 = rpInd.gatherline(sym,'R1')
##########    S1 = rpInd.gatherline(sym,'S1')
##########    print S1,R1,pivot
    ##do the same for weekly by adding dur to variables and create a weekly  from dailys..
##    find pivots, find fibbo retraces on recnt moves[rangebars,hi,lo]
##    read spots from file
##    calculate two roundies
##    calculate 10 handles off high of day,lowday,openday,yestclose,prevhourhilow
#############################################
##########################
import RP_Snapshot
print '   '
 
###############
def create_roundies(sym):
    curprice = 2100 #need to read froma bar ranger
##    take curr price
##    factor = price / 100
##    using factor, calculate 3 roundies up and 3 down
##    write them to roundie file
##    create combined lines file with adding lines to roundies
####################
tag_listall = tagsdict.values()
tag_list = []
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
def get_info(date):
    todayhyphen = rpu_rp.todaysdatehypens(date)
##    RP_Snapshot.snapshot_sym(sym,date,['5mins']) ## need this to create good both bars ## 
    btime = '15:30:0'
    RP_Snapshot.show_one_bar('ES','1min',btime,date)
    ###############
    ############
    regionlist = ['USA','EUROPE','ASIA']
    for r in regionlist:
        for tag in tag_list:
            ctag = r+tag
            startbartime = tagsstartdict[ctag]
            endbartime = tagsenddict[ctag]
##            print r,tag,ctag,startbartime,endbartime
            rangehilos = BarUtiles.show_hi_lo_bar_range(sym,'5mins',startbartime,endbartime,date)
            LOW = rangehilos[0]
            HIGH = rangehilos[1]
            HIGHTIME = rangehilos[3].replace(bla,'')
            LOWTIME = rangehilos[2].replace(bla,'')
            CLOSE = rangehilos[4]
            OPEN = rangehilos[6] ## closetime is in 5
            print('%8s %8s %8s %8s %8s %8s %8s %8s %8s %8s' % (r,tag,LOW,HIGH,CLOSE,LOWTIME,HIGHTIME,startbartime,endbartime,OPEN))
#####################
######################
def scan_bars_for_tag(bars,price,sym,start,end,date):
    bars = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    for bar in bars:
        print bar
        ## check if line price has been tagged
#############################
def detect_sliceDice(lineprice,start,end):
    bars = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)

    startprice = float(head(bars)[6])
    if startprice <  lineprice :
        position = 'below'
        pass
    else:
        position = 'above'
        pass
    sflag = 'untagged'
    for bar in bars:
        currprice = bar[6]
        if position == 'below':
            if currprice > lineprice:
                sflag='firsttag'
                pass
            if sflag == 'firsttag':
                pass
######################
def OBV(date,sym):
##    bars = RP_Snapshot.show_bar_range(sym,'5mins',start,end,date)
    ticks = bars
######bs = [1,2,6,6,5,6,7,8,9]
######bshighs = [1,2,13,4,5,6,7,8,9]
######bslows = [1,2,3,4,5,5,5,5,5]
######
######scanvalue = 3
######stochval2 = 3            
######def StochD(Kpercarray,emaval):
######    Dpercarray =  EMAmvavgToArray(Kpercarray,emaval)
######    return Dpercarray
#################################
###################################
###################################  
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
############
####def slice_dice_dectector(sym,date,starttime,endtime,spotline,direction):
####    for bar in rangebars:
####if direction == 'up':
#### firsttouch = if spotline is breached...5sec bar is lowhigh on spot
####    tagstatus = 'touched'
####    if tagstatus =='touched, look for next touch...withing
###   after first touch, should move back minimum 1 point...BEFORE moving 2.75 handleif spotlineStatus1tou
####################
def linetagger(spotline,sym):
    print spotline, 'checking if tagged in last 5 minutes'
    ## am i under or over line at start of 5 mins?...under
    ##diff to spotline = spotline - recentprice
    ## if diff < 0:  then status = tagged print status, spotline, curprice
    ## followthru amount ?
#########################
'''
#################################
def show_spots(sym,date,limit):
    curprice = float(TicksUtile.recenttick(sym,'recent'))
    spotfile = libarea + 'spotlines.' + sym+ '.csv'
    spotlines= rpu_rp.CsvToLines(spotfile)
    print limit, ' is limit'
    for l in spotlines:
        spotp = float(l[0])
        distance = abs(spotp-curprice)
        if (spotp-curprice) > 0:
            underover = 'under'
        else:
            underover = 'over'
        if distance < limit:
##            print curprice-spotp,spotp,curprice,sym,'spot prices',limit
            if underover == 'under':
                print 'ready to SELL at ',spotp, 'how manypasses?',curprice,sym,distance
            else:
                print 'ready TO BUY at ',spotp, 'how manypasses?',curprice,sym,distance
#####################
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
def getslices(sym,barsize,start,end,date,slicesize):
    import RP_Snapshot
    bars = RP_Snapshot.show_bar_range(sym,barsize,start,end,date)
    lenbars =len(bars)
    c=0
    while c < (lenbars - slicesize +1 ):
        slicebars = bars[c:c+slicesize]
        mode= 'CLOSEPRICE '
        find_swing_pointsnew(slicesize,slicebars,mode)
        c+=1
#########    
def find_swing_pointsnew(slicesize,slicebars,mode):
##    print len(slicebars)
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
    print '===='
    for bar in slicebars:
##        print bar
        ##first, locate the hi lo
        barhigh = float(bar[highnum])
        barlow = float(bar[lownum])
##        print barhigh,barlow
        if barhigh > slicehi:
            slicehi = barhigh
            barhinum = c
        if barlow < slicelow:
            slicelow = barlow
            barlownum = c
        c+=1
    ## now we have slicehi          
    ##make sure slice is not an endbar
    barhi = slicebars[barhinum]
    barlow = slicebars[barlownum]
    bar1 = slicebars[0]
    barlast = slicebars[slicesize-1]
    bar1high = float(bar1[highnum])
    barlasthigh = float(barlast[highnum])
    bar1low = float(bar1[lownum])
    barlastlow = float(barlast[lownum])

    tag = 'noswing'
##    print slicehi,slicelow,bar1[highnum],barlast[highnum] 
    if bar1high != slicehi and barlasthigh != slicehi:
        tag = 'swinghi'
        activebar =barhi
    if bar1low != slicelow and barlastlow != slicelow:
        tag ='swinglo'
        activebar = barlow
    if tag != 'noswing':
        print tag,activebar
##################################       
factor = 10
proximitylimit = 9.0
sym = 'ES'
##run_8s(sym)
##show_spots(sym,date,proximitylimit)
barsize = '15mins'
##barsize = '5mins'
##barsize = '1min'
##barsize = '1hour'     
start = '01:00:05'
end   = '20:58:05'
slicesize = 5
getslices(sym,barsize,start,end,date,slicesize)
##find_swing_points(sym,barsize,start,end)
######print 'low high close lowtime,hitime,startrange,endrange'
######get_info(date)

''' boll bands calculation
SMAval = 20
    SMAprice = price at SMAval
    Stdvariable = 0.382
    SMA H23 =AVERAGE(F4:F23)
    Upper Bollinger Band I23 = SMAprice + (std*Stdvariable)
    Lower Bollinger Band J23 = SMAprice - (std *Stdvariable)
    1. Work out the Mean (the simple average of the numbers)
2. Then for each number: subtract the Mean and square the result
3. Then work out the mean of those squared differences.
4. Take the square root of that and we are done!
The formula actually says all of that, and I will show you how.
mean = simpleaverage  of slice array at 20
diffmean = take each value - mean
sqdiffmean = diffmean *diffmean
meansqdiff = meanof sqdiffmeans
sqroot of meanssqdiffs
'''


