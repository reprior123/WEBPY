import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
#########################################
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    print var
    locals()[var] = nd[var]
####################
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
import ctypes
###################################
##############################
symbol_list = symdict.keys()
##symbol_list =['ES','EUR.USD']
barlistall = bardict.keys()  ##
barlist =[]
barlist = ['1 Week']
##########################################
date =  rpu_rp.todaysdateunix()
date = '20150905'
datehyphen = rpu_rp.todaysdatehypens(date)
##########################
def create_weeklies():
    sym = 'SPX'
    ##RP_Snapshot.snapshot_sym(sym,date)
    basisdur = '1day'
    TicksUtile.assemble_dur_bars(date,sym,'1day','initialize','5secs')
    TicksUtile.assemble_bars_1min_basis(date,sym,'1Week','bartobar',basisdur)
    indlist = ['mcross','pivot','R','R2','S','S2']
    threshold = 0.0
    rpInd.create_states_files(sym,'1Week',date,threshold,indlist)
    rpInd.create_states_files(sym,'1day',date,threshold,indlist)
############################################
def get_dload_barsWbu(start_path,dur,barfileout,sym):
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
                print f
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                print  fp,'working'
                lines = rpu_rp.CsvToLines(fp)
                for l in lines:
##                    print l
                    newl =[]
                    if len(l) > 2:
                        timestring = l[1]
                        e = TicksUtile.time_to_epoch(timestring)
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
    rpu_rp.WriteArrayToCsvfile(fileoutname+'news', cleans)
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
    rpu_rp.WriteArrayToCsvfile(fileoutname, newalls)
##        newn.append(sym)
##########################################
indlist = ['RSI','ROC']
########durlist = ['1min', '5mins', '15mins', '3mins', '1hour', '1day']
########symlist = ['ES','CL','FDAX']
dur = '5mins'
sym ='ES'
##ind = 'mcross'
##newstatearea = statearea +'statedir' +month + '/'
def ensure_dir(d):
##    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
## need to create the states files in each dir        
mlist = glob.glob(DataDown +'dir*')
for ma in mlist:
    month =  ma[16:]
    newstatearea = statearea +'statedir' +month 
    newstateareaslash = newstatearea + '/'
    ensure_dir(newstatearea)
    
    f = newstateareaslash+'ES.'+dur+'.mcross.state.csv'
    fileoutname = newstateareaslash+ sym+'.'+dur+'.multiinds.state.csv'
    farray = rpu_rp.CsvToLines(f)
    line =[]
    fullarr =[]
    for l in farray:
        t = l[0]
        indlist = indlist_part #['RSI','ROC']
        for ind in indlist:
            l.append(ind)
            l.append(rpInd.ShowABarofIndByTime(sym,dur,ind,t,555555)[1])
            l.append(rpInd.ShowABarofIndByTime(sym,dur,ind,t,555555)[3])
        print t,dur
        fullarr.append(l)
    rpu_rp.WriteArrayToCsvfile(fileoutname+'news', fullarr)

########start_path = DataDown +'dir201601/'

########for sym in symlist:
########    for dur in durlist:
########        secs = secdict[dur]
########        barfileout = DataDown + '20161233.' + sym +'.' + dur+'.ddload.csv' #'blalines.csv'
########        get_dload_barsWbu(start_path,dur,barfileout,sym)
        
