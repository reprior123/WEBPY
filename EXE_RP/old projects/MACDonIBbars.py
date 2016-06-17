# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_ACTANT/'
localtag = '_ACTANT'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles, rpu_rp
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
#######################################
##inputfile = 'ibhistdata.15 mins.2 D.20150428.EUR.csv'
##lines = rpu_rp.CsvToLines(inputfile)
###########################################
def strip1string(multilinearrayin,fieldnum):
    arrayout = []
    for line in multilinearrayin:
        arrayout.append(line[fieldnum])
    return arrayout    
###############
def strip1value(multilinearrayin,fieldnum):
    arrayout = []
    for line in multilinearrayin:
        arrayout.append(float(line[fieldnum]))
    return arrayout    
#####################################    ##############
def mvavgToArray(arrayin,smaNum):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    while barnum < numbars:
        if barnum < smaNum:
            tot += arrayin[barnum]
            diviser = barnum + 1
        else:
            tot += arrayin[barnum] - arrayin[barnum-smaNum]
            diviser = smaNum
        smaval = tot/diviser
        barnum +=1
        arrayout.append(smaval)
    return arrayout
############################
def EMAmvavgToArray(arrayin,smaNum):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    multiplier = round(float(2.0/(smaNum+1)),4)
    while barnum < numbars:
        if barnum < smaNum:
            tot += arrayin[barnum]
            diviser = barnum + 1
            prevema = tot/diviser
            ema = prevema
        else:
            tot += arrayin[barnum] - arrayin[barnum-smaNum]
            ema = ((arrayin[barnum] - prevema) * multiplier) + prevema
            diviser = smaNum
        smaval = tot/diviser
        barnum +=1
        prevema = ema
        arrayout.append(ema)
    return arrayout
######################################
def difftwoarrays(a1,a2):
    alength = len(a1)
    arrayout =[]
    c = 0 
    while c < alength:
        diff = a1[c] - a2[c]
        arrayout.append(diff)
        c += 1
    return arrayout
#####################
def print_arrays(a1,a2,a3):
    barnum = 0
    numbars = len(a1)
    print numbars
    while barnum < numbars:
        if round(1000*a2[barnum],2) > -0.03 and round(1000*a2[barnum],2) < 0.03:
            print a1[barnum],round(1000*a2[barnum],2),round(float(a3[barnum]),4)
        barnum +=1
#######################################
files = ['ibhistdata.15 mins.2 D.20150428.GBP.csv', 'ibhistdata.15 mins.2 D.20150428.EUR.csv']
for inputfile in files:
    print inputfile
    ##inputfile = 'ibhistdata.15 mins.2 D.20150428.EUR.csv'
    lines = rpu_rp.CsvToLines(inputfile)
    ###########################################
    bs = strip1value(lines,5)
    sma26 = EMAmvavgToArray(bs,26)
    sma12 = EMAmvavgToArray(bs,12)
    ##print len(sma26), len(sma12)
    diffs = difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = EMAmvavgToArray(diffs,9)
    macddiverg = difftwoarrays(diffs,macdavg)
    datearray = strip1string(lines,1)
    rawprice = strip1value(lines,5)
    print_arrays(datearray,macddiverg,rawprice)
###########################
####################################
#####################
def join_2_arrays(array1,array2):  ## assumes one field in postion 0
    ## check if arrays are same length
    print 'array2 is x long',len(array2)
    print 'array1 is x long',len(array1)
    arrayout =[]
    c=0
    if len(array1) == len(array2):
        while c < len(array2):
            print(' %s %8.2f %8.2f' % (array1[c],array2[c],round(priceseries[c],4)))
##            arrayout.append(diff)
            c+=1
##    return arrayout
##############################################
