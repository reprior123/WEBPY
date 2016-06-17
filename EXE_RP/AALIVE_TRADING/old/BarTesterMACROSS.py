# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
#####################
import  rpu_rp, rpInd
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
#######################################
today =  rpu_rp.todaysdateunix()
##today ='20150528'
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
    bs = float(rpInd.strip1value(lines,5))* float(decimalboost) ##raw close price
    bshighs = rpInd.strip1value(lines,3)
    bslows = rpInd.strip1value(lines,4)
    timestamparray = rpInd.strip1value(lines,1)
    lenbs = len(bs)
    tailstart = lenbs - 50
    print tailstart,'tailstart'
    ########################
    sma21 = rpInd.mvavgToArray(bs,21)
    sma9 = rpInd.mvavgToArray(bs,9)
    ema21 = rpInd.EMAmvavgToArray(bs,21)
    ema9 = rpInd.EMAmvavgToArray(bs,9)    
    sma50 = rpInd.EMAmvavgToArray(bs,50)
    sma12 = rpInd.EMAmvavgToArray(bs,12)
    ################  MACD   ##########
    macddiff = rpInd.difftwoarrays(rpInd.EMAmvavgToArray(bs,12),rpInd.EMAmvavgToArray(bs,26))## macd is the mvavg9 on this diff
    macdavg = rpInd.EMAmvavgToArray(macddiff,9)
    macddiverg = rpInd.difftwoarrays(macddiff,macdavg)
    ########## RSI   #######
    RSIgain = rpInd.RSIGainLoss(bs,'gain')
    RSIloss = rpInd.RSIGainLoss(bs,'loss')
    rsiavggain = rpInd.RSImvavgToArray(RSIgain,14)
    rsiavgloss = rpInd.RSImvavgToArray(RSIloss,14)
    RSratios = rpInd.ratiotwoarrays(rsiavggain,rsiavgloss) ##    rsi = 100 - ( 100 / (1 + RS))
    rsiArray =[]
    for ratio in RSratios:
        rsi = min(100,(100 - ( 100 / (1 + ratio))))
        rsiArray.append(rsi)
    #################
    tenkan = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,9)
    kijunSen = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,26)
    diff = rpInd.difftwoarrays(tenkan,kijunSen)
    #######################
    MA9CROSS21 = rpInd.difftwoarrays(sma9,sma21)
    ######################
    signbs = rpInd.show_sign(bs,'price')
    slopebs = rpInd.show_slope(bs,'price')

    signmcd = rpInd.show_sign(macddiverg,'mcd')
    crossesmcd = rpInd.show_crossover(signmcd,'mcd')
    slopemcd = rpInd.show_slope(macddiverg,'macddiverg') 

    CLVarr = rpInd.CLV_Value(bs,bslows,bshighs)##    CLVarr = CLV_Value(Carray,Larray,Harray)
    print len(bslows)
    MDarray = rpInd.makearrayJust2(timestamparray,slopebs,signbs,bs,macddiverg,crossesmcd,slopemcd)
    macdcrosses = rpInd.show_macd_low_lines(MDarray,'Slope','Slope',3,.001,4)#(arrayin,texttosell,texttobuy,pricefnum,macdtestval,macdfnum)
    ma = rpu_rp.grep_array_to_array(macdcrosses,'up')
    rpInd.format_lines(ma)
##    CrossMAarray = rpInd.join_8arrays_to_1_array(timestamparray,slope,sign,bs,sma21,MA9CROSS21,CLVarr,kijunSen,'3strings')
##    rpInd.show_test_lines(CrossMAarray,'negnegcross','posposcross',3,(1.0/decimalboost))

##    CLVarray = rpInd.join_8arrays_to_1_array(timestamparray,slope,sign,bs,sma21,CLVarr,CLVarr,kijunSen,'3strings')
##    rpInd.show_test_lines(CLVarray,'negnegcross','posposcross',3,(1.0/decimalboost))
    print 'timestamparray,slope,sign,bs,sma21,CLVarr,CLVarr,kijunSen,'   
##    cross test needs to work on variable fields
##    slope test needs to work on variable...
##    print CLVarr
##    show_macd_low_lines  
    ################################################
durationselect = '3 M1 Day'
durationselect = '4 D15 mins'
durationselect = '4 D5 mins'
files =  glob.glob(DataDown+ today + '.EUR.' +durationselect + '*.csv') #[date 5 mins.2 D.GBP.csv
print files
#############################################
for inputfile in files:  
    sym = inputfile.split('.')[1]
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
    raw_input('click to continue ' + sym + inputfile)
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
