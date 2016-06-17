# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles, rpu_rp, rpInd
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
#######################################
##files = ['ibhistdata.5 mins.2 D.20150428.GBP.csv'
today =  rpu_rp.todaysdateunix()
files =  glob.glob(EXE+ 'IbPy-master/' + today + '*EUR*.csv')
print files                  
##                   'ibdata.15mins.2D.*514.ES.csv')
### the recent trick will not work with multiple files
#############################################
### need to add swingpoint finder on hi los from 5 second bars######
##############################################
for inputfile in files:
    print inputfile
    rpInd.prepare_tick_files(inputfile,'tempbars.csv')
    lines = rpu_rp.CsvToLines('tempbars.csv')
#######################
    if 'ES' in str(inputfile):
        decimalboost = 1
    elif 'USD' in str(inputfile):
        decimalboost= 100
    else:
        decimalboost = 1000 
    ################
    bs = rpInd.strip1value(lines,5) ##raw close price
    bsshort = bs[0:100]
    bshighs = rpInd.strip1value(lines,3)
    bslows = rpInd.strip1value(lines,4)
    timestamparray = rpInd.strip1value(lines,1)
    ########################
    sma26 = rpInd.EMAmvavgToArray(bs,26)
    sma12 = rpInd.EMAmvavgToArray(bs,12)
    diffs = rpInd.difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = rpInd.EMAmvavgToArray(diffs,9)
    macddiverg = rpInd.difftwoarrays(diffs,macdavg)
    datearray = rpInd.strip1string(lines,1)

    testlevel = float(10)
                      ########## 
    RSIgain = rpInd.RSIGainLoss(bs,'gain')
    RSIloss = rpInd.RSIGainLoss(bs,'loss')
    rsiavggain = rpInd.RSImvavgToArray(RSIgain,14)
    rsiavgloss = rpInd.RSImvavgToArray(RSIloss,14)
##    print rsiavgloss
    RS = rpInd.ratiotwoarrays(rsiavggain,rsiavgloss)    
##    rsi = 100 - ( 100 / (1 + RS))
    rsiArray =[]
    for ratio in RS:
        rsi = min(100,(100 - ( 100 / (1 + ratio))))
        rsiArray.append(rsi)
        #################
##    print_arrays(datearray,macddiverg,rawprice,decimalboost,testlevel,'tested' + str(testlevel) +' '+inputfile)
##    K = rpInd.create_stoch(bs,bshighs,bslows,14,'K')
##    D = rpInd.mvavgToArray(K,3)
##    KDsprd = rpInd.difftwoarrays(K,D) ## K breaks below D = sell
##    DSLOPE = rpInd.AddSlopeToArray(D)
##    slopeseries = rpInd.join_arrays_toarray(D,KDsprd,K,bs,timestamparray,3,30)
##    rpInd.format_arrays(slopeseries,'formatmode')
    tenkan = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,9)
    kijunSen = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,26)
    barSMA50  = rpInd.mvavgToArray(bs,50)
    diff = rpInd.difftwoarrays(barSMA50,bs)
    diff = rpInd.difftwoarrays(tenkan,kijunSen) 
    slopeseries = rpInd.join_arrays_toarray(bs,kijunSen,diff,tenkan,timestamparray,3,300)
##    rpInd.format_arrays(slopeseries,'formatmode')
    seeks = rpInd.seek_crossover_2_arrays(diff,bs,timestamparray)
    slopeseries = rpInd.join_arrays_toarray(bs,kijunSen,diff,tenkan,timestamparray,3,300)
##    print seeks    
##    rpInd.create_bars(arrayin,barticksize,bartimesize,mode)
##    newbars = rpInd.create_bars(lines,9,10000,'fullbar') # justtick,justtime, keep time to large number to ignore timebar function   
##    slopeseries =  seek_crossover_2_arrays(K,D,'vals',bs)
    ### k - D is positive after the cross, buy sig    
    ## D 1st bar sloping down and over 80
##    bla = join_2_arrays(K,D)
    ##    test_study_values(timestamparray,valuearray,pricearray,decimalboost,testlevela2,linetext)##########    this is stochastic stuff
##############    bla2 = test_stoch_values(timestamparray,Dval,bs,1,10,linetext)
##    for val in K:
##        print val,'this is stoch 1min'
## need to look for crossovers and add slope
'''
TenkanSenmvavgToArray(arrayhighs,arraylows,smaNum):
C:\Users\bob\GDRIVE\EXE_RP\IbPy-master>grep def rpI*
def strip1string(multilinearrayin,fieldnum):
def strip1value(multilinearrayin,fieldnum):
def mvavgToArray(arrayin,smaNum):
def RSImvavgToArray(arrayin,smaNum):
def RSIToArray(arrayin,smaNum):
def RSIGainLoss(arrayin,gainmode):
def AddSlopeToArray(arrayin):
def EMAmvavgToArray(arrayin,smaNum):
def difftwoarrays(a1,a2):
def ratiotwoarrays(a1,a2):
def print_arrays(a1,a2,a3,decimalboost,testlevela2,linetext):
def test_study_values(timestamparray,valuearray,pricearray,decimalboost,testlevela2,linetext):
def test_stoch_values(timestamparray,valuearray,pricearray,decimalboost,testlevela2,linetext):
def join_arrays(array1,array2,array3,formatmode,priceseries,joinnum,trimmernum):  ## assumes one field in postion 0
def join_arrays_toarray(array1,array2,array3,array4,array5,joinnum,trimmernum):  ## assumes one field in postion 0
def format_arrays(array1,formatmode):  ## assumes one field in postion 0
def create_stoch(arrayclose,arrayhis,arraylows,barticksize,mode):
def clean_oner_bars(filename):
def seek_crossover_2_arrays(a1,a2,formatmode,priceseries):  ## assumes one field in postion 0
def prepare_tick_files(filename,outfname):
    ##########################################
'''
