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
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
from datetime import datetime
import ctypes 
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import ibutiles
######
#############################
symbol_list = symdict.keys()
symbol_list =['ES']
########################################
def sum_array(array,mode):
    c=0
    suma =0
    while c < len(array):
        suma+=int(array[c])
        c+=1
        if mode == 'toponly':
            suma = int(array[0])
        else:
            pass
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
def checkDOMticks(sym,fnums):
    filein = DataDown +today+'.'+sym+ '.RTMktDepth.csv'
    buylineprice = prepare_empty_array(fnums)
    buylinesize = prepare_empty_array(fnums)
    selllineprice = prepare_empty_array(fnums)
    selllinesize =  prepare_empty_array(fnums)
    prevtotdiff = 0
    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),15000):
##        print line
        
        position = int(line[1].replace('position=','').replace('>','').replace(' ',''))
        size = float(line[5].replace('size=','').replace('>','').replace(' ',''))
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
    sizeweightedbid = sum_2arrays_weighted(buylineprice,buylinesize,'bla')
    sizeweightedsell = sum_2arrays_weighted(selllineprice,selllinesize,'bla')
    totalbuy = float(sum_array(buylinesize,'all'))
    totalsell = float(sum_array(selllinesize,'all') )    
    totdiff = totalbuy - totalsell
    totalratio = totalbuy/totalsell
    topbuy = float(sum_array(buylinesize,'toponly'))
    topsell = float(sum_array(selllinesize,'toponly'))     
    topdiff = topbuy - topsell
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
        print 'top>>>>',topbuy,'x',topsell, 'Topbuy ratio =',topbuy/(topsell+1), 'Totalbook Ratio >>>',totalratio
##        print time,'B', buylinesize,  selllinesize, 'S',buytopprice,selltopprice
#####################
def checkRTnonbarticks(sym,fnums):
    fullarray =[]
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv'
    prevtotdiff = ask = bid =0
    string =''
    time = ''
    size = ''
    tprice = 0.0
    tsize = singletrade = totdaysize= vwap =''
    totdowns = totups = 0
    tottickups=0
    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),2000):
##        print line

        if 'tickString' in str(line) and 'tickType=48':
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
##            print string
        if 'tickPrice' in str(line):
##            print line
            time = line[4]
            if line[1] == ' field=1':
                    bid= float(line[2].replace(' price=',''))
                    pass
            if line[1] == ' field=2':                
                    ask = float(line[2].replace(' price=',''))
                    pass
##            if bid == 0.0:
##                print line
        if 'tickSize' in str(line):
            time = line[3]
            size = line[2]
        if 'tickString' in str(line) and len(string) > 2 and bid > 0 and ask > 0:
            if bid == tprice:
                bflag = 'down'
##                print 'hitbid'
                totdowns += tsize
                tottickups = tottickups -1
                pass
            else:
                bflag = 'uptick'
##                print 'uptick'
                totups += tsize
                tottickups +=1
            aout =[]
            diffupsdowns = totups-totdowns
            aout.append(bid)
##            aout.append(ask)
##            aout.append(time)
##            aout.append(tprice)
##            aout.append(tsize)
##            aout.append(vwap)
##            aout.append(bflag)
            aout.append(diffupsdowns)
            aout.append(tottickups)
            aout.append('upsVSdowns')
            fullarray.append(aout)
    c=0
    x = len(fullarray)
    for l in fullarray:
        c+=1
        if c > (x - 3):
            print l
###############################
            #####################
fullarray =[]
def checkRTnonbarticksNEW(sym,fnums):
##    fullarray =[]
    filein = DataDown +today+'.'+sym+ '.RTtickData.csv'
    prevtotdiff = ask = bid =0
    string =''
    time = ''
    size = ''
    tprice = 0.0
    tsize = singletrade = totdaysize= vwap =''
    totdowns = totups = 0
    tottickups=0
    for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),400):
##        print line
        if 'tickString' in str(line) and 'tickType=48':
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
##            print string
        if 'tickPrice' in str(line):
##            print line
            time = line[4]
            if line[1] == ' field=1':
                    bid= float(line[2].replace(' price=',''))
                    pass
            if line[1] == ' field=2':                
                    ask = float(line[2].replace(' price=',''))
                    pass
##            if bid == 0.0:
##                print line
        if 'tickSize' in str(line):
            time = line[3]
            size = line[2]
        if 'tickString' in str(line) and len(string) > 2 and bid > 0 and ask > 0:
            if bid == tprice:
                bflag = 'down'
##                print '>>>>>>>>','hitbid',tsize,'@', tprice,bid,ask
                tag = '>>>>>>>>'+' '+'hitbid'+' '+str(tsize)+' '+'@'+' '+ str(tprice)+ ' '+str(bid)+' '+str(ask)

                totdowns += tsize
                tottickups = tottickups -1
                pass
            else:
                bflag = 'uptick'
##                print 'XXXXXXXX','uptick',tsize,'@', tprice,bid,ask
                tag = 'XXXXXXXX'+' uptick '+str(tsize)+' @ '+ str(tprice)+' '+ str(bid)+' '+str(ask)

                totups += tsize
                tottickups +=1
            aout =[]
            if tsize > 50:
                aout.append(tag)
                fullarray.append(aout)
##            print fullarray
    c=0
    x = len(fullarray)
    for l in fullarray:
        c+=1
        if c > (x - 4):
            print l
###############################
threshold = 0.0
loopmax =2000
loop = 0
sleeptime = 2
while loop < loopmax:
    sym = 'ES'
    print '====='
    checkRTnonbarticksNEW(sym,1)
    print '>>>>>'
##    checkDOMticks(sym,10)
    sleep(sleeptime)
    loop+=1
'''
another array with price gaps...then the top gap as in width between bidoffer
scenariios....
bidHitNfad...count how often
offerliftnfade
others?
trade top book bid, bid size increses...opp for sell
'''
#################################onerow =[]
##genericTicks other types with return codes:
##100 Option Volume (currently for stocks) 29, 30
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
