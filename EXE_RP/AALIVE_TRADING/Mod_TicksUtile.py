################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open('importmodlist.txt').readlines()
for module in moduleNames:
    if module != titleself:
        my_module = importlib.import_module(module.strip())
######################
ftnodashspace = ' %Y%m%d %H:%M:%S'
ftdashnospace = '%Y-%m-%d %H:%M:%S'
#################################
print 'loading ticks'
def convertTime(timestring,formatout,direction):
    if direction == 'timetoepoch':            
        if  formatout == 'dashspace':
            formatstring = spaceYtime_format
        elif formatout == 'nodashspace': #time_to_epochold
            formatstring = ftnodashspace
        elif formatout == 'dashnospace': #time_to_epochnospace
            formatstring = ftdashnospace
        else:
            print 'need correct format arg in timeto epoch'
        output = int(time.mktime(time.strptime(timestring, formatstring))) ### above is timetoepoch     
    else:
        epoch = timestring
        output = datetime.fromtimestamp(float(epoch)).strftime(spaceYtime_format) #epoch_to_time
    return output
##########################################################
def throw_out_lastbar(f):
##    f = DataDown+ date + '.' + sym + '.'  + dura.replace(' ','') +'.ddload.csv'
    lines = rpu_rp.CsvToLines(f)
    c=0
    newarr = []
    for l in lines:
        c+=1
        if c < len(lines):
            newarr.append(l)
    rpu_rp.WriteArrayToCsvfile('tmp',newarr)
    shutil.copyfile('tmp',f)
####################################
def merge_bar_files(filerecent,fileddload,fileboth,cutoffmintime):
    cutofftimeEpoch = last_bar_epoch(fileddload,'noround')
    # last_bar_epoch(filename,roundformat) 
    recentlines = rpu_rp.CsvToLines(filerecent)  ## usually dload
    ddloadlines = rpu_rp.CsvToLines(fileddload) ## usually recent
    ddloadlineslen = len(ddloadlines)
    cleanrlines =[]     
    for rline in recentlines:
        if len(rline) > 2:
            bartime_epoch =  convertTime(rline[1],'dashspace','timetoepoch')
##            print bartime_epoch, rline[1], cutofftimeEpoch,cutoffmintime
            if bartime_epoch > (cutofftimeEpoch + cutoffmintime) and len(rline) > 3:
                ddloadlines.append(rline)
##    print 'dloadfile premerge len = ',ddloadlineslen, 'recfile len = ',len(recentlines),'merged = ',len(ddloadlines)
    rpu_rp.WriteArrayToCsvfile(fileboth,ddloadlines) ## bothfile outfile created here
##############################################
def createMultiDay_bar_files(sym,dur,baseroot):
##    merge_bar_files(file1,file2,outfile,cutoffmintime):
##    baseroot = '.both.csv'
    rootname ='.multiday' + baseroot
    outfile = DataDown +'multiday'+'.'+sym+'.'+dur.replace(' ','')+rootname
    filelist = glob.glob(DataDown + '201509*' + '.'+sym+'.'+dur.replace(' ','')+baseroot)
    tempout = 'tmp'
    c=0
    for file2 in filelist:
        c+=1
        file1 = outfile
        if c == 1:
            file1 = file2
        print file1,file2
        merge_bar_files(file1,file2,tempout,0)
        shutil.copyfile(tempout,outfile)
#################################
def last_bar_epoch(filename,roundformat): #'rounded or noround  #last_bar_epochrounded
##    from datetime import date, timedelta, datetime, time
    from datetime import  datetime, timedelta
    twolines =[]
    try:
        if 'both' in filename:
            stag = 'partial'
        else:
            stag = 'xxcxxx'
        twolines = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filename),2)
##        print twolines
        for line in twolines:  ### the both file has partial tag, ddload does not
            if stag  not in str(line):
                timeofbar = line[1]
##                print timeofbar
        if len(twolines) == 0:
            lastlines = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(filename),2)
            timeofbar = ' 2000-01-01 23:59:51' #### <<< this needs work!!!!! possible bad for hourly merging early in day
        if roundformat == 'noround':
            epochtimeofbar = convertTime(timeofbar,'dashspace','timetoepoch')#
######            print epochtimeofbar,'bla'
        else:
            roundTo=60
            timeb =  datetime.strptime(timeofbar, spaceYtime_format)
            dt = timeb
            seconds = (dt - dt.min).seconds
            # // is a floor division, not a comment on following line:
            rounding = (seconds+roundTo/2) // roundTo * roundTo
            roundtime = dt + timedelta(0,rounding-seconds,-dt.microsecond)
            epochtimeofbar = convertTime(str(roundtime),'dashnospace','timetoepoch')# int(time.mktime(time.strptime(timeofbar, formatstring)))
    except:
        timeofbar =' 2000-03-01 23:59:51'
        print 'bombed getting last bar epoch time in TicksUtile here'
        print 'probably missing a download file for one or all durations'
##        epochtimeofbar = convertTime(timeofbar,'dashspace','timetoepoch')
##    print timeofbar, filename
    return epochtimeofbar
#############################
def quarterround(num):
    return round(num*4)/4
#########
def create_bars_from_bars(bararrayin,today,sym,dur,durinseconds,hamode): #startmodes[initialize,bartobar,addonbartoboth]
##    print 'create bars from bars',dur,bararrayin[1]
    import time
    startmode = 'initialize'  ## no need for recent or rootfile as prev both dur bars have 5ticks in them
    rootname ='.ddload.csv'
    rootfile = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+rootname       
    startbartime = last_bar_epoch(rootfile,'rounded')####ddload_cutoff_epoch(rootfile,'normal')
    bar_percentage_required = 0.10   ###<<<<<<<<<<<<<    
########    print 'creating bars startmode,',startmode,startbartime
    barhi = float(0)
    barlo = float(99999999)
    tickcount = tottickcount = 0
    bararrayout =[]
    timearray =[]
    prevhi =  prevlo =   0
    totallength = len(bararrayin)
    prevbar_time = ' 2015-06-01 00:00:00'
##    if dur == '5secs':
##        prevbar_time = ' 2015-11-09 10:03:55'
    prevbar_time_epoch =   convertTime(prevbar_time,'dashspace','timetoepoch')  
##    print prevbar_time_epoch, prevbar_time
    prevdurbar_epoch = 0
    recentfile = DataDown +today+'.'+sym+ '.' +dur.replace(' ','')+  '.recent.csv'
##    flush the recentfile
    rpu_rp.WriteArrayToCsvfile(recentfile,[])
##    print recentfile
    ######################
    firsttripflag = 'notstarted'
    hardlimit = 4000
    if dur == '5secs':
        hardlimit = 99000000000
    barlimiter = min(4000,len(bararrayin))
    taillines = rpu_rp.tail_array_to_array(bararrayin,barlimiter) ##the one hour needs 720 rt msec ticks..so this might savesomething        
    totallength = len(taillines)
    lc =1
    barvolumetot = 0
    tickval = float(tickvaluedict[sym])
    prevhaopenpr = prevhaclosepr = openpr =1950.0

    for line in taillines:
##        print line
        if lc ==2:
            prevhaopenpr = float(line[2])
            prevhaclosepr = float(line[5])
        lc +=1
        tottickcount +=1 
        if len(line) > 3:
##            print line, 'this line'
            bar_time = line[1]
            if bar_time ==  '1':
                bar_time = ' 2015-06-01 00:00:00' 
            bar_time_epoch =   convertTime(bar_time,'dashspace','timetoepoch') 
            openpr = float(line[2])
            highpr = float(line[3])
            lowpr = float(line[4])
            closepr = float(line[5])
##            print line
                       
            barvolume =  int(line[6])
            barvolumetot  += barvolume
            ############
            barTobarElapsed = bar_time_epoch - prevbar_time_epoch
            barToprevdurbarElapsed = bar_time_epoch - prevdurbar_epoch
            prevbar_time_epoch = bar_time_epoch
            ##################
##            if int(durinseconds) > -1:
##                lessthanval = -1
##            else:
            lessthanval = 0
            testval = int(durinseconds) - barToprevdurbarElapsed - lessthanval
##            print testval
            tickcount +=1
            if highpr > barhi:
                barhi = highpr
            if lowpr < barlo:
                barlo = lowpr
            if tickcount == 1:
                habaropenpr = openpr
                newbartime = bar_time
                #############
            setflag= 'skip'
            
            haclosepr = quarterround(((habaropenpr + barhi + barlo +closepr )/4)) #
            habaropenpr = quarterround(((prevhaopenpr + prevhaclosepr)/2))
            habarhi = max(highpr,habaropenpr,haclosepr)
            habarlo = min(lowpr,habaropenpr,haclosepr)
            if int(durinseconds) == 60 and firsttripflag != 'started':    ######<<<<<<<<< this sets up the 5 second delay               
                resetamt = 5
            elif int(durinseconds) > 60 and firsttripflag != 'started':
                resetamt = 60
##                print resetamt
            else:
                resetamt = 0
            partflag ='full'
            if tottickcount == 1  :
                setflag = 'noreset'
            if bar_time_epoch >= (startbartime  - resetamt) and firsttripflag != 'started':
##                print 'tripped',dur,sym,bar_time_epoch,startbartime,bar_time
                setflag = 'reset'
                firsttripflag = 'started'              
            if testval <= 0   :
                setflag = 'reset'
            partbar = True
            barperc = float(float(barToprevdurbarElapsed) / float(durinseconds) )
            if  tottickcount == totallength and setflag != 'reset' and barperc > bar_percentage_required :
##                print round(barperc,3), barToprevdurbarElapsed, int(durinseconds)
                time = ' 2019-03-03 03:03:03' 
                partflag = 'partial'
                setflag = 'reset'
                partbar = True
       
            if setflag == 'reset' and len(line) > 3:
                tickcount =0          
                barline =[]
                bardir = 'grn'
                bartdesc = 'tail'
                bardesc = 'shortbar'
                barlen = haclosepr-habaropenpr
                if barlen < tickval:
                    bardir = 'red'
             
                barhead = habarhi-max(habaropenpr,haclosepr)
                bartail = habarlo-min(habaropenpr,haclosepr)
                barbigmult = 2
                if dur == '3mins':
                    barbigmult = 1

                barminbig = (tickval*barbigmult)-(tickval*0.10)    
                if abs(barlen) > barminbig :
                    bardesc = 'bigbar'
                if barhead == 0 and bardir == 'red':
                    bartdesc = 'notail'
                if bartail == 0  and bardir == 'grn':
                    bartdesc = 'notail'
                    
                bardesc = bardir +'N' + bartdesc + 'N'+ bardesc
                ilist = [sym, newbartime,openpr,barhi,barlo,closepr,barvolumetot,partflag,barToprevdurbarElapsed]
##                         habaropenpr,habarhi,habarlo,haclosepr,barlen,barhead,bartail,bardesc]
                if hamode == 'hamode':
                    ilist = [sym, newbartime,openpr,barhi,barlo,closepr,barvolumetot,partflag,barToprevdurbarElapsed,\
                         habaropenpr,habarhi,habarlo,haclosepr,barlen,barhead,bartail,bardesc]
                for item in ilist:
                    barline.append(item)
                prevdurbar_epoch = bar_time_epoch
                if partbar == True:
                    bararrayout.append(barline)
                barhi = 0
                barlo = 99999999
                habarhi = 0 #max(highpr,habaropenpr,haclosepr)
                habarlo = 9999999 #min(lowpr,habaropenpr,haclosepr)
                barvolumetot = 0
                partflag = 'full'
                
                prevhaopenpr = habaropenpr
                prevhaclosepr = haclosepr
##
##    rpu_rp.WriteArrayToCsvfileAppend(recentfile,bararrayout)
    return bararrayout
    #######################
def clean_RTTick5secBars(oneline,sym):
    onelinenew =[]
##    print oneline
    reqid = (oneline[0]).replace('<realtimeBar reqId=','')
    epochstring = (oneline[1]).replace(' time=','')
    timedate = convertTime(epochstring,'dashspace','epochtotime') #epoch_to_time(epochstring,'dashspace','epochtotime')
    openpr = float(oneline[2].replace(' open=',''))
    highpr =  float(oneline[3].replace(' high=',''))
    lowpr =  float(oneline[4].replace(' low=',''))
    closepr =  float(oneline[5].replace(' close=',''))
    vwappr =  float(oneline[7].replace(' wap=',''))
    volume =  int(oneline[6].replace(' volume=',''))
    ilist = [sym,timedate,openpr,highpr,lowpr,closepr,volume,vwappr,sym]
    for item in ilist:
        onelinenew.append(item)
##    print onelinenew
    return onelinenew
###########################
def clean_rtTICKbar(oneline,sym):
    onelinenew =[]
##    print oneline
##    reqid = (oneline[0]).replace('<realtimeBar reqId=','')
    fullstring = str(oneline)
##    epochstring = (oneline[1]).replace(' time=','')
##    timedate = convertTime(epochstring,'dashspace','epochtotime') #epoch_to_time(epochstring,'dashspace','epochtotime')
##    openpr = float(oneline[2].replace(' open=',''))
##    highpr =  float(oneline[3].replace(' high=',''))
##    lowpr =  float(oneline[4].replace(' low=',''))
##    closepr =  float(oneline[5].replace(' close=',''))
##    vwappr =  float(oneline[7].replace(' wap=',''))
##    volume =  int(oneline[6].replace(' volume=',''))
##    ilist = [sym,timedate,openpr,highpr,lowpr,closepr,volume,vwappr,sym]
    ilist = [sym,fullstring]
    for item in ilist:
        onelinenew.append(item)
    return onelinenew
###########################
def clean_rtDOMbar(oneline,sym):
    onelinenew =[]
##    print oneline
##    reqid = (oneline[0]).replace('<realtimeBar reqId=','')
    fullstring = str(oneline)
##    epochstring = (oneline[1]).replace(' time=','')
##    timedate = convertTime(epochstring,'dashspace','epochtotime') #epoch_to_time(epochstring,'dashspace','epochtotime')
##    openpr = float(oneline[2].replace(' open=',''))
##    highpr =  float(oneline[3].replace(' high=',''))
##    lowpr =  float(oneline[4].replace(' low=',''))
##    closepr =  float(oneline[5].replace(' close=',''))
##    vwappr =  float(oneline[7].replace(' wap=',''))
##    volume =  int(oneline[6].replace(' volume=',''))
##    ilist = [sym,timedate,openpr,highpr,lowpr,closepr,volume,vwappr,sym]
    ilist = [sym,fullstring]
    for item in ilist:
        onelinenew.append(item)
    return onelinenew
###########################
###########################
def prepare_rtDOMbars(date,sym,startmode):
##    print 'preparing 5secs in tickutiles...',startmode
    durinseconds= 1
    singleslist = glob.glob(DataDown+ date + '.' + sym  +'.rtDOMbar.*')
    newsingles =[]
    #. .. this creates the recent file 5secs used in merge_bar
    filesinglebars = DataDown +date+'.'+sym+'.'+'DOMS'+'.recent.csv'
    for f in singleslist:
        fline = rpu_rp.CsvToLines(f)
        newsingles.append(fline[0])
        os.remove(f)       
        rpu_rp.WriteArrayToCsvfileAppend(filesinglebars,newsingles)        
######    outputbothFile = DataDown +date+'.'+sym+'.'+'DOMS'+'.both.csv'
######    file1 = outputbothFile.replace('.both.','.ddload.')
######    file2 = outputbothFile.replace('.both.','.recent.')
######    cutoffmintime = int(2)
######    print 'merging recent file to dload in Ticksutile.prepare....mod'
######    merge_bar_files(file1,file2,outputbothFile,cutoffmintime) ## this creates both file
####################
###########################
def prepare_rtTICKbar(date,sym,startmode):
    durinseconds= 1
    singleslist = glob.glob(DataDown+ date + '.' + sym  +'.rtTICKbar.*')
    newsingles =[]
    #. .. this creates the recent file  used in merge_bar
    filesinglebars = DataDown +date+'.'+sym+'.'+'TICKrtbar'+'.recent.csv'
    for f in singleslist:
        fline = rpu_rp.CsvToLines(f)
        newsingles.append(fline[0])
        os.remove(f)       
        rpu_rp.WriteArrayToCsvfileAppend(filesinglebars,newsingles)        
######    outputbothFile = DataDown +date+'.'+sym+'.'+'TICKrtbar'+'.both.csv'
######    file1 = outputbothFile.replace('.both.','.ddload.')
######    file2 = outputbothFile.replace('.both.','.recent.')
######    cutoffmintime = int(2)
######    print 'merging recent file to dload in Ticksutile.prepare....mod'
######    merge_bar_files(file1,file2,outputbothFile,cutoffmintime) ## this creates both file
####################     
###########################
def prepare_tickfilesto5secBars(date,sym,startmode):
##    print 'preparing 5secs in tickutiles...',startmode
    durinseconds= 1
    singleslist = glob.glob(DataDown+ date + '.' + sym  +'.rtimebar.*')
    newsingles =[]
    #. .. this creates the recent file 5secs used in merge_bar
    filesinglebars = DataDown +date+'.'+sym+'.'+'5secs'+'.recent.csv'
    for f in singleslist:
        fline = rpu_rp.CsvToLines(f)
        newsingles.append(fline[0])
##        print fline[0]
##        movefile = f.replace(DataDown,DataDown+'tempsingles/') ##        movearea = DataDown+'tempsingles' ##        shutil.move(f,movearea)
        os.remove(f)       
        rpu_rp.WriteArrayToCsvfileAppend(filesinglebars,newsingles)        
    outputbothFile = DataDown +date+'.'+sym+'.'+'5secs'+'.both.csv'
    file1 = outputbothFile.replace('.both.','.ddload.')
    file2 = outputbothFile.replace('.both.','.recent.')
    cutoffmintime = int(2)
    print 'merging recent file to dload in Ticksutile.prepare....mod'
    merge_bar_files(file1,file2,outputbothFile,cutoffmintime) ## this creates both file
#################### 
def create_state_files(today,sym,dur,indicator):   
    outfile = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.' + indicator + 'state.csv'
    infile = DataDown +today+'.'+sym+'.'+dur.replace(' ','')+'.both.csv'
    arrayin = rpu_rp.CsvToLines(infile)
    arrayout = rpInd.GetStates(arrayin,sym,indicator)
    rpu_rp.WriteArrayToCsvfile(outfile,arrayout)
##############
def recenttick(sym,mode):
    if mode == 'recent':
        RTFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    elif mode == '1min':
        RTFile = DataDown + today + '.' + sym + '.1min.ddload.csv'        
    else:
        RTFile = DataDown + today + '.' + sym + '.1min.both.csv'
        
    tickvalue = float(tickvaluedict[sym])
    if os.path.isfile(RTFile) :
        arr = rpu_rp.CsvToLines(RTFile)
        tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RTFile),1)[0]
##        tickp = (tickline[2]).replace(' price=','')# price=8948.5', ## for using live ticker nto 5sec
        tickp = tickline[5] ## uses 5 sec tick bar style
        lasttick = rpu_rp.rounderrp(float(tickp),tickvalue)
    else:
        lasttick = 9999
    return lasttick
######################
def backupTickfiles(fname1):
    f2 =[]
    f1=[]
    fname2  = fname1.replace('.csv','bu.csv')
    if os.path.isfile(fname2): 
        f2 = rpu_rp.CsvToLines(fname2)
    if os.path.isfile(fname1):
        f1 = rpu_rp.CsvToLines(fname1)
        for line in f1:
            f2.append(line)
        rpu_rp.WriteArrayToCsvfile(fname2,f2)
    #############
def trimFile(fname1,linesleft):
    c=0
    f2 =[]
    f1=[]
    f3=[]
    fname2  = fname1.replace('.csv','bu.csv')
    print fname1
    if os.path.isfile(fname2): 
        f2 = rpu_rp.CsvToLines(fname2)
    if os.path.isfile(fname1):
        f1 = rpu_rp.CsvToLines(fname1)
        lengthf1 = len(f1)
        topfile = lengthf1 - linesleft
        print topfile,linesleft
        for line in f1:
            c+=1
            if c < topfile:
                f2.append(line)
            else:
                f3.append(line)
        rpu_rp.WriteArrayToCsvfile(fname2,f2)
        rpu_rp.WriteArrayToCsvfile(fname1,f3)
        #######################
def fibbo(fibR,anchor,peak,trend):
    trend = 'up'
    if trend == 'up':
        movehandles = (peak - anchor)
        fibspot = peak  - (movehandles * fibR)
        fibhandles = (movehandles * fibR)
        pass
    return fibspot,movehandles,fibhandles
