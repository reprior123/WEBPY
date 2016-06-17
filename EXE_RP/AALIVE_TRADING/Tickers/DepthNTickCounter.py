import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
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
#################### 
##today = yesterday
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
##from datetime import datetime
import ctypes 
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
#############################
symbol_list = symdict.keys()
symbol_list =['ES']
print today
########################################
def show_avg(arrayin):   
    c=0
    tot=0
    while c < len(arrayin):
        tot+=arrayin[c]
        c+=1
    avg = tot/len(arrayin)
    return avg
###############
def show_2_arrays(array1,array2,sortorder):
    if sortorder == 'r':
        c=len(array1)-1
        incrvalue = -1
    else:
        c=0
        incrvalue = 1
    for l in array1:
        print ('%8.2f x %d' % (array1[c],array2[c]))
        c+=incrvalue
#####################
def show_2_arrays_bigsize(array1,array2,sortorder,perclimit):
    avgarray1 = show_avg(array2)
    dfactor =10
##    print avgarray1, ' = avg'
    if sortorder == 'r':
        c=len(array1)-1
        incrvalue = -1
    else:
        c=0
        incrvalue = 1
    for l in array1:
        size = array2[c]
        price = array1[c]
##        print ('%8.2f x %d' % (price,size))
        if size > (perclimit* avgarray1):
##            print size
            print ('%8.2f x %d  <<<<' % (price,size/dfactor))
        else:
            print ('%8.2f x %d' % (price,size/dfactor))
        c+=incrvalue
    return int(avgarray1)
#####################
def sum_array(array,mode,rows):
    c=0
    suma =0
    if mode == 'all':
        rows = len(array)
    while c < rows:
        suma+=int(array[c])
        c+=1
    return suma
#######
def sum_2arrays_weighted(array,array2,mode):
    c=0
    suma =0
    while c < len(array):
        suma+=float(array[c])*1#float(array2[c])
        c+=1
        if mode == 'toponly':
            suma = int(array[0])
        else:
            pass
    return suma/c
#############
def prepare_empty_array(fnums):
    c=0
    arrayout = []
    while c < fnums:
        arrayout.append(0)
        c+=1
    return arrayout
###########################
def presort(sym,style):
    larray=[]
    filein = DataDown +today+'.'+sym+ '.RTMktDepth.csv'
    if style == 'dom':
        for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),1000):
            if 'updateMktDepth' in str(line):
##                print line
                larray.append(line)
    return larray
####################    
def checkDOMticks(sym,fnums,arrayinlines):
    filein = DataDown +today+'.'+sym+ '.RTMktDepth.csv'
    buylineprice = prepare_empty_array(fnums)
    buylinesize = prepare_empty_array(fnums)
    selllineprice = prepare_empty_array(fnums)
    selllinesize =  prepare_empty_array(fnums)
    prevtotdiff = 0
    divfactor = 1
    for line in arrayinlines: #rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),1000):
        position = int(line[1].replace('position=','').replace('>','').replace(' ',''))
        size = round((float(line[5].replace('size=','').replace('>','').replace(' ',''))),0)
        operation = line[2].replace('operation=','').replace('>','').replace(' ','')
        price = float(line[4].replace('price=','').replace('>','').replace(' ',''))
        time = line[6].replace(' ','')
        zflag = 'clean'
        if price == 0 or size == 0:
##            print 'zeros'
            zflag = 'haszeros'
        if 'side=1' in str(line):
            buylineprice[position] = price
            buylinesize[position] = size
            buylinesizewtd = buylineprice[position] * buylinesize[position]
        else:
            selllineprice[position] = price
            selllinesize[position] = size       
    ##        return buylineprice, buylinesize,selllineprice,selllinesize,timenow
##    sizeweightedbid = sum_2arrays_weighted(buylineprice,buylinesize,'bla')
##    sizeweightedsell = sum_2arrays_weighted(selllineprice,selllinesize,'bla')
    totalbuy = float(sum_array(buylinesize,'all',88))
    totalsell = float(sum_array(selllinesize,'all',88) )    
    totdiff = totalbuy - totalsell
    totalratio = totalbuy/totalsell
    topbuy = float(sum_array(buylinesize,'toponly',1))
    topsell = float(sum_array(selllinesize,'toponly',1))     
    topdiff = topbuy - topsell
    topratio = topbuy/(topsell +.00001)
    if totdiff == 0:
        totdiff = 1
    if totalbuy > 0:
        totdiffperc = 100 * (round(float(totdiff/(totalsell +totalbuy)),3))
    else:
        totdiffperc  = 0.0
        ############
    if topdiff == 0:
        topdiff = 1
    if topbuy > 0:
        topdiffperc = 100 * (round(float(topdiff/(topsell +topbuy)),3))
    else:
        topdiffperc  = 0.0
##        print totdiffperc, totdiff, totalbuy
    difftoprev = totdiff - prevtotdiff
    prevtotdiff = totdiff
    buytopprice = buylineprice[0]
    selltopprice = selllineprice[0]
##    print 'SELL', selllinesize, totalsell, totdiff
    showflag = 'no'
    if abs(totalratio) > 1.20 or totalratio < .95 :
        showflag = 'show'
    if abs(difftoprev) > 2000000:
        showflag ='show'
    if  abs(topdiffperc)> 20000 :
        showflag = 'show'
    if showflag == 'show' :
##            print buytopprice,'BUY', buylinesize, totalbuy, totdiff, totalsell, selllinesize, 'SELL',selltopprice,time,difftoprev,str(totdiffperc)
##        print 'tot',totalbuy,'x',totalsell, totdiff, str(totdiffperc),'%', difftoprev
        print 'topBOOK>>',topbuy,'x',topsell, 'Topbuy ratio =',round(topbuy/(topsell+1),2), 'Totalbook Ratio >>>',round(totalratio,2)
##        print time,'B', buylinesize,  selllinesize, 'S',buytopprice,selltopprice
    print "\n" * 50
##    print selllineprice
##    print selllinesize
    avgsells = show_2_arrays_bigsize(selllineprice,selllinesize,'r',1.5)
    print '-----'
    avgbuys = show_2_arrays_bigsize(buylineprice,buylinesize,'n',1.5)
    print 'WHOLE BOOK'
##    print ('%4d x %4d = %4d | %4.1f' % (totalbuy, totalsell, totdiff, totalratio))
    print ('%4d x %4d = %4d | %4.1f' % (totalbuy/divfactor, totalsell/divfactor, totdiff/divfactor, totalratio))
    print 'TOPBOOK'
    print ('%4d x %4d = %4d | %4.1f' % (topbuy/divfactor, topsell/divfactor, topdiff/divfactor, topratio))
    print ('avg %4d x %4d' % (avgbuys,avgsells))
#####################
fullarray =[]
def checkRTnonbarticksNEW(sym,fnums):
    fullarray =[]
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv.new'
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv'
    prevtotdiff = ask = bid =0
    prevtime =''
    string =''
    prevtradeuid=''
    time = ''
    size = ''
    tprice = 0.0
    tsize = singletrade = totdaysize= vwap =''
    totdowns = totups = 0
    tottickups=0
    nettickhits = 0
    lastsize = lastprice = bidsize = asksize =  0
    prevtick = nettickups = totHits = totLifts = 0

    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),4000):
##        print line
        if 'tickString' in str(line) and 'tickType=48' in str(line):
            time = line[3]
            string = line[2].split(';')
            if len(string) > 2:
                tprice = float(string[0].replace('value=',''))
                tsize = float(string[1])
                singletrade = string[5]
                totdaysize = string[3]
                vwaps  = string[4]
                if len(vwaps) > 0:
                    vwap  = round(float(string[4]),2)
                else:
                    vwap =0.0
##            value=1984.50;1;1441796865858;207069;1982.49963539;true>
##            print tsize,tprice,time,'trade', bid, ask, bidsize, asksize
        if 'tickSize' in str(line):
##            0 BID_SIZE tickSize()
##            1 BID_PRICE tickPrice()
##            2 ASK_PRICE tickPrice()
##            3 ASK_SIZE tickSize()
##            4 LAST_PRICE tickPrice()
##            5 LAST_SIZE tickSize()
            fs = line[1].replace(' field=','')
            sizetime = line[3]
            value = int((line[2].replace(' size=','')).replace('>',''))
            size = value
########            print sizetime,size,fs,'size'
            if fs == '0':
                bidsize = value
            elif fs == '3':
                asksize = value
            elif fs =='5':
                lastsize = value
            else:
                pass
        if 'tickPrice' in str(line):
            pricetime = line[4]
            value = float(line[2].replace(' price=',''))
            fp = line[1].replace(' field=','')
            if fp == '1':
                bid= value
                pass
            elif fp == '2':
                ask = value
            else:
                lastprice = value
##            if bid == 0.0:
        tradeuid = time + str(tsize) + str(tprice)
        if 'tickString' in str(line) and len(string) > 2 and bid > 0 and ask > 0 and tradeuid != prevtradeuid:
            if tprice > prevtick:
                tickdir='uptick'
            elif tprice < prevtick:
                tickdir = 'downtick'
            else:
                tickdir = 'neutral'              
            if bid == tprice:
                tickflag = 'HitBid'           
            else:
                tickflag = 'LiftOffer'          
            aout =[]
            prevtick = tprice
            if tsize > 0 and time != 'xxx':
                aout.append(tickflag)
                aout.append(tickdir)
                aout.append(tprice)
                aout.append(tsize)
                aout.append(bid)
                aout.append(ask)
                aout.append(time)
##                print aout
                fullarray.append(aout)  ### how many upticks in a row?
                prevtime = time
                prevtradeuid = tradeuid
##            print fullarray
    c=0
    x = len(fullarray)
##    print x
    limiter  = min(int(x *.90),10)
    f = limiter
##    print f
    netlifts = netticks = 0
    lifthitscore = 0
##    print 'netlifts','   netUPticks    liftscore'
    for l in fullarray:
##        print l
##        ['LiftOffer', 'uptick', 1995.5, 2.0, 1995.25, 1995.5, '15:49:02.881000']
##        ['HitBid', 'neutral', 1995.5, 50.0, 1995.5, 1995.75, '15:49:02.894000']
        c+=1
        if c > f:
##            print l
            tprice = l[2]
            lifttag=l[0]
            tsize = l[3]
            ticktag=l[1]
            if lifttag == 'HitBid':
                netlifts = netlifts -1
                lifthitscore += (tsize * (-1))
                pass
            else:
                netlifts +=1
                lifthitscore += (tsize * (1))
            if ticktag == 'downtick':
                netticks = netticks -1
                pass
            elif ticktag == 'uptick':
                netticks +=1
            else:
                pass        
            if c > (x - 8):
                pass
                print l
    print ('%4d  %4d | %4d %4.1f  %s netlifts   netUPticks    liftscore' % (netticks, lifthitscore, x, limiter,tprice))
###############################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
def createVolHistogram(sym,fnums):
##    fullarray =[]
##    today = '20151013'
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv'
    prevtotdiff = ask = bid =0
    string =''
    time = ''
    size = ''
    tprice = 0.0
    tsize = singletrade = totdaysize= vwap =''
    totdowns = totups = 0
    tottickups=0
    pricearrayraw =[]
    pnsize =[]
    lastsize = lastprice = bidsize = asksize =  9999
    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),4440000):
        if 'tickString' in str(line) and 'tickType=48' in str(line):
            pnsizeline =[]
##            print line
            time = line[3]
            string = line[2].split(';')
            if len(string) > 2:
##                print string
                tprice = float(string[0].replace('value=',''))
                tsize = float(string[1])
                singletrade = string[5]
                totdaysize = string[3]
                vwaps  = string[4]
                if len(vwaps) > 0:
                    vwap  = round(float(string[4]),2)
                else:
                    vwap =0.0
##            value=1984.50;1;1441796865858;207069;1982.49963539;true>
##            print tsize,tprice,time,'trade', bid, ask, bidsize, asksize
            pricearrayraw.append(tprice)
            pnsizeline.append(tprice)
            pnsizeline.append(tsize)
            pnsize.append(pnsizeline)

    uarray = rpu_rp.uniqArray(pricearrayraw)
    ldiv = 100
    print "\n" * 50
    strings =''
    for price in uarray:
        lvol =0.0
        for l in pnsize:
            if price == l[0]:
                lvol += l[1]
        if lvol > 6 :
##            print ('avg %6.2f ... %4d .. %s' % (price,lvol,int(lvol/ldiv)*'l'))
            strings +=  ('avg %6.2f ... %4d .. %s\n' % (price,lvol,int(lvol/ldiv)*'l'))
    print strings
    Mbox('b', strings, '')
##########################################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
#############################
###############################         
threshold = 0.0
loopmax = 1000
loop = 0
sleeptime = 1
while loop < loopmax:
    sym = 'ES'
##    print '====='
    
##    createVolHistogram(sym,1)
##    sleep(3)
##    print '>>>>>'
    lines = presort(sym,'dom')
##    checkDOMticks(sym,10,lines)
    checkRTnonbarticksNEW(sym,1)
    sleep(sleeptime)
    
    loop+=1
'''
checkRTnonbarticksNEW(sym,fnums)
another array with price gaps...then the top gap as in width between bidoffer
scenariios....
bidHitNfad...count how often
offerliftnfade
others?
trade top book bid, bid size increses...opp for sell

#################################onerow =[]
##genericTicks other types with return codes:
##100 Option Volume (currently for stocks) 29, 30aw
##101 Option Open Interest (currently for stocks) 27, 28
##104 Historical Volatility (currently for stocks) 23
##162 Index Future Premium 31
##165 Miscellaneous Stats 15, 16,17, 18,19, 20,21
##221 Mark Price (used in TWS P&L computations) 37
##225 Auction values (volume, price and imbalance) 34, 35,36
##########233 RTVolume - contains lasttradeprice, lastsize, lasttime, totalvolume, VWAP, single trade flag.48
##Single trade flag - True indicates filled by a single market maker; False is multiple marketmakers
##Here is an example of the RTVolume formatting for AAPL:
##RTVolume=701.28;1;1348075471534;67854;701.46918464;true
##RTVolume=701.26;3;1348075476533;67857;701.46917554;false
TickType.getField(int tickType) to
retrieve the field description. For example, a field value of 38

0 BID_SIZE tickSize()
1 BID_PRICE tickPrice()
2 ASK_PRICE tickPrice()
3 ASK_SIZE tickSize()
4 LAST_PRICE tickPrice()
5 LAST_SIZE tickSize()
6 HIGH tickPrice()
7 LOW tickPrice()
8 VOLUME tickSize()
9 CLOSE_PRICE tickPrice()
10 BID_OPTION_COMPUTATION tickOptionComputation()
11 ASK_OPTION_COMPUTATION tickOptionComputation()
12 LAST_OPTION_COMPUTATION tickOptionComputation()
13 MODEL_OPTION_COMPUTATION tickOptionComputation()
14 OPEN_TICK tickPrice()
15 LOW_13_WEEK tickPrice()
16 HIGH_13_WEEK tickPrice()
17 LOW_26_WEEK tickPrice()
18 HIGH_26_WEEK tickPrice()
API Reference Guide 525
Chapter 9 Reference
Tick Value Description Event/Function/Method
19 LOW_52_WEEK tickPrice()
20 HIGH_52_WEEK tickPrice()
21 AVG_VOLUME tickSize()
22 OPEN_INTEREST tickSize()
23 OPTION_HISTORICAL_VOL tickGeneric()
24 OPTION_IMPLIED_VOL tickGeneric()
25 OPTION_BID_EXCH NOT USED
26 OPTION_ASK_EXCH NOT USED
27 OPTION_CALL_OPEN_INTEREST tickSize()
28 OPTION_PUT_OPEN_INTEREST tickSize()
29 OPTION_CALL_VOLUME tickSize()
30 OPTION_PUT_VOLUME tickSize()
31 INDEX_FUTURE_PREMIUM tickGeneric()
32 BID_EXCH tickString()
33 ASK_EXCH tickString()
34 AUCTION_VOLUME tickSize()
35 AUCTION_PRICE tickPrice()
36 AUCTION_IMBALANCE tickSize()
37 MARK_PRICE tickPrice()
38 BID_EFP_COMPUTATION tickEFP()
39 ASK_EFP_COMPUTATION tickEFP()
40 LAST_EFP_COMPUTATION tickEFP()
41 OPEN_EFP_COMPUTATION tickEFP()
42 HIGH_EFP_COMPUTATION tickEFP()
43 LOW_EFP_COMPUTATION tickEFP()
44 CLOSE_EFP_COMPUTATION tickEFP()
45 LAST_TIMESTAMP tickString()
46 SHORTABLE tickString()
47 FUNDAMENTAL_RATIOS tickString()
48 RT_VOLUME tickString()
49 HALTED See Note 2 below.
50 BIDYIELD tickPrice()
See Note 3 below
51 ASKYIELD tickPrice()
See Note 3 below
'''
