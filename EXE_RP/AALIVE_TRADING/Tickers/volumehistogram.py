################################
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
global timedate_format, nextorderID, date, today,recentlimit, time_format
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, BarUtiles
import glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
######################
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global  sym, symbol_list, symdict
########################################
date = today
####################
#############################
symbol_list = symdict.keys()
symbol_list =['FDAX', 'ES']
date = today
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
    dfactor =100
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
    filein = DataDown +date+'.'+sym+ '.RTMktDepth.csv'
    if style == 'dom':
        for line in rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filein),1000):
            if 'updateMktDepth' in str(line):
##                print line
                larray.append(line)
    return larray

#####################
fullarray =[]
#############################
def createVolHistogram(sym,fnums):
    filein = DataDown +date+'.'+sym+ '.RTtickData.csv'
    totlen =  len(rpu_rp.CsvToLines(filein))
    thirdlen = int(totlen/3)
    tails = [thirdlen,thirdlen*2,totlen]
    for tailvalue in tails:
        print totlen
        sleep(4)
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
        for line in rpu_rp.head_array_to_array(rpu_rp.CsvToLines(filein),tailvalue):
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
        ldiv = 1000
        print "\n" * 50
        strings =''
        for price in uarray:
            lvol =0.0
            for l in pnsize:
                if price == l[0] and price > 0.0 :
                    lvol += l[1]
            if lvol > 12000 :
    ##            print ('avg %6.2f ... %4d .. %s' % (price,lvol,int(lvol/ldiv)*'l'))
                strings +=  ('avg %6.2f ... %4d .. %s\n' % (price,lvol,int(lvol/ldiv)*'|'))
        print strings
    ##    Mbox('b', strings, '')
##########################################
def createVolHistogramdload(sym,fnums,ldiv,roundfactor):
    filein = DataDown +date+'.'+sym+ '.1min.both.csv'
    totlen =  len(rpu_rp.CsvToLines(filein))
    thirdlen = int(totlen/3)
    tails = [thirdlen,thirdlen*2,totlen]
    for tailvalue in tails:
        print totlen, thirdlen
        sleep(2)
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
        for line in rpu_rp.head_array_to_array(rpu_rp.CsvToLines(filein),tailvalue):
            if len(line) > 2 and '2015-12-10' in str(line):
##                print line
                pnsizeline =[]
                time = line[1]
                tprice = float(line[5].replace('value=',''))
                tprice = round(float(line[5].replace('value=','')),roundfactor)
                tsize = float(line[6])
##                singletrade = string[5]
##                totdaysize = string[3]
##                vwaps  = string[4]
                vwap =0.0
                ##            value=1984.50;1;1441796865858;207069;1982.49963539;true>
                ##            print tsize,tprice,time,'trade', bid, ask, bidsize, asksize
                pricearrayraw.append(tprice)
                pnsizeline.append(tprice)
                pnsizeline.append(tsize)
                pnsize.append(pnsizeline)

        uarray = rpu_rp.uniqArray(pricearrayraw)
##        ldiv = 200
        print "\n" * 50
        strings =''
        for price in uarray:
            lvol =0.0
            for l in pnsize:
                if price == l[0] and price > 0.0 :
                    lvol += l[1]
            if lvol > 0 :
    ##            print ('avg %6.2f ... %4d .. %s' % (price,lvol,int(lvol/ldiv)*'l'))
                strings +=  ('avg %6.2f ... %4d .. %s\n' % (price,lvol,int(lvol/ldiv)*'|'))
        print strings
    ##    Mbox('b', strings, '')
##########################################
###############################         
threshold = 0.0
loopmax = 1
loop = 0
sleeptime = 3
while loop < loopmax:
    snumlist = [0,1]
    for snum in snumlist:
        sym = symbol_list[snum] #'ES'
        ldiv =50
        if snum == 1:
            ldiv =1000
        roundfactor =2
        createVolHistogramdload(sym,1,ldiv,roundfactor)
        sleep(sleeptime)  
    loop+=1
'''
another array with price gaps
...then the top gap as in width between bidoffer
scenariios....
bidHitNfad...count how often
offerliftnfade
others?
trade top book bid, bid size increses...opp for sell
'''
