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
##        print openpr,closepr
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
##        print 'xxxx',prevclose, openpr,highpr, lowpr,time

        gapdiff = prevclose - openpr
        if gapdiff != 0:
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
durlist = ['5secs']#'15mins']#, '5mins','15mins']
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
'''
A Doji is formed when the open and the close are the same or
very close. The length of the shadows are not important.
The Japanese interpretation is that the bulls and the bears are conflicting.
The appearance of a Doji should alert the investor of major indecision.

 
The Gravestone Doji is formed when the open and the close
occur at the  low of the day. It is found occasionally at
market bottoms, but it's forte is calling market tops.
The name, Gravestone Doji, is derived by the formation of the signal looking like a gravestone.


The Long-legged Doji has one or two very long shadows.
Long-legged Doji's are often signs of market tops.
If the open and the close are in the center of the
session's trading range, the signal is referred to as a Rickshaw Man.
. The Japanese believe these signals to mean that the trend has "lost it's sense of direction."


The Bullish Engulfing Pattern is formed at the end of a downtrend.
A white body is formed that opens lower and closes higher than the
black candle open and close from the previous day. This complete
engulfing of the previous day's body represents overwhelming buying pressure dissipating the selling pressure.


The Bearish Engulfing Pattern is directly opposite to the bullish pattern.
It is created at the end of an up-trending market. The black real body
completely engulfs the previous day's white body. This shows that the bears are now overwhelming the bulls.


The Dark Cloud Cover is a two-day bearish pattern found at the
end of an upturn or at the top of a congested trading area.
The first day of the pattern is a strong white real body.
The second day's price opens higher than any of the previous day's trading range.


The Piercing Pattern is a bottom reversal.
It is a two candle pattern at the end of a declining market.
The first day real body is black. The second day is a long white body.
The white day opens sharply lower, under the trading range of the previous day.
The price comes up to where it closes above the 50% level of the black body.

Hammer and Hanging-man are candlesticks with long lower shadows
and small real bodies. The bodies are at the top of the trading session.
This pattern at the bottom of the down-trend is called a Hammer.
It is hammering out a base. The Japanese word is takuri, meaning "trying to gauge the depth".


The Morning Star is a bottom reversal signal. Like the morning star,
the planet Mercury, it foretells the sunrise, or the rising prices.
The pattern consists of a three day signal.
 


The Evening Star is the exact opposite of the morning star.
The evening star, the planet Venus, occurs just before the
darkness sets in. The evening star is found at the end of the uptrend.


A Shooting Star sends a warning that the top is near. It got its name by looking like a shooting star. 
The Shooting Star Formation, at the bottom of a trend, is a bullish signal. It is known as an inverted
hammer. It is important to wait for the bullish verification. Now that we have seen some of the basic signals,
let's take a look at the added power of some of the other formations.
'''
