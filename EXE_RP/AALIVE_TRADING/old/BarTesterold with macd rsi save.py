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
##############################################
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
    bs = rpInd.strip1float(lines,5,decimalboost) ##raw close price
    bshighs = rpInd.strip1float(lines,3,decimalboost)
    bslows = rpInd.strip1float(lines,4,decimalboost)
    timestamparray = rpInd.strip1string(lines,1)
    lenbs = len(bs)
    tailstart = lenbs - 50
    print tailstart,'tailstart'
    ########################
##    sma21 = rpInd.mvavgToArray(bs,21)
##    sma9 = rpInd.mvavgToArray(bs,9)
##    ema21 = rpInd.EMAmvavgToArray(bs,21)
##    ema9 = rpInd.EMAmvavgToArray(bs,9)    
##    sma50 = rpInd.EMAmvavgToArray(bs,50)
##    sma12 = rpInd.EMAmvavgToArray(bs,12)
##    ################  MACD   ##########
##    macddiff = rpInd.difftwoarrays(rpInd.EMAmvavgToArray(bs,12),rpInd.EMAmvavgToArray(bs,26))## macd is the mvavg9 on this diff
##    macdavg = rpInd.EMAmvavgToArray(macddiff,9)
##    macddiverg = rpInd.difftwoarrays(macddiff,macdavg)
    ########## RSI   #######
##    RSIgain = rpInd.RSIGainLoss(bs,'gain')
##    RSIloss = rpInd.RSIGainLoss(bs,'loss')
##    rsiavggain = rpInd.RSImvavgToArray(RSIgain,14)
##    rsiavgloss = rpInd.RSImvavgToArray(RSIloss,14)
##    RSratios = rpInd.ratiotwoarrays(rsiavggain,rsiavgloss) ##    rsi = 100 - ( 100 / (1 + RS))
##    rsiArray =[]
##    for ratio in RSratios:
##        rsi = min(100,(100 - ( 100 / (1 + ratio))))
##        rsiArray.append(rsi)
    #################
##    tenkan = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,9)
##    kijunSen = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,26)
##    diff = rpInd.difftwoarrays(tenkan,kijunSen)
    #######################
##    MA9CROSS21 = rpInd.difftwoarrays(sma9,sma21)
    ######################
    signbs = rpInd.show_sign(bs,'price')
    slopebs = rpInd.show_slope(bs,'price')

##    signmcd = rpInd.show_sign(macddiverg,'mcd')
##    crossesmcd = rpInd.show_crossover(signmcd,'mcd')
##    slopemcd = rpInd.show_slope(macddiverg,'macddiverg')
    ##### MA Cross ##
    macrossval = rpInd.difftwoarrays(rpInd.EMAmvavgToArray(bs,9),rpInd.EMAmvavgToArray(bs,21))
    signmcd = rpInd.show_sign(macrossval,'mcd') 
    crossesmcd = rpInd.show_crossover(signmcd,'mcd')
    slopemcd = rpInd.show_slope(macrossval,'mcd')
    print len(signmcd),len(macrossval),len(crossesmcd)
    MDarray = rpInd.makearrayJust2(timestamparray,slopebs,signbs,bs,macrossval,crossesmcd,signmcd)
##    macdcrosses = rpInd.show_macd_low_lines(MDarray,'Slope','Slope',3,.001,4)#(arrayin,texttosell,texttobuy,pricefnum,macdtestval,macdfnum)
    ma = rpu_rp.grep_array_to_array(MDarray,'cross')
    rpInd.format_lines(ma,5)  #tailamount
    ################################################
##    setup aloop for time durations
durationselect = '4 D15 mins' ## this has to match timebarforsnaps
files =  glob.glob(DataDown+ today + '.EUR.' +durationselect + '*.csv') #[date 5 mins.2 D.GBP.csv
print files
#############################################
for inputfile in files:  
    sym = inputfile.split('.')[1]
    ticklines = rpu_rp.CsvToLines(today + '.' + sym + '.ticksnaps.csv')
    lastline = rpu_rp.tail_to_txtfile(inputfile,2,'outfile')
    strings= rpu_rp.catstring('outfile')
    fulldatetime = strings.split(',')[1]
    time = fulldatetime.split()[1]
    hourmincutoff = time.split(':')[0] + time.split(':')[1]
    print hourmincutoff
    timebarforsnaps = 900
    newbars =   rpInd.create_bars(ticklines,5000,timebarforsnaps,'fullbar','snapshot', sym,hourmincutoff) #field three is timesize in seconds
##        ## idendify last line of historical as 9:05
##        meld the ticksaps bars to  historical
##        EUR, 2015-06-04 09:05:00, 1.12455, 1.12485, 1.12425, 1.1246, -1
##    the last minute of the main bars = ?
##    tail last line of inputfile
    rpu_rp.WriteArrayToCsvfile(DataDown+today + '.' + sym+ '.recent'+ durationselect + '.csv',newbars)
    lines = createlines(inputfile)
    if 'ES' in str(inputfile) or 'NQ' in str(inputfile):
        decimalboost = 1
    elif 'USD' in str(inputfile):
        decimalboost= 100
    else:
        decimalboost = 100
    process_ticks(lines,decimalboost)
    raw_input('click to continue ' + sym + inputfile)
##########################################          
