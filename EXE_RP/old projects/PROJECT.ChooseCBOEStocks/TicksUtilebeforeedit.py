# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rpu_rp, rpInd
from datetime import datetime
import datetime as dt
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
#######################################
today =  rpu_rp.todaysdateunix()  ##
##today ='20150619'
time_format = "%H:%M:%S"
spaceYtime_format = ' %Y-%m-%d %H:%M:%S'
#########################
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
modedict = rpu_rp.create_dict(libbars,0,5)

symdict = rpu_rp.create_dict(libsyms,0,1)
##########################################################
def merge_bar_files(filename,cutoffmintime):
    outfile = filename.replace('ddload.csv','both.csv')       
    recentfile = filename.replace('ddload.csv','recent.csv')
    cleanrecentfile = filename.replace('ddload.csv','cleanrecent.csv')   
    rlines = rpu_rp.CsvToLines(recentfile)
    cleanrlines =[]     
    for rline in rlines:
        bartime = rline[1]      
        bartime_epoch = int(time.mktime(time.strptime(bartime, spaceYtime_format)))
        if bartime_epoch > ((ddload_cutoff_epoch(filename,'newformat'))+ cutoffmintime) and len(rline) > 3:
            cleanrlines.append(rline)
    rpu_rp.WriteArrayToCsvfile(cleanrecentfile,cleanrlines)
                            
    destination = open(outfile,'wb')
    shutil.copyfileobj(open(filename,'rb'), destination)
    shutil.copyfileobj(open(cleanrecentfile,'rb'), destination)
    destination.close()
    lines = rpu_rp.CsvToLines(outfile)  ## creating bothfile here
    return lines
##############################################
def format_lines(arrayin,tailamt):
    formatl ='%11s %13s %11s %8.2f  %8.2f %11s %9s '
    linenum = 0
    cutoff = len(arrayin) - tailamt
    for line in arrayin:
        time = line[0]
        price = float(line[3])
        pslope = line[1]
        psign = line[2]
        mcd = float(line[4])
        mslope = line[5]
        msign = line[6]
        linenum +=1
        if linenum > cutoff:
            print (formatl % (time,pslope,psign,price,mcd,mslope,msign))
##################################
def ddload_cutoff_epoch(histfilename,formatchoice):
    if formatchoice == 'oldformat':
        formatstring = '%H:%M:%S'
    else:
        formatstring = ' %Y-%m-%d %H:%M:%S'
    try:
        rpu_rp.tail_to_txtfile(histfilename,1,TMP +'outfile') ## get last line of historical file for time check
        oneline = rpu_rp.catstring(TMP +'outfile') ## this is the last line
        timeofbar = (oneline.split(',')[1])
        epochtimeofbar = int(time.mktime(time.strptime(timeofbar, formatstring)))
    except:
        timeofbar =' 2015-03-01 23:59:58'
        print 'bombed getting ddload cutoff time in TicksUtile here'
##        rpu_rp.tail_to_txtfile(histfilename,1,TMP +'outfile') ## get last line of historical file for time check
##        oneline = rpu_rp.catstring(TMP +'outfile') ## this is the last line
##        timeofbar = (oneline.split(',')[1])
##        print timeofbar
        epochtimeofbar = int(time.mktime(time.strptime(timeofbar, formatstring)))
    return epochtimeofbar
##################################
def create_bars_from_bars(bararrayin,today,sym,dur,durinseconds):
    #############
    import time
    startbartime = ddload_cutoff_epoch(DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.ddload.csv','normal')
    barhi = float(0)
    barlo = float(99999999)
    tickcount = tottickcount = 0
    bararrayout =[]
    timearray =[]
    prevhi =  prevlo =   0
    totallength = len(bararrayin)
    prevbar_time = ' 2015-06-01 00:01:01'
    prevbar_time_dt = dt.datetime.strptime(prevbar_time, spaceYtime_format)
    prevbar_time_epoch =  int(time.mktime(time.strptime(prevbar_time, spaceYtime_format)))
    prevdurbar_epoch = 0
    ##################
    recentfile = DataDown +today+'.'+sym+ '.' +dur.replace(' ','')+  '.recent.csv'
##    flush the recentfile
    rpu_rp.WriteArrayToCsvfile(recentfile,[])
    ######################
    firsttripflag = 'notstarted'
    for line in bararrayin:
        if len(line) > 3:
    ##        print line
            bar_time = line[1]
            if bar_time ==  '1':
                bar_time = ' 2015-06-01 00:01:01' 
            bar_time_dt = dt.datetime.strptime(bar_time, spaceYtime_format)
            bar_time_epoch =  int(time.mktime(time.strptime(bar_time, spaceYtime_format)))
            openpr = float(line[2])
            highpr = float(line[3])
            lowpr = float(line[4])
            closepr = float(line[5])
            ############                     
            barTobarElapsed = bar_time_epoch - prevbar_time_epoch
            barToprevdurbarElapsed = bar_time_epoch - prevdurbar_epoch
            prevbar_time_epoch = bar_time_epoch
            ##################
            tottickcount +=1   
            ##########        
            testval = int(durinseconds) - barToprevdurbarElapsed
            tickcount +=1
            if highpr > barhi:
                barhi = highpr
            if lowpr < barlo:
                barlo = lowpr
            if tickcount == 1:
                baropen = openpr
                newbartime = bar_time
                #############
            setflag= 'skip'
            if int(durinseconds) > 5:
                resetamt = 5
                pass
            else:
                resetamt = 0
            if tottickcount == 1  :
                setflag = 'noreset'
            elif bar_time_epoch > (startbartime + int(durinseconds) - resetamt) and firsttripflag != 'started':
    ##            print 'tripped',dur,sym,bar_time_epoch,startbartime,bar_time
                setflag = 'reset'
                firsttripflag = 'started'
            elif testval <= 0 :
                setflag = 'reset'
            elif  tottickcount == totallength:
                setflag = 'reset'
            else:
                setflag = 'skip'
            if setflag == 'reset' and len(line) > 3:
                tickcount =0          
                barline =[]
##                barclose = closepr
                partbar = True
                partflag = 'full'
                if tottickcount == totallength:
                    time = ' 2019-03-03 03:03:03' 
                    partbar = True
                    partflag = 'partial'
                    setflag = 'reset'
                barline.append(sym)
                barline.append(newbartime)
                barline.append(baropen)
                barline.append(barhi)
                barline.append(barlo)              
                barline.append(closepr)
                barline.append(partflag)
                barline.append(barToprevdurbarElapsed)
                prevdurbar_epoch = bar_time_epoch
                if partbar == True:
                    bararrayout.append(barline)
                barhi = 0
                barlo = 99999999
            
    rpu_rp.WriteArrayToCsvfileAppend(recentfile,bararrayout)
    return bararrayout
##################
def format_RTTicks_to_5secBars(arrayin,sym):
    arrayout = []
    spaceYtime_format = ' %Y-%m-%d %H:%M:%S'
    for line in arrayin:
        oneline =[]
        txttoremove = ['reqId',',','\'','time','open','high','low','close','volume','wap','count',' ']
        parsedline = str(line)
        for item in txttoremove:
            parsedlinenew = parsedline.replace(item,'')
            parsedline = parsedlinenew
        line = parsedlinenew.split('=')
        epochstring = (line[2])
        timedate = datetime.fromtimestamp(float(epochstring)).strftime(spaceYtime_format)
        openpr = float(line[3])
        highpr = float(line[4])
        lowpr = float(line[5])
        closepr = float(line[6])
        oneline.append(sym)
        oneline.append(timedate)
        oneline.append(openpr)
        oneline.append(highpr)
        oneline.append(lowpr)
        oneline.append(closepr)
        oneline.append(sym)
        arrayout.append(oneline)
    return arrayout
############################
def align_tickfile(cutofftime,tickfile):
    tempfile = tickfile.replace('.csv','temp.csv')
    tempout = 'bla'
    bufile = tickfile.replace('.csv','bu.csv')
    shutil.copyfile(tickfile,bufile)
    
    rlines = rpu_rp.CsvToLines(tickfile)
    cleanrlines =[]
    for rline in rlines:
        bartime = rline[1]      
        bartime_epoch = int(time.mktime(time.strptime(bartime, spaceYtime_format)))
        if bartime_epoch > cutofftime:
            cleanrlines.append(rline)
    rpu_rp.WriteArrayToCsvfile(tempfile,cleanrlines)
    shutil.copyfile(tempfile,tempout)
##############################################
##histfilename= data  +15secs.csv'
##tickfile = '5 secs'
##align_tickfile(ddload_cutoff_epoch(histfilename,'spaceY'),tickfile)
def prepare_tickfilesto5secBars(today,sym):
    RTticksFile = DataDown +today+'.'+sym+ '.RTticks.csv'
    RTBarsin = rpu_rp.CsvToLines(RTticksFile)
    RTTickBarsReformatted = format_RTTicks_to_5secBars(RTBarsin,sym)

    RTbothFile = DataDown +today+'.'+sym+ '.both.csv'
    if os.path.isfile(RTticksFile) :
        RTBars5Sec = create_bars_from_bars(RTTickBarsReformatted,today,sym,'5secs',1) #. .. this creates the recent file 5secs used in merge_bar
    else:
        RTBars5Sec = create_bars_from_bars(RTbothFile,today,sym,'5secs',1)
        ##RTticks > RTbars[5secRecentBars]
    filetomerge = DataDown +today+'.'+sym+'.'+'5secs'+'.ddload.csv'
    cutoffmintime = int(2)
    merge_bar_files(filetomerge,cutoffmintime)  #this creates the both file using ddload and recent....
    return 
##############
def assemble_dur_bars(today,sym,dur,durinseconds):   
    Bars5secBothfile = DataDown +today+'.'+sym+'.'+'5secs'+'.both.csv'
    Bars5secBoth = rpu_rp.CsvToLines(Bars5secBothfile)
    create_bars_from_bars(Bars5secBoth,today,sym,dur,durinseconds) ## writes recent for each dur
    ## merge  the dur ddload with  dur recents > dur boths
    filetomerge = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.ddload.csv'
    cutoffmintime = int(int(durinseconds) - 5)
    merge_bar_files(filetomerge,cutoffmintime)  #this creates the both file 
####################
def create_state_files(today,sym,dur,indicator):   
    outfile = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.' + indicator + 'state.csv'
    infile = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.both.csv'
    arrayin = rpu_rp.CsvToLines(infile)
    arrayout = rpInd.GetStates(arrayin,sym,indicator)
    rpu_rp.WriteArrayToCsvfile(outfile,arrayout)
