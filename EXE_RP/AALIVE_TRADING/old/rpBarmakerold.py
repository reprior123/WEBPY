# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    print var, nd[var]
    locals()[var] = nd[var]
####################################
import rpu_rp, TicksUtile
decimalboost = 1
##today =  rpu_rp.todaysdateunix()  ##
##today = '20151006'
#################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################################
def strip1string(multilinearrayin,fieldnum):
    arrayout = []
    for line in multilinearrayin:
        if len(line) > 2:
            arrayout.append(line[fieldnum])
    return arrayout    
###############
def strip1float(multilinearrayin,fieldnum,sym):
    arrayout = []
    rf = roundfactordict[sym]
    for line in multilinearrayin:
        if len(line) > 2:
            valb = round(float(line[fieldnum]),int(rf))
            arrayout.append(valb)
    return arrayout    
#################################################
    ### if want to disable boost, set boost function to value 1
def boost_pricearray(arrayprices,sym):
    decimalboost = float(dboostdict[sym])
    arrayout =[]
    for l in arrayprices:
        if len(l) > 0 :
            newl = []
            newl.append(l[0])
            newl.append(l[1])
            newl.append(round(float(l[2])*decimalboost,4))
            newl.append(round(float(l[3])*decimalboost,4))
            newl.append(round(float(l[4])*decimalboost,4))
            newl.append(round(float(l[5])*decimalboost,4))
            if len(l) == 7 :
                newl.append('full')
                newl.append(l[6])
            else:
                newl.append(l[6])
                newl.append(l[7])
            arrayout.append(newl)
    return arrayout
################################################
def GetBars(arrayin,sym,Indtitle,dur,threshold):  #add barr age from last cross here
    print arrayin[177]
    print arrayin[176]

    bscloses = strip1float(arrayin,5,sym) ##raw close price
##    date =  rpu_rp.todaysdateunix()  ##
    bsopens = strip1float(arrayin,2,sym) ##raw open price
    bshighs = strip1float(arrayin,3,sym)
    bslows = strip1float(arrayin,4,sym)
    timestamparray = strip1string(arrayin,1)
    arraybars = make_bars(timestamparray,bsopens,bshighs,bslows,bscloses)
    return arraybars
    
def create_bars_files(sym,dur,date,threshold,newindlist):
    print dur
    durinseconds = secdict[dur]
    DurBoth = rpu_rp.CsvToLines( DataDown+ date + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
    DurBothBoosted = boost_pricearray(DurBoth,sym)
    for indicator in newindlist:
        indarr = GetBars(DurBothBoosted,sym,indicator,dur,threshold)
        statename = sym+'.'+dur.replace(' ','')+'.'
        statefile = statearea +statename + indicator  + '.bars.csv'
        rpu_rp.WriteArrayToCsvfile(statefile, indarr)
#################################
def make_bars(times,opens,highs,lows,closes):  ## S1 is the same but with lows ## pivot,high,lo,close arrays
    c=0
    bars =[]
    prevbarline = [1972.0, 1971.25, 1972.0, 1971.25, 'green', 0.75, 0.75, 0.0, 0.0, 0.0, 0.0, ' 2015-10-06 01:26:00', 'flat']
    prevclose = 0.0
    while c < len(opens): #a1 is pivotpoint array a2 is highs    
        barline =[]
        time = (times[c])
        openpr = float(opens[c])
        highpr = float(highs[c])
        lowpr = float(lows[c])
        closepr = float(closes[c])
        print openpr,closepr
##        print openpr,closepr,highpr,lowpr
        if closepr > openpr :
            bar = 'green'
            uppertail = highpr - closepr
            lowertail = openpr - lowpr
            fullbarwidth = highpr - lowpr
            solidbarwidth = closepr - openpr
        elif openpr > closepr:
            bar = 'red'
            lowertail = closepr - lowpr
            uppertail = highpr - openpr
            fullbarwidth = highpr - lowpr
            solidbarwidth = closepr - openpr
        else:
            bar = 'yellow'
            uppertail = highpr - openpr
            lowertail = closepr - lowpr
            solidbarwidth = .0001
            fullbarwidth = highpr - lowpr
        if fullbarwidth == 0:
            fullbarwidth = 0.001       
##        print fullbarwidth
        utailpct = round(uppertail /  fullbarwidth,2)
        ltailpct =  round(lowertail / fullbarwidth,2)
        tag = 'flat'

        if utailpct > .50:
            tag = 'upperBIG'
        if ltailpct > .50:
            tag = 'lowertailbig'
        prevclose = prevbarline[0]
        print 'xxxx',prevclose, openpr,highpr, lowpr,time

        gapdiff = prevclose - openpr
        if gapdiff == 110:
            print prevclose, openpr, gapdiff, time
            
        barline.append(highpr)
        barline.append(openpr)
        barline.append(closepr)
        barline.append(lowpr)
        barline.append(bar)
        barline.append(abs(solidbarwidth))
        barline.append(fullbarwidth)
        barline.append(uppertail)
        barline.append(lowertail)
        barline.append(utailpct)
        barline.append(ltailpct)
        barline.append(time)
        barline.append(tag)
        bars.append(barline)
        prevbarline = barline
        prevclose = closepr
##        print barline
########
        c+=1
    print len(opens)
    return bars
#################################
sym = 'ES'
dur = '5mins'
date = today
threshold = 0
newindlist = ['bars']
durlist = ['1hour']#'15mins']#, '5mins','15mins']
for dur in durlist:
    create_bars_files(sym,dur,date,threshold,newindlist)
#################################################################
#######
def fibbo_50retrace(low,high,sym,perc) :  # could also use a time range for a range of bars / add this to states per duration
    retraceval = (high-low)/(100/perc)
    return retraceval
#############
################
def find_hi_low(array,scanvalue,style,cvalue):
    if cvalue < scanvalue:
        slicestartvalue = cvalue -1
    else:
        slicestartvalue  = cvalue-scanvalue
    arrayslice = array[slicestartvalue:cvalue]
    oldlow = 9999
    oldhigh = -9999           
    d = 0
    while d < len(arrayslice):                       
        newlow = arrayslice[d]
        newhigh = arrayslice[d]
        if newlow < oldlow:
            oldlow = newlow
        if newhigh > oldhigh:
            oldhigh = newhigh
        d+=1 
    if style == 'lowestlow':
        final  = round(oldlow,6)
    else:
        final  = round(oldhigh,6)
    return final
##################   
