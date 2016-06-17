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
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
################
##symbol_list = symdict.keys()
##symbol_list =['ES','EUR.USD']
##barlistall = bardict.keys()  ##
##barlist =[]
barlist = ['1 Week']
########################################## 
def create_weeklies():
    sym = 'SPX'
    basisdur = '1day'
    TicksUtile.assemble_dur_bars(date,sym,'1day','initialize','5secs')
    TicksUtile.assemble_bars_1min_basis(date,sym,'1Week','bartobar',basisdur)
    indlist = ['mcross','pivot','R','R2','S','S2']
    threshold = 0.0
    rpInd.create_states_files(sym,'1Week',date,threshold,indlist)
    rpInd.create_states_files(sym,'1day',date,threshold,indlist)
############################################
def get_dload_barsWbu(start_path,dur,barfileout,sym):
    import TicksUtile   
    total_size = 0
    alllines =[]
    alltimes =[]
    fileoutname = barfileout
    for dirpath, dirnames, filenames in os.walk(start_path):
##        print dirpath
        subdirsize = 0
        for f in filenames:
##            if 'ES.'+dur+'.ddload' in f :
            if '.'+sym+'.'+dur+'.ddload' in f  :
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
##############                print  fp,'working'
                lines = rpu_rp.CsvToLines(fp)
                for l in lines:
                    newl =[]
                    if len(l) > 2:
                        timestring = l[1]
                        e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
##                        fsourcedate = f.replace('.ES.'+dur+'.ddload.csv','')
                        fsourcedate = f.split('.')[0]
                        fsourcesym = f.split('.')[1]
                        fsourcedur = f.split('.')[2]
                        l.append(fsourcedate)
                        l.append(fsourcesym)
                        l.append(fsourcedur)
                        newl.append(l[8])
                        newl.append(l[9])

                        newl.append(l[1])
                        newl.append(l[7])

                        newl.append(l[2])
                        newl.append(l[3])
                        newl.append(l[4])
                        newl.append(l[5])
                        newl.append(l[6])
                        alllines.append(newl)
    from operator import itemgetter, attrgetter, methodcaller
    sortedall = sorted(alllines,key=itemgetter(0,1,2,3),reverse=True)
    usort = rpu_rp.uniqnosort(sortedall)
    prevdur = time = ''
    cleans =[]
    for y in usort:
##        print y
        dur = y[2]
        time = y[3]
        if dur == prevdur and time == prevtime:
##            print y
##            print prevy,'prev'
            pass
        else:
            cleans.append(y)
        prevdur = dur
        prevtime = time
        prevy = y
##    rpu_rp.WriteArrayToCsvfile(fileoutname+'news', cleans)
    newalls=[]
    for n in cleans:
##        print n
        newn =[]
        sym = n[0]
        dur = n[1]
        time = n[2]
        openp = n[4]
        hip = n[5]
        lowp = n[6]
        closep = n[7]
        volu = n[8]
        newn.append(sym)
        newn.append(time)
        newn.append(openp)
        newn.append(hip)
        newn.append(lowp)
        newn.append(closep)
        newn.append(volu)
        newalls.append(newn)
    sortednewalls = sorted(newalls,key=itemgetter(0),reverse=False)
    sortednewallsu = rpu_rp.uniq(sortednewalls)

    sortednewallsuClean = []
    preve = 0
    for l in sortednewallsu:
        timestring = l[1]
        try:
            e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
        except:
            print timestring,' did not work, needs old format'
            e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
        diffcur = e - preve
        preve = e
        if diffcur >= int(secs) or '22:30:00'  in timestring:
            sortednewallsuClean.append(l)
        else:
##            print diffcur,timestring,dur,'did not pass test'
            pass
    lenfull = len(sortednewallsuClean)
    third1 = int(round(lenfull/3))
    third2 = 2*third1
    third3 = lenfull - third2 + 1
    print lenfull,third1,third2,third3,dur,sym
    part33 =  rpu_rp.head_array_to_array(sortednewallsuClean,third1)
    third2array = rpu_rp.head_array_to_array(sortednewallsuClean,third2)
    part34 =  rpu_rp.tail_array_to_array(third2array,third1)
    part35 =  rpu_rp.tail_array_to_array(sortednewallsuClean,third3)
                     
    rpu_rp.WriteArrayToCsvfile(fileoutname, part33)
    third2name = fileoutname.replace('33','34')
    rpu_rp.WriteArrayToCsvfile(third2name, part34)
    third3name = fileoutname.replace('33','35')
    rpu_rp.WriteArrayToCsvfile(third3name, part35)
##########################################
##########################################
def create_timelist(barfile):
    fileoutname = 'barsout.csv'
    lines = rpu_rp.CsvToLines(barfile)
    preve = 0
    prevfname = 0
    ubars =[]
    uubars =[]
    diffprev = 1
    timelist = []
    for l in lines:
        if len(l) > 2:
##            print l
            timestring = l[2]
##            e = TicksUtile.time_to_epoch(timestring)
            timelist.append(timestring)
    timelistu = rpu_rp.uniq(timelist)
    return timelistu
##    rpu_rp.WriteArrayToCsvfile(fileoutname, ubars)
##########################################
def verify_bars(barfile):
    fileoutname = 'barsout.csv'
    lines = rpu_rp.CsvToLines(barfile)
    print barfile, 'needs verify'
    dur = barfile.split('.')[2]
    sym = barfile.split('.')[1]
    print dur
    durinseconds = int(secdict[dur])
    print dur, durinseconds
    preve = 0
    prevfname = 0
    ubars =[]
    uubars =[]
    diffprev = 1
    for l in lines:
        if len(l) > 2:
            timestring = l[1]
            e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
            diffcur = e - preve
##            print diffcur
            if diffcur != durinseconds:
                print sym,dur,diffcur, durinseconds,l
                ubars.append(l)
            else:
                pass
            preve = e
            prevline = l
            diffprev = diffcur
    rpu_rp.WriteArrayToCsvfile(fileoutname, ubars)
##    for b in ubars:
##        print b
    return ubars

##########################################
def check_bars(bararray):  ### what does this do?
    lines = bararray
    preve = 0
    prevfname = 0
    ubars =[]
    uubars =[]
    diffprev = 1
    for l in lines:
        if len(l) > 2:
            timestring = l[1]
            e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
            diffcur = e - preve
##            fname = int(l[7])
            fname = str(l[7])
##            fnamediff = fname - prevfname
            # analyze this bars diff and the previous...
            if diffcur == 0 :
                print l
                '''and diffprev == 0:
                pass
            elif diffcur != 0 and diffprev == 0 :
##                ubars.append(prevline)
                ubars.append(l)
            elif diffcur != 0 and diffprev !=0:
                ubars.append(l)
            else:
                pass
            preve = e
            prevfname = fname
            prevline = l
            diffprev = diffcur
###########
filelist = glob.glob(DataDown + '*both*')
##for f in filelist:
##    print f
##    verify_bars(f)
'''
######################
def chopMonthToDays(bararray,sym,dur,secs):  ### what does this do?
    lines = bararray
    print secs
    preve = 0
    prevfname = 0
    ubars =[]
    uubars =[]
    diffprev = 1
    daylist =[]
    for l in lines:
        if len(l) > 2:
            timestring = l[1]
            date = timestring[0:11]
            daylist.append(date)
    daylistu = rpu_rp.uniq(daylist)
    for day in daylistu:
        daysarray=[]
        for l in bararray:
            if day in l[1] :
                timestring = l[1]
                try:
                    e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
                except:
                    e = TicksUtile.convertTime(timestring,'dashspace','timetoepoch')
                diffcur = e - preve
                preve = e
##                print diffcur,timestring
                if diffcur == int(secs):
                    daysarray.append(l)
##                    print l
        print day, sym,dur, len(daysarray)
        fileoutname = DataDown + day +'.' + sym +'.' + dur+'.cleaned.csv' 
        rpu_rp.WriteArrayToCsvfile(fileoutname, daysarray)
##                save daysarray to file
######################################
#### need to create hourly and others from 1 or 5min for missing gaps....
##  grab all 1 minute and look for gaps and 5 mins      
monthlist = glob.glob(DataDown +'dir201603*')
for m in monthlist:
    month =  m[16:]
    print month, m         
    start_path = DataDown +'dir'+month+'/'  
    durlist = ['1min', '5mins', '15mins', '3mins', '1hour', '1day']
    symlist = symlistTicker
    for sym in symlist:
        for dur in durlist:
            secs = secdict[dur]
            barfileout = DataDown + month +'33.' + sym +'.' + dur+'.ddload.csv' #'blalines.csv'
            get_dload_barsWbu(start_path,dur,barfileout,sym)            
            barfilein = DataDown + month +'33.' + sym +'.' + dur+'.ddload.csv' #'blalines.csv'
##            bararray = rpu_rp.CsvToLines(barfilein)
##            chopMonthToDays(bararray,sym,dur,secs)
            ##############
    ##########        bla =  create_timelist(barfileout)
    ##########        preve = 0
    ##########        for u in bla:
    ##########            e = TicksUtile.time_to_epoch(u)
    ##########            if (e-preve) != int(secs):
    ##########                print e,preve,u,e-preve
    ##########            preve = e    
            ##    print u
            ##print bla
            
            print 'done'
            newbars = verify_bars(barfileout)
            newbars = verify_bars(barfileout.replace('33','34'))
            newbars = verify_bars(barfileout.replace('33','35'))
##            check_bars(newbars)
            ########################

