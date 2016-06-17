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
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
############################################
decimalboost = 1
#################
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
        try:
            if len(line) > 2:
                valb = round(float(line[fieldnum]),int(rf))
                arrayout.append(valb)
                pass
        except:
            print line
    return arrayout    
#################################################
def mvavgToArray(arrayin,smaNum):
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    while c < numbars:
        if c < smaNum:
            valtodrop = 0
            div = c+1
        else:
            valtodrop = float(arrayin[c-smaNum])
            div = smaNum                             
        tot += float(arrayin[c])
        tot = tot - valtodrop
        sma = tot/div
        c += 1
        arrayout.append(round(sma,10))
    return arrayout
#################################################
def SMAmvavgToArray(arrayin,smaNum):
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    while c < numbars:
        if c < smaNum:
            valtodrop = 0
            div = c+1
        else:
            valtodrop = float(arrayin[c-smaNum])
            div = smaNum                             
        tot += float(arrayin[c])
        tot = tot - valtodrop
        sma = tot/div
        c += 1
        arrayout.append(round(sma,10))
    return arrayout
#################################################
def maxminAvgToArray(arrayin):
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    totval = 0
    maxval = arrayin[0]
    minval = arrayin[0]
    while c < numbars:
        val = arrayin[c]
        totval+=val
        if val < minval:
            minval = val
        if val > maxval:
            maxval = val
        c += 1
    avg = totval/numbars
##        arrayout.append(round(sma,10))
    return minval,maxval,avg
######################
#################################################
def maxminABSAvgToArray(arrayin):
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    totval = 0
    maxval = arrayin[0]
    minval = arrayin[0]
    while c < numbars:
        val = arrayin[c]
        totval+=abs(val)
        if val < minval:
            minval = val
        if val > maxval:
            maxval = val
        c += 1
    avg = totval/numbars
##        arrayout.append(round(sma,10))
    return minval,maxval,avg
######################
def maxStdAvgToArray(arrayin):
    smavalstd = 50
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    totval = 0
    maxval = arrayin[0]
    minval = arrayin[0]
    stdarray = StdToArray(arrayin,smavalstd)
    for s in stdarray:
        std = s
    while c < numbars:
        val = arrayin[c]
        totval+=abs(val)
        if val < minval:
            minval = val
        if val > maxval:
            maxval = val
        c += 1
    avg = totval/numbars
##        arrayout.append(round(sma,10))
    return std,maxval,avg
######################
######################
def ArrayToAllStats(arrayin,smavalstd):
    smavalstd = 50
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    totval = totvalAbs = 0
    maxval = arrayin[0]
    minval = arrayin[0]
    minvalNegs = maxvalNegs = 0
    minvalPoss = maxvalPoss = 0
    stdarray = StdToArray(arrayin,smavalstd)
    for s in stdarray:
        std1 = round(s,4)
    while c < numbars:
        val = round(arrayin[c],4)
        totvalAbs+=abs(val)
        totval+=val
        if val < minval:
            minval = val
        if val > maxval:
            maxval = val
        if val < minvalNegs and val < 0:
            minvalNegs = val
        if val > maxvalNegs and val < 0:
            maxvalNegs = val          
        if val < minvalPoss and val > 0:
            minvalPoss = val
        if val > maxvalPoss and val > 0:
            maxvalPoss = val
        c += 1
    avg = round(totval/numbars,4)
    AbsAvg = round(totvalAbs/numbars,4)
##        arrayout.append(round(sma,10))
    return minval,maxval,avg,AbsAvg,std1,minvalNegs,maxvalNegs,minvalPoss,maxvalPoss
######################
def MaxMinAvgIndArray(sym,dur,ind,fieldnum):
    arrayfull = rpu_rp.CsvToLines(statearea + sym+'.'+dur+'.'+ind+'.state.csv')
    arrayin = strip1float(arrayfull,fieldnum,sym)
    stats = maxminAvgToArray(arrayin)
    return stats
#################################################
def MaxMinABSAvgIndArray(sym,dur,ind,fieldnum):
    arrayfull = rpu_rp.CsvToLines(statearea + sym+'.'+dur+'.'+ind+'.state.csv')
    arrayin = strip1float(arrayfull,fieldnum,sym)
    stats = maxminABSAvgToArray(arrayin)
    return stats
######################
def MaxStdAvgIndArray(sym,dur,ind,fieldnum):
    arrayfull = rpu_rp.CsvToLines(statearea + sym+'.'+dur+'.'+ind+'.state.csv')
    arrayin = strip1float(arrayfull,fieldnum,sym)
    stats = maxStdAvgToArray(arrayin) ## gives std,max,avg
    return stats
######################
def StatesArrayToAllStats(sym,dur,ind,fieldnum):
    arrayfull = rpu_rp.CsvToLines(statearea + sym+'.'+dur+'.'+ind+'.state.csv')
    arrayin = strip1float(arrayfull,fieldnum,sym)
    stats = ArrayToAllStats(arrayin,50) ## gives std,max,avg
    return stats
######################
def CreateIndvalueTable(indlist,durlist,symlist,filename):
    mmarrayfull =[]
####    def StdToArray(arrayin,smavalstd)
##    indlist = indlist_All#['ROC', 'mcross']
    print 'minval,maxval,avg,AbsAvg,std1,MinvalNegs,MaxvalNegs,minvalPoss,maxvalPoss'
    stdvariable = 1 ###add this to a table to make diff for each ind and to get more foo
    for sym in symlist:
        for dur in durlist:
            for ind in indlist:
                mmarray =[]
##                t = MaxMinAvgIndArray(sym,dur,ind,1)
##                t = MaxStdAvgIndArray(sym,dur,ind,1)            
                t = StatesArrayToAllStats(sym,dur,ind,1)
                tarray = list(t)
                print tarray, sym,dur,ind
                midpoint =  0 #  round(tarray[2],4)
                maxval = round(tarray[1],4) # this gives max 
                maxval = stdvariable * round(tarray[4],4) #this gives the std rather than max
                stdvalue = 1 * round(tarray[4],4) #this gives the std rather than max
                mmarray.append(ind)
                mmarray.append(dur)
                mmarray.append(midpoint) ## this is the midpoint level, normally 0
                mmarray.append(maxval) ## this is the max abs value for 80% rules
                ##                mmarray.append(tarray[0]) ## is minvalue
                mmarray.append('slopenormal')
                mmarray.append('PCompareNormal')
                mmarray.append(sym)
                mmarray.append(stdvalue)
                mmarrayfull.append(mmarray)
##    print mmarrayfull
    rpu_rp.WriteArrayToCsvfile(filename,mmarrayfull)
##        rpu_rp.WriteArrayToCsvfile(libarea +'indlevels.' + sym + '.csv',mmarrayfull)
####    print ind,dur,midpointvalue = 0?,maxvalue,,PCompareNormal
##########################
##CreateIndvalueTable(indlist,durlist,symlist)
###############
def EMAmvavgToArray(arrayin,smaNum):
    c = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    mult = float(2.0/(smaNum+1))
    prevemavalue = arrayin[c]
    while c < numbars:
        valuenow = arrayin[c]
        if c < smaNum:
            tot += valuenow
            diviser = c + 1
            ema = tot/diviser
        else:
            ema = valuenow * mult + (prevemavalue * (1 - mult))
##            tot += (valuenow) - (prevsmavalue)
##            ema = ((valuenow - prevema) * multiplier) + prevema
##            diviser = smaNum
        c +=1
        prevemavalue = ema
        arrayout.append(round(ema,4))
    return arrayout
######################################combine the SMA and EMA and use mode !!! <<<#####
def lableToarray(bsclose,tag):
    arrout =[]
    for c in bsclose:
        arrout.append(tag)
    return arrout
###########################3
def difftwoarrays(a1,a2):
    alength = min(len(a1),len(a2))
    arrayout =[]
    c = 0 
    while c < alength:
        diff = round((a1[c] - a2[c]),6)
        arrayout.append(diff)
        c += 1
    return arrayout
######################################
###########################3
def difftwoarraysMIDS(a1,a2):
    alength = min(len(a1),len(a2))
    arrayout =[]
    c = 0 
    while c < alength:
        diff = round(((a1[c] - a2[c]))/2 + a1[c],6)
        arrayout.append(diff)
        c += 1
    return arrayout
def ratiotwoarrays(a1,a2,mode,basevalue1,basevalue2):
##    a1tailed =rpu_rp.tail_array_to_array(a1,100000)
##    a2tailed = rpu_rp.tail_array_to_array(a2,100000)
    alength = len(a1)
    maxaval = alength
    blength = len(a2)
    if alength != blength:
        if blength < alength:
            maxaval = blength
        print 'different length arrays for es compare!!!'        
##    blength = len(a2tailed)
##    print alength,blength
##    minlength = min(alength,blength)
    arrayout =[]
    c = 0 
    while c < maxaval:
        if a2[c] == 0 or a1[c] == 0:
            ratio = 100
        else:
            if mode == 'simple':
                perc1 = perc2 = 1
            perc1 = a1[c]/basevalue1
            perc2 = a2[c]/basevalue2
            ratio = perc1/perc2 
        arrayout.append(round(ratio,4))
        c += 1
    return arrayout
#####################
def makearrayJust2(time,slopebs,signbs,bsclose,indy2,slope2,sign2,indlabel):  ## assumes one field in postion 0
    arrayout =[]
    c=0
    while c < len(bsclose):
        newline =[]
        numfields = 8
        f = 0
        flist = [time,slopebs,signbs,bsclose,indy2,slope2,sign2,indlabel]
        for f in flist:
            if f == indlabel:
                newline.append(indlabel)
            else:
                newline.append(f[c])
        arrayout.append(newline)
        c+=1
    return arrayout
##############################################
def show_slope(arrayin,mode):
    arrayout =[]
    c = 0
    diff = 0
    while c < len(arrayin):
        if c == 0 :
            prevc = 0
        else:
            prevc = c-1
        diff = round(arrayin[c] - arrayin[prevc],6)
        if diff < 0 :
            result = 'slopedn'
        elif diff > 0:
            result = 'slopeup'
        else:
            result ='slopeft'
        final = round(diff,4)
        if mode == 'tagstyle':
            arrayout.append(result)
        else:
            arrayout.append(final)
        c +=1
    return arrayout
######################################################
def show_cross(signs,mode):  
    c=0
    prevsign = 'flat'
    arrayout =[]
    crossage = 0
    while c < len(signs):
        sign = signs[c]
        crossage +=1
        crossageprint = crossage
        if sign == prevsign:
            crossflag = 'nocross'
        elif sign == 'neg':
            crossflag = 'negcrxx'
            crossage = 0
        else:
            crossflag = 'poscrxx'
            crossage = 0
        if mode == 'crossage':
            arrayout.append(crossageprint)
            pass
        else:
            arrayout.append(crossflag)
        prevsign = sign
        c+=1
    return arrayout
##############################################
def show_sign(a1,tag,threshold):  
    c=0
    arrayout =[]
    signof_diffval = 'na'
    while c < len(a1):
        diffval = a1[c]
        if diffval < (0.0 - threshold) :
            signof_diffval = 'neg'
        if diffval > (0.0 + threshold) :
            signof_diffval = 'pos'
        c+=1
        arrayout.append(signof_diffval)   
    return arrayout
###########################################
def show_sign2thresholds(a1,tag,threshold1,threshold2):  
    c=0
    arrayout =[]
    signof_diffval = 'na'
    while c < len(a1):
        diffval = a1[c]
        if diffval < (0.0 - threshold1) :
            signof_diffval = 'pos'
        if diffval > (0.0 + threshold2) :
            signof_diffval = 'neg'
        c+=1
        arrayout.append(signof_diffval)   
    return arrayout
###########################################
def pivotpoint(a1,a2,a3): ## hi,lo,close arrays
    c=0   
    arrayout =[]
    while c < len(a1):
        c+=1
        piv = round((a1[c-2] + a2[c-2] + a3[c-2])/3,4) ####    ppoint = (prevbarHi + prevbarlo +prevclose)/3
        arrayout.append(piv)
    return arrayout
######################
def RS1(a1,a2,a3,mode):  ## S1 is the same but with lows ## pivot,high,lo,close arrays
    c=0
    arrayRout =[]
    arraySout =[]
##    arrayout.append(a1[0])
    pivotarray = pivotpoint(a1,a2,a3)
    while c < len(pivotarray): #a1 is pivotpoint array a2 is highs
        if c == 0:
            prevint = 0
            pass
        else:
            prevint = c-1
        R1 = (2*pivotarray[c]) -  a2[prevint]
        S1 = (2*pivotarray[c]) -  a1[prevint]
        c+=1  
        arrayRout.append(round(R1,4))
        arraySout.append(round(S1,4))
    if mode == 'R':
        return arrayRout
    else:
        return arraySout
###################################
def RS2(a1,a2,a3,mode):  ## S1 is the same but with lows ## pivot,high,lo,close arrays
    c=0
    arrayRout =[]
    arraySout =[]
##    arrayout.append(a1[0])
    pivotarray = pivotpoint(a1,a2,a3)
    while c < len(pivotarray): #a1 is pivotpoint array a2 is highs
        if c == 0:
            prevint = 0
            pass
        else:
            prevint = c-1
        R1 = (2*pivotarray[c]) -  a2[prevint]
        S1 = (2*pivotarray[c]) -  a1[prevint]
        R2 = (pivotarray[c] - S1 ) + R1
        S2 = (pivotarray[c]) - ( R1  - S1 )
        c+=1  
        arrayRout.append(round(R2,4))
        arraySout.append(round(S2,4))
    if mode == 'R':
        return arrayRout
    else:
        return arraySout
###################################
def MACDdiverg(bsclose):
    sma26 = EMAmvavgToArray(bsclose,26)
    sma12 = EMAmvavgToArray(bsclose,12)
    macddiff = difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = EMAmvavgToArray(macddiff,9)
    macddiverg = difftwoarrays(macddiff,macdavg)
    return macddiverg
###########################
def Trigger_from_states(sym,dur,label):
    statefile = statearea + sym + '.' +  dur.replace(' ','') + '.' + label  + '.state.csv'
    mdarray = rpu_rp.CsvToLines(statefile)
    array_of_crosses = rpu_rp.grep_array_to_array(mdarray,'crxx')
##    print array_of_crosses
    return array_of_crosses
###################################
def Trigger_from_statesValues(sym,dur,label,valuemin,valuemax):
    statefile = statearea + sym + '.' +  dur.replace(' ','') + '.' + label  + '.state.csv'
    mdarray = rpu_rp.CsvToLines(statefile)
    array_of_crosses = []
    for l in mdarray:
##        print l
        if float(l[1]) < float(valuemin):
            l[7] = 'poscrxx'
            array_of_crosses.append(l)
        if float(l[1]) > float(valuemax):
            l[7] = 'negcrxx'
            array_of_crosses.append(l)
##            print array_of_crosses
##    array_of_crosses = rpu_rp.grep_array_to_array(mdarray,'crxx')
##            for p in array_of_crosses:
##                print p
    return array_of_crosses
##############################################
def ShowBarCountofInd(sym,dur,ind):
    lastbar =[]
    statefile = statearea + sym + '.' +  dur + '.' + ind  + '.state.csv'
    barcount = len((rpu_rp.CsvToLines(statefile)))
    return barcount
###################################
def ShowLastBarofInd(sym,dur,ind):
    lastbar =[]
    statefile = statearea + sym + '.' +  dur + '.' + ind  + '.state.csv'
    lastbar = (rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(statefile),1))[0]
    return lastbar
###################################
def ShowABarofInd(sym,dur,ind,barnum):
    lastbar =[]
    statefile = statearea + sym + '.' +  dur + '.' + ind  + '.state.csv'
    lastbar = (rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(statefile),barnum))[0]
    return lastbar
###################################
def ShowABarofBars(sym,dur,barnum):
    lastbar =[]
##    statefile = DataDown + sym + '.' +  dur + '.' + ind  + '.state.csv'
    statefile = DataDown + today + '.'+ sym + '.' +  dur  + '.both.csv'
    lastbar = (rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(statefile),barnum))[0]
    return lastbar
###################################
def ShowABarofIndByTime(sym,dur,ind,bartime,barfnumlimit):
    lastbar =[]
    statefile = statearea + sym + '.' +  dur + '.' + ind  + '.state.csv'
    lastfewbars = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(statefile),barfnumlimit)
    for bar in lastfewbars:
        if TicksUtile.time_to_epoch(bar[0]) <= TicksUtile.time_to_epoch(bartime) :
            lastbar = bar
    return lastbar
###################################
def ShowRecentPositionState(sym):
    recentstate = 'flat'
    sfile = sigarea + today+ '.positionstate.csv'
    mdarray = rpu_rp.CsvToLines(sfile)
    array_of_crosses = rpu_rp.grep_array_to_array(mdarray,'1')
    for l in array_of_crosses:
        if sym== l[0]:
            recentstate = l[1]
    return recentstate
###################################
def ShowRecentAge(sym,dur,ind,rootname):
    statfnum =12
    recentage = ShowRecentIndValue(sym,dur,ind,statfnum)
    return recentage
###################################
def ShowRecentIndValue(sym,dur,ind,statfnum):
##    print sym,dur,ind
    ##    fnum 2 = value,fnum3 = sign,fnum4=slopeval,fnum5=slope,fnum8=crossstatus,fnum10+ = barprices
    lastbar = ShowLastBarofInd(sym,dur,ind)
    recentval = lastbar[statfnum]
    return recentval
###################################
def ShowRecentStateStats(sym,dur,label,rootname,statfnum):
    ##    fnum 2 = value,fnum3 = sign,fnum4=slopeval,fnum5=slope,fnum8=crossstatus,fnum10+ = barprices
    lastbar = ShowLastBarofInd(sym,dur,ind)
    recentval = lastbar[statfnum]
    return recentval
####################
def ShowRecentCRXLine(sym,dur,label,mode):
    recentline = []
    statefile = statearea + sym + '.' +  dur.replace(' ','') + '.' + label  + '.state.'+ fflag +'csv'
    array_of_crosses = rpu_rp.grep_array_to_array(rpu_rp.CsvToLines(statefile),'crxx')
    for l in array_of_crosses:
        recentline = l
    return recentline
###################################
def ShowRecentCRXTime(sym,dur,label,mode):
    l = ShowRecentCRXLine(sym,dur,label,mode)
    recentage = l[0]
    return recentage
###################################
def ShowRecentCRXCode(sym,dur,label,mode):
    l = ShowRecentCRXLine(sym,dur,label,mode)
    recentage =  str(l[0]) + str(l[2]) + label + dur
    return recentage
###################################
def ShowRecentClPrice(sym,dur,label,mode):
    l = ShowRecentCRXLine(sym,dur,label,mode)
    recentage = l[11]
    return recentage
###################################
def ShowRecentStateValue(sym,dur,label,mode):
    statfnum =1
    recentage = ShowRecentIndValue(sym,dur,ind,statfnum)
    return recentage
###################################
def TRarray(highs,lows,closes):
##    TR = max(high-low,abs(high- prevclose),abs(low-prevclose))
##    def mvavgToArray(arrayin,smaNum):
    numbars = len(closes)
    arrayout =[]
    prevclose = closes[0]
    slicearray =[]
    c = 0
    while c < numbars:
        close = closes[c]
        high = highs[c]
        low = lows[c]
        TR = max((high-low),(abs(high- prevclose)),abs(low-prevclose))
        prevclose = close
        c += 1
        arrayout.append(round(TR,4))
    return arrayout
###########################
def TRhilowarray(highs,lows,closes):
##    TR = max(high-low,abs(high- prevclose),abs(low-prevclose))
##    def mvavgToArray(arrayin,smaNum):
    numbars = len(closes)
    arrayout =[]
    prevclose = closes[0]
    slicearray =[]
    c = 0
    while c < numbars:
        close = closes[c]
        high = highs[c]
        low = lows[c]
        TR3 = (high - low)
        c += 1
        arrayout.append(round(TR3,4))
    return arrayout
###########################
def TR3array(highs,lows,closes):
##    TR = max(high-low,abs(high- prevclose),abs(low-prevclose))
##    def mvavgToArray(arrayin,smaNum):
    numbars = len(closes)
    arrayout =[]
    prevclose = closes[0]
    slicearray =[]
    c = 0
    while c < numbars:
        close = closes[c]
        high = highs[c]
        low = lows[c]
        TR3 = (close + high + low)/3
        c += 1
        arrayout.append(round(TR3,4))
    return arrayout
###########################
def ATR(highs,lows,closes,maVal):
    TRarrayreal = TRarray(highs,lows,closes)
    prevATR=TRarrayreal[0]
    c=0
    arrayout =[]
    numbars = len(TRarrayreal)
    while c < numbars:
        if c< maVal:
            TR = (mvavgToArray(TRarrayreal,maVal))[c] ##     for the first  bars use TR#1 = hi-low,
            pass
        else:            
            TR = TRarrayreal[c]
        ATR = ((prevATR *(maVal-1)) + TR) / maVal  #    ATR =((prevATR *13) + TR) / 14  ## using 14 period value
        prevATR = ATR
        c += 1
        arrayout.append(round(ATR,4))
    return arrayout
###########################
##    14 periods, losses are positive values
##    rsi = 100   -  ((100/ (1+RS))
##    RS = avgGain / AvgLoss
##                    1st avg gain = sum of gains over past 14 bars,,same for loss
##                    following
##                    avggain = ((prevAvgGain) * 13 +currgain)/14
          ## Alternate method of rsi using prev          
###########################
##ROC GT than 0 = increase in up momo
##LT than 0 = increase in down momo
##signal = ROC going up, price going down is Bullish
##roc slope down,  price up, is bearish
#################
def ROC(closes,nfactor):
    closexperiodsago=closes[0]
    c=0
    arrayout =[]
    numbars = len(closes)
    while c < numbars:
        if c > nfactor:
            closenow = closes[c]
            closexperiodsago = closes[c-nfactor]
            roc = (closenow - closexperiodsago)/closexperiodsago
        else:
            closenow = closes[c]
            closexperiodsago = closes[c]
            roc = (closenow - closexperiodsago)/closexperiodsago                      
        c+=1
        arrayout.append(round(roc *100,4))    
    return arrayout
##############
'''
  1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low) 
  2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
  3. 20-period CMF = 20-period Sum of Money Flow Volume / 20 period Sum of Volume 
'''
#############################
def CMF(closes,lows,highs,volume,maVal):   ## chalkin moneyflow
    c=0
##    volumes =[]
    mfvolumes =[]
    arrayout=[]
    numbars = len(closes)
    while c < numbars:
        mfmult = ((closes[c] - lows[c]) - (highs[c] - closes[c])) / (highs[c] - lows[c])
        mfvolume = mfmult * volume[c]
##        volumes.append(volume[c])
        mfvolumes.append(mfvolume)
        c+=1
        ## 20period sum of mfvolumes / volume   same as mvaverage?
##    AvgGain = mvavgToArray(Gainarray,14)
##        arrayout.append(round(RSI,2))
    return volume #arrayout
###########################
def RSI(closes,maVal):
    c=0
    Gain = Loss = 0
    Gainarray =[]
    Lossarray =[]
    arrayout=[]
    numbars = len(closes)
##    print numbars
    while c < numbars:
        if c < 1:
            Barchange = 0
        else:
            Barchange = closes[c] - closes[c-1]
##            print Barchange
            if Barchange > 0:
                Gain = Barchange
                Loss = 0
                pass
            elif Barchange < 0:
                Gain = 0
                Loss = abs(Barchange)
                pass
            else:
                Gain = 0
                Loss = 0
        Gainarray.append(Gain)
        Lossarray.append(Loss)
        c+=1
    AvgGain = mvavgToArray(Gainarray,14)
    AvgLoss = mvavgToArray(Lossarray,14)
    d=0
    while d < len(AvgLoss):
        RS = AvgGain[d] / max(0.0000001,AvgLoss[d])
        RSI = 100 - ( 100 / (1 + RS))
        d+=1
        arrayout.append(round(RSI,2))
    return arrayout
###########################
def keltner_channels(highs,lows,closes,mult,uplow):
    c=0
    mult = 2
    arrayout =[]
    hilows = TRhilowarray(highs,lows,closes)
    avghilow = EMAmvavgToArray(hilows,10)
    
    midtots = TR3array(highs,lows,closes)
    avgmidtots = EMAmvavgToArray(midtots,10)
    while c < len(avghilow):
        a = avgmidtots[c]
        b = avghilow[c]
        if uplow == 'lower':
            dist = a - b
            pass
        else:
            dist = a+b
        c += 1
        arrayout.append(round(dist,4))
    return arrayout        
##################
def StdToArray(arrayin,smavalstd):
##    print smavalstd,'sma'
    c = 0
    std = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0 
    while c < numbars:
        if c < smavalstd:
            std = 0
        else:       
            slicearray = arrayin[(c-smavalstd):c]
            tot = 0
            numnums =len(slicearray)
            for num in slicearray:
                tot +=num
            simplemean1 =  float(tot/numnums)
            diffsq = float(0)
            for num1 in slicearray:
                diff = float(num1 - simplemean1)
                diffsq += float(diff * diff)
            meanofSquares = float(diffsq/(numnums-1))
            std = meanofSquares ** (0.5) 
        arrayout.append(round(std,10))
        c += 1
##        if c > (numbars -2) and numbars > 1500:
##            print std,numbars,numnums,simplemean1
##            print slicearray
##            print '==='
##            for g in slicearray:
##                print g
    return arrayout
#################################################
##################
def stddev(highs,lows,closes,SMAVal):
    c=0
    arrayout =[]
    midtots =  closes #TR3array(highs,lows,closes)   
    avgmidtots = mvavgToArray(midtots,SMAVal)
    stdarray = StdToArray(avgmidtots,SMAVal)   
    while c < len(closes):
        std = stdarray[c]
        c += 1
        arrayout.append(round(std,4))
    return arrayout        
##################
def bbands(highs,lows,closes,SMAVal,stdvariable,uplow):
    c=0
##    print stdvariable
    arrayout =[]
##    stdarray = stddev(highs,lows,closes,SMAVal)
    midtots =  TR3array(highs,lows,closes)
    avgmidtots = mvavgToArray(midtots,SMAVal)
    stdarray = StdToArray(midtots,SMAVal)   
    while c < len(closes):
        std = stdarray[c]
        price  = avgmidtots[c] # this should be the ma at 20
        if uplow == 'lower':
            bbandprice = price - (std * stdvariable)
        else:
            bbandprice = price + (std * stdvariable)
        c += 1
        arrayout.append(round(bbandprice,4))
    return arrayout        
##################
def keltner_channel_mid(highs,lows,closes,mult):
##    ATRarray = ATR(highs,lows,closes,10)
    midtots = TR3array(highs,lows,closes)
    c=0
    mult = 2
    arrayout =[]
    mvarray = EMAmvavgToArray(midtots,10)
    return mvarray        
    ###################################
def show_bar8(today,sym):
    filein = DataDown + today + '.' + sym + '.5mins.both.csv'
    lines = rpu_rp.CsvToLines(filein)
##    oneline = grep '16:05:00' filein
    onelinearray = rpu_rp.grep_array_to_array(lines,'16:05:00')
    print onelinearray
#####################3
def diffvES(close1,close2):
    basevalue1 = close1[0]
    basevalue2 = close2[0]
##    print base1, base2
    mode = 'simple'
    mode = 'realperc'
##    basevalue2 = 11330.50 #11243.0
##    basevalue1 = 2093.25 # 2088.75
##    print close1
    hardratio = 0.1851
    diffed = ratiotwoarrays(close1,close2,mode,basevalue1,basevalue2)
    return diffed
######################
def create_RSlines(sym,clprice):
    linelist = ['R1', 'pivot', 'S1', 'S2', 'R2']
    prevval = 99999
    for line in linelist:        
        newline = float(gatherline(sym,line)[1])
        newlinediff = float(float(clprice) - newline)
        if abs(newlinediff)< prevval:
            prevval = abs(newlinediff)
            livetag = line
            activeline = newline
    if newlinediff  < 0 :
        linestatus = 'below'
    else:
        linestatus = 'above'
    print livetag, activeline, newlinediff, linestatus, clprice
##############################################
##USD.JPY, 2015-08-26 23:25:05,120.0075,120.0725,120.0075,120.0725,full,300
##USD.JPY, 2015-08-26 23:30:05,120.0725,120.1025,120.055,120.0975,partial,230
###########################
    ### if want to disable boost, set boost function to value 1
def boost_pricearray(arrayprices,sym):
    decimalboost = float(dboostdict[sym])
##    decimalboost = float(1.0)
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
def create_states_files(sym,dur,date,threshold,newindlist):
    durinseconds = secdict[dur]
    DurBoth = rpu_rp.CsvToLines( DataDown+ date + '.'+sym+'.' + dur.replace(' ','') + '.both.csv')
    DurBothBoosted = boost_pricearray(DurBoth,sym)
    for indicator in newindlist:
##        print 'creating states',indicator
        indarr = GetStates(DurBothBoosted,sym,indicator,dur,threshold,date)
        statename = sym+'.'+dur.replace(' ','')+'.'
        statefile = statearea +statename + indicator  + '.state.csv'
        rpu_rp.WriteArrayToCsvfile(statefile, indarr)
#################################
def joinArraysStates(tarray,indicator,sign,slope,slopetag,Indtitle,sym,crxxflag,tagarray,highs,lows,bsclose,crossages,stdval):  ## assumes one field in postion 0
    arrayout =[]
    c=0
    while c < len(indicator):
        newline =[]
        f = 0
        flist = [tarray,indicator,sign,slope,slopetag,Indtitle,sym, crxxflag, tagarray, highs, lows, bsclose,crossages,stdval]
        for f in flist:
            if f == sym or f == Indtitle:
                newline.append(f)
            else:
                newline.append(f[c])
        arrayout.append(newline)
        c+=1
    return arrayout
#######
def fibbo_50retrace(low,high,sym,perc) :  # could also use a time range for a range of bars / add this to states per duration
    retraceval = (high-low)/(100/perc)
    return retraceval
#############
def check_lines(linesfile,curprice,tolerance):
    for l in linesfile:
        diff = curprice - l[0]
        if diff < tolerance:
            lines.append(l[0])
            pass
        pass
    return lines
###################
def gatherline(sym,ind):
    dur = '1day'
    indfile = statearea + sym + '.' + dur + '.' + ind + '.state.csv'
    lineprice = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(indfile),1)[0]
    return lineprice
################
###################
def gatherlineNEW(sym,ind,dur):
    print sym,ind,dur
##    dur = '1day'
    indfile = statearea + sym + '.' + dur + '.' + ind + '.state.csv'
    lineprice = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(indfile),1)[0]
    return lineprice
################
def find_hi_low(array,scanvalue,style,cvalue):
    if cvalue < scanvalue:
        slicestartvalue = cvalue -1
    else:
        slicestartvalue  = cvalue-scanvalue
    arrayslice = array[slicestartvalue:cvalue]
    oldlow = 999999999
    oldhigh = -999999999          
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
def StochD(Kpercarray,emaval):
    Dpercarray =  EMAmvavgToArray(Kpercarray,emaval)
    return Dpercarray
###########################
def StochK(highs,lows,closes,scanvalue):
    c=1
    Kpercarray=[]
    while c < len(lows):
        currclose = closes[c-1]
        lowestlow = float(find_hi_low(lows,scanvalue,'lowestlow',c))
        highesthigh = float(find_hi_low(highs,scanvalue,'highesthigh',c))
        Kperc = ((currclose - lowestlow)/ (highesthigh - lowestlow + 0.0000000001)) * 100
        Kpercarray.append(round(Kperc,1))
##        if Kperc < 0:
##            print currclose,lowestlow,highesthigh,Kperc,c,len(lows)
        c+=1
    return Kpercarray
###########################
def Stoch_CROSS(Karray,Darray):
    diffarray = difftwoarrays(Karray,Darray)
    return diffarray
###########################  
def RVIline(Kpercarray,emaval):
    Dpercarray =  EMAmvavgToArray(Kpercarray,emaval)
    return Dpercarray
###########################
def RVIsignal(opens,highs,lows,closes):
    c=1
    Kpercarray=[]
    while c < len(closes):
        currclose = closes[c-1]
        curropen = opens[c-1]
        currhi = highs[c-1]
        currlo = lows[c-1]
##        print currclose -curropen,currhi-currlo
##        lowestlow = float(find_hi_low(lows,scanvalue,'lowestlow',c))
##        highesthigh = float(find_hi_low(highs,scanvalue,'highesthigh',c))
        Kperc = ((currclose - curropen)/ (currhi - currlo + 0.0000000001)) * 1
        Kpercarray.append(round(Kperc,1))
##        if Kperc < 0:
##            print currclose,lowestlow,highesthigh,Kperc,c,len(lows)
        c+=1
    return Kpercarray
###########################
def RVI_CROSS(Karray,Darray):
    diffarray = difftwoarrays(Karray,Darray)
    return diffarray
###########################
def GetStates(arrayin,sym,Indtitle,dur,threshold,date):  #add barr age from last cross here
##    decimalboost = dboostdict[sym]
##    print 'getting states for...',Indtitle
    if len(arrayin)  > 3 :
        pass
    else:
        arrayin = [['ES', ' 2015-10-20 22:58:05',2019.5,2020.25,2019.5,2019.75,'full','60'],['ES', ' 2015-10-20 22:58:05',2019.5,2020.25,2019.5,2019.75,'full','60']]
    bsclose = strip1float(arrayin,5,sym) ##raw close price
    bs = bsclose
##    print Indtitle
    symES = 'ES'
##    date =  rpu_rp.todaysdateunix()  ##
    EsFile = rpu_rp.CsvToLines( DataDown+ date + '.'+symES+'.' + dur.replace(' ','') + '.both.csv')
    DurBothBoostedES = boost_pricearray(EsFile,symES)
    bsES = strip1float(DurBothBoostedES,5,'ES')
##    print sym,dur,Indtitle
    bsopen = strip1float(arrayin,2,sym) ##raw open price
    bshighs = strip1float(arrayin,3,sym)
##    bsvolume = strip1float(arrayin,6,sym)
    bslows = strip1float(arrayin,4,sym)
    bsbardiff = difftwoarrays(bsclose,bsopen)
    barrange = difftwoarrays(bshighs,bslows)
    barmids = difftwoarraysMIDS(bshighs,bslows)
    timestamparray = strip1string(arrayin,1)
    stochval = 14
    stochval2 = 3
    rvival = 4
    rvival2 = 10
    comparebs = rpu_rp.tail_array_to_array(bsclose,100)
    compareES = rpu_rp.tail_array_to_array(bsES,100)
    comparetimes = rpu_rp.tail_array_to_array(timestamparray,100)
##    print comparetimes
    stdvarbb = 1#.382
    bbandma = 20
    if Indtitle == 'pivot':
        indicator = pivotpoint(bshighs,bslows,bsclose)
        signindicator = indicator
    elif Indtitle == 'R1':
        indicator = RS1(bshighs,bslows,bsclose,'R')
        signindicator = indicator
    elif Indtitle == 'S1':
        indicator = RS1(bshighs,bslows,bsclose,'S')
        signindicator = indicator
    elif Indtitle == 'S2':
        indicator = RS2(bshighs,bslows,bsclose,'S')
        signindicator = indicator
    elif Indtitle == 'R2':
        indicator = RS2(bshighs,bslows,bsclose,'R')
        signindicator = indicator
    elif Indtitle == 'mcross':
        indicator = difftwoarrays(EMAmvavgToArray(bsclose,9),EMAmvavgToArray(bsclose,21))
        signindicator = indicator
    elif Indtitle == 'AO':
        indicator = difftwoarrays(SMAmvavgToArray(barmids,5),SMAmvavgToArray(barmids,34))
        signindicator = indicator
    elif Indtitle == 'AOAcc':
        indicator = difftwoarrays(difftwoarrays(SMAmvavgToArray(barmids,5),SMAmvavgToArray(barmids,34)),SMAmvavgToArray(difftwoarrays(SMAmvavgToArray(barmids,5),SMAmvavgToArray(barmids,34)),5))
        signindicator = indicator
    elif Indtitle == 'price':
        indicator = bsclose
        signindicator = bsbardiff
    elif Indtitle == 'highs':
        indicator = bshighs
        signindicator = bsbardiff
    elif Indtitle == 'lows':
        indicator = bslows
        signindicator = bsbardiff        
    elif Indtitle == 'mcd':
        indicator = MACDdiverg(bsclose)
        signindicator = indicator
    elif Indtitle == 'kupper':
        indicator = keltner_channels(bshighs,bslows,bsclose,2,'upper')
        signindicator = indicator
    elif Indtitle == 'klower':
        indicator = keltner_channels(bshighs,bslows,bsclose,2,'lower')
        signindicator = indicator
    elif Indtitle == 'stddev':
        indicator = stddev(bshighs,bslows,bsclose,bbandma)
        signindicator = indicator
    elif Indtitle == 'bbandlower':
        indicator = bbands(bshighs,bslows,bsclose,bbandma,stdvarbb,'lower')#simpleAvgVal,stdvariable)
        signindicator = indicator
    elif Indtitle == 'bbandupper':
        indicator = bbands(bshighs,bslows,bsclose,bbandma,stdvarbb,'upper')#simpleAvgVal,stdvariable)
        signindicator = indicator
    elif Indtitle == 'kmid':
        indicator = keltner_channel_mid(bshighs,bslows,bsclose,2)
        signindicator = indicator
    elif Indtitle == 'ema':
        indicator = EMAmvavgToArray(bsclose,21)
        signindicator = indicator
    elif Indtitle == 'sma200':
        indicator = mvavgToArray(bsclose,200)
        signindicator = indicator
    elif Indtitle == 'sma50':
        indicator = mvavgToArray(bsclose,50)
        signindicator = indicator
    elif Indtitle == 'sma100':
        indicator = mvavgToArray(bsclose,100)
        signindicator = indicator
    elif Indtitle == 'diffvES':
        indicator = diffvES(comparebs,compareES)
##        timestamparray = comparetimes
        signindicator = indicator
    elif Indtitle == 'RSI':
        indicator = RSI(bsclose,14)
        signindicator = indicator
    elif Indtitle == 'ROC':
        indicator = ROC(bsclose,9)
        signindicator = indicator
    elif Indtitle == 'StochD':
        indicator = StochD((StochK(bshighs,bslows,bsclose,stochval)),stochval2)
        signindicator = indicator   
    elif Indtitle == 'StochK':
        indicator = StochK(bshighs,bslows,bsclose,stochval)
        signindicator = indicator
    elif Indtitle == 'Stoch_CROSS':  
        indicator = Stoch_CROSS(StochK(bshighs,bslows,bsclose,stochval),StochD(StochK(bshighs,bslows,bsclose,stochval),stochval2))
        signindicator = indicator
    elif Indtitle == 'ATR':
        indicator = ATR(bshighs,bslows,bsclose,14)
        signindicator = indicator
    elif Indtitle == 'RVIline':
        ind1 = EMAmvavgToArray(RVIsignal(bsopen,bshighs,bslows,bsclose),rvival2)
        indicator = RVIline(ind1,rvival)
        signindicator = indicator   
    elif Indtitle == 'RVIsignal':
        indicator = EMAmvavgToArray(RVIsignal(bsopen,bshighs,bslows,bsclose),rvival2)
        signindicator = indicator
    elif Indtitle == 'RVI_CROSS':
        ind1 = EMAmvavgToArray(RVIsignal(bsopen,bshighs,bslows,bsclose),rvival2)
        ind2 = RVIline(ind1,rvival)
        indicator = RVI_CROSS(ind1,ind2)
        signindicator = indicator
        pass
    elif Indtitle == 'CMF':
        maVal=20
        indicator = bsclose #20 #'20' #CMF(bsclose,bslows,bshighs,bsvolume,maVal)
        signindicator = indicator
    else:
        print 'unknown indicator', Indtitle
    sign = show_sign(signindicator,Indtitle,threshold)
    if Indtitle == 'RSI':
        sign = show_sign2thresholds(signindicator,Indtitle,21,81)
    durarray =lableToarray(bsclose,dur)
    slope = show_slope(indicator,'value')
    slopetag = show_slope(indicator,'tagstyle')
    showcrxx = show_cross(sign,'noage')
    crossages = show_cross(sign,'crossage')
    stdval =  stddev(1,1,indicator,50)
##    print ' got here'
    
    if Indtitle == 'diffvES':
        arrayout = joinArraysStates(comparetimes,indicator,sign,slope,slopetag,Indtitle,sym,showcrxx,durarray,bshighs,bslows,bsclose,crossages,stdval)
    else:
        arrayout = joinArraysStates(timestamparray,indicator,sign,slope,slopetag,Indtitle,sym,showcrxx,durarray,bshighs,bslows,bsclose,crossages,stdval)
    alist = timestamparray,indicator,sign,slope,slopetag,Indtitle,sym,showcrxx,durarray,bshighs,bslows,bsclose,crossages,stdval
    prevlena = 0
##    print 'joining states'
    return arrayout
###########################  RVI      
##%K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
##%D = 3-day SMA of %K
##Lowest Low = lowest low for the look-back period
##Highest High = highest high for the look-back period
##%K is multiplied by 100 to move the decimal point two places
