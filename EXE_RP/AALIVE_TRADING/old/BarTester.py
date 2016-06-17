# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import  rpu_rp, rpInd
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
#######################################
today =  rpu_rp.todaysdateunix()
##today ='20150527'
### need to add swingpoint finder on hi los from 5 second bars######
##############################################
#######################
def createlines(fname):
    print inputfile
    rpInd.prepare_tick_files(inputfile,'tempbars.csv')
    lines = rpu_rp.CsvToLines('tempbars.csv')
    return lines
###############################
global decimalboost
global tailstart
##########################################
def process_ticks(lines,decimalboost):
    ################
    bs = rpInd.strip1value(lines,5) ##raw close price
    lenbs = len(bs)
    tailstart = lenbs - 50
    print tailstart,'tailstart'
    ###############
    bsshort = bs[0:1000000]
    bshighs = rpInd.strip1value(lines,3)
    bslows = rpInd.strip1value(lines,4)
    timestamparray = rpInd.strip1value(lines,1)
    ########################
    sma26 = rpInd.EMAmvavgToArray(bs,26)
    sma12 = rpInd.EMAmvavgToArray(bs,12)
    sma50 = rpInd.EMAmvavgToArray(bs,50)
    macddiff = rpInd.difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = rpInd.EMAmvavgToArray(macddiff,9)
    macddiverg = rpInd.difftwoarrays(macddiff,macdavg)
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
    tenkan = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,9)
    kijunSen = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,26)
    #######################
    barSMA50  = rpInd.mvavgToArray(bs,50)
    diff = rpInd.difftwoarrays(barSMA50,bs)
    diff = rpInd.difftwoarrays(tenkan,kijunSen)
    slope50 = rpInd.show_slope(barSMA50)
    sign50 = rpInd.show_sign_and_crosses(macddiverg)
##    newarray = rpInd.join_8arrays_to_1_array(timestamparray,bs,sma26,sma12,sma50,macddiverg,tenkan,kijunSen,'mode')
    newarray = rpInd.join_8arrays_to_1_array(timestamparray,slope50,sign50,bs,sma50,macddiverg,tenkan,kijunSen,'3strings')
##    farray = rpInd.format_arrays(newarray,3)
    ##backtest_sigs(arrayin,texttosell,texttobuy,pricefnum)
##    rpInd.backtest_sigs(newarray[0:600000],'negcross','poscross',3)
##    rpInd.backtest_sigs(newarray[tailstart:600000],'slope','slope',3)
    rpInd.show_test_lines(newarray[tailstart:600000],'negnegcross','posposcross',3)
    rpInd.show_macd_low_lines(newarray[tailstart:600000],'negnegcross','posposcross',3,(0.005/decimalboost))

    
    ################################################
durationselect = '4 D15 mins'
files =  glob.glob(EXE+ 'IbPy-master/' + today + '.*.' +durationselect + '*.csv') #[date 5 mins.2 D.GBP.csv
print files
#############################################
for inputfile in files:  
    sym = inputfile.split('.')[1]
    print sym
    ticklines = rpu_rp.CsvToLines(today + '.' + sym + '.ticksnaps.csv')
    newbars =   rpInd.create_bars(ticklines,5000,900,'fullbar','snapshot', sym)
    rpu_rp.WriteArrayToCsvfile(today + '.' + sym+ '.recent'+ durationselect + '.csv',newbars)
    lines = createlines(inputfile)
    if 'ES' in str(inputfile) or 'NQ' in str(inputfile):
        decimalboost = 1
    elif 'USD' in str(inputfile):
        decimalboost= 100
    else:
        decimalboost = 1000
    process_ticks(lines,decimalboost)
    raw_input('click to continue ' + sym )
##########################################          
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
