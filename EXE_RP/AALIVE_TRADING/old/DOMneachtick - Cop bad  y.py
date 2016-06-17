# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
########################
    #####################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################
import  rpu_rp, rpInd, ibutiles, TicksUtile
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, sym
global symbol_list
today =  rpu_rp.todaysdateunix()
from datetime import datetime
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
symbol_list =['ES']
ticktypedict = rpu_rp.create_dict(libsyms,0,11)
########################################
##########
def sum_array(array):
    c=0
    suma =0
    while c < len(array):
        suma+=int(array[c])
        c+=1
    return suma
symTickerIddict ={}
contractdict ={}
sym = 'ES'

filein = DataDown +today+'.'+sym+ '.RTtickDOMs.bu.csv'
buylineprice =[0,0,0,0,0]
buylinesize =[0,0,0,0,0]
selllineprice =[0,0,0,0,0]
selllinesize =[0,0,0,0,0]
prevtotdiff = 0
for line in rpu_rp.CsvToLines(filein):
########    if 'operation=2' in str(line) and 'position=0'  in str(line):
########        print line
##    line = (cline.replace('>','')).replace(' ','')
##    print line
    arrayout = []

    position = int(line[1].replace('position=','').replace('>','').replace(' ',''))
##    side = line[3].replace('side=','')
    size = line[5].replace('size=','').replace('>','').replace(' ','')
    operation = line[2].replace('operation=','').replace('>','').replace(' ','')
    price = line[4].replace('price=','').replace('>','').replace(' ','')
##    if price == '0.0':
##        print line
    if 'side=1' in str(line):
        buylineprice[position] = price
        buylinesize[position] = size
        pass
    else:
        selllineprice[position] = price
        selllinesize[position] = size

    totalbuy = sum_array(buylinesize)
    totalsell = sum_array(selllinesize)     
    totdiff = totalbuy - totalsell
    if totdiff == 0:
        totdiff = 1
    totdiffperc = round(totdiff/max(totalbuy,totalsell),5)
##    print totalbuy, totalsell
    difftoprev = totdiff - prevtotdiff
    prevtotdiff = totdiff
    buytopprice = buylineprice[0]
    selltopprice = selllineprice[0]

##    print 'SELL', selllinesize, totalsell, totdiff
    if difftoprev > 250 and difftoprev < 5000 :
        print buytopprice,'BUY', buylinesize, totalbuy, totdiff, totalsell, selllinesize, 'SELL',selltopprice,difftoprev,totdiffperc
##    line = parsedlinenew.split('=')

        '''
another array with price gaps...then the top gap as in width between bidoffer
scenariios....
bidHitNfad...count how often
offerliftnfade
others?
trade top book bid, bid size increses...opp for sell

'''
##    epochstring = (line[2])
#################################onerow =[]
##        <tickString tickerId=1, tickType=45, value=1441585476>
##<tickPrice tickerId=1, field=4, price=1922.75, canAutoExecute=0>
##<tickPrice tickerId=1, field=4, price=1922.75, canAutoExecute=0>
##<tickSize tickerId=1, field=5, size=2>


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
