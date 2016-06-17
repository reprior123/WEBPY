import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import  glob, csv, subprocess, datetime, shutil, subprocess, time
import rpu_rp, rpInd, ibutiles
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   #
############################################
global today
global sym
newDataList = []
mode = 'intraday'#'intraday' #'hourly' ## 'daily'  'intraday'
#################################
global barlist, bar
def throw_out_lastbar(sym,dura,date):
    f = DataDown+ today + '.' + sym + '.'  + dura.replace(' ','') +'.ddload.csv'
    fnew = DataDown+ today + '.' + sym + '.'  + dura.replace(' ','') +'.ddloadnew.csv'
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
def dload_list(symbol_list,durmode):
    barlistall = bardict.keys()
    barlist =[]
    for b in barlistall:
        if modedict[b] != 'special' : 
            barlist.append(b)
    ##########################
    def backupTickfiles(fname1):
        fname2  = fname1.replace('.csv','bu.csv')
        f1 = rpu_rp.CsvToLines(fname1)
        f2 = rpu_rp.CsvToLines(fname2)
        for line in f1:
            f2.append(line)
        rpu_rp.WriteArrayToCsvfile(fname2,f2)
        rpu_rp.WriteArrayToCsvfile(fname1,[])
        #############
    def error_handler(msg):
        if  'historicalData' in str(msg):
            print 'error probably pacing hist data'
            pass
        elif 'connection is OK' in str(msg):
            pass
        else:
            print "Server Error: %s" % msg
#############
    def historical_data_handler(msg):  
        global newDataList
        fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
        if ('finished' in str(msg.date)) == False:  ### keep building the list
    ##        print (int(msg.date))
            fstring = "%Y-%m-%d %H:%M:%S"
            dateold = localtime(int(msg.date))
            tdate = strftime(fstring, dateold)       
            if bar == '1 day':
                tdate = (str((int(msg.date))))[0:4] + '-' + str((int(msg.date)))[4:6]+ '-' + str((int(msg.date)))[6:8] + ' 23:59:58'
    ##            print tdate
    ##            print msg.date
            dataStr = '%s, %s, %s, %s, %s, %s, %s' % (sym, tdate, msg.open, msg.high, msg.low, msg.close, msg.volume)  
            newDataList = newDataList + [dataStr]  
        else:
            print 'next list'
            rpu_rp.WriteStringsToFile(fname,'') #flush the file
            for a in newDataList:
                if len(a) > 2:
                    rpu_rp.WriteStringsToFileAppend(fname,a)
            newDataList = []
            ##########
    def reply_handler(msg):
        if msg.typeName == 'historicalData':
            pass
        else:
            print "Server Response: %s, %s" % (msg.typeName, msg)
####################
    tws_conn = Connection.create(port=7496, clientId=109)
    tws_conn.connect()
    tws_conn.register(error_handler, 'Error')
    tws_conn.registerAll(reply_handler)
    tws_conn.register(historical_data_handler, message.historicalData)
    #######################################
    trans_id = 0
    if durmode == 'd':
        barlist = ['1day']
    if durmode == '5secs':
        barlist =['5secs']
    for sym in symbol_list:
        for bar in barlist:
            fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
            backupTickfiles(fname)
            ##########
            duration = bardict[bar]
            barspaced = bardictspaced[bar]
            contract = ibutiles.create_ticksym(trans_id,sym)
            ticktype = ticktypedict[sym]
            
            print bar, sym, duration,ticktype, barspaced
            tws_conn.reqHistoricalData(trans_id, contract, '', duration, barspaced, ticktype, 0, 2)
            trans_id = trans_id + 1  
            sleep(3)
    ###############
    print 'disconnecting from ib..'
    tws_conn.disconnect()
    for sym in symbol_list:
        for dura in barlist: 
            throw_out_lastbar(sym,dura,today)
            ###########################
            #########################
def dload_listNEW(symbol_list,durmode,strike):
    barlistall = bardict.keys()
    barlist =[]
    for b in barlistall:
        if modedict[b] != 'special' : 
            barlist.append(b)
    ##########################
    def backupTickfiles(fname1):
        fname2  = fname1.replace('.csv','bu.csv')
        f1 = rpu_rp.CsvToLines(fname1)
        f2 = rpu_rp.CsvToLines(fname2)
        for line in f1:
            f2.append(line)
        rpu_rp.WriteArrayToCsvfile(fname2,f2)
        rpu_rp.WriteArrayToCsvfile(fname1,[])
        #############
    def error_handler(msg):
        if  'historicalData' in str(msg):
            print 'error probably pacing hist data'
            pass
        elif 'connection is OK' in str(msg):
            pass
        else:
            print "Server Error: %s" % msg
#############
    def reply_handler(msg):
        if msg.typeName == 'historicalData':
            pass
        else:
            print "Server Response: %s, %s" % (msg.typeName, msg)
####################
    def historical_data_handler(msg):  
        global newDataList
        fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
        if ('finished' in str(msg.date)) == False:  ### keep building the list
    ##        print (int(msg.date))
            fstring = "%Y-%m-%d %H:%M:%S"
            dateold = localtime(int(msg.date))
            tdate = strftime(fstring, dateold)       
            if bar == '1 day':
                tdate = (str((int(msg.date))))[0:4] + '-' + str((int(msg.date)))[4:6]+ '-' + str((int(msg.date)))[6:8] + ' 23:59:58'
    ##            print tdate
    ##            print msg.date
            dataStr = '%s, %s, %s, %s, %s, %s, %s' % (sym, tdate, msg.open, msg.high, msg.low, msg.close, msg.volume)  
            newDataList = newDataList + [dataStr]  
        else:
            print 'next list'
            rpu_rp.WriteStringsToFile(fname,'') #flush the file
            for a in newDataList:
                if len(a) > 2:
                    rpu_rp.WriteStringsToFileAppend(fname,a)
            newDataList = []
            ##########
    tws_conn = Connection.create(port=7496, clientId=109)
    tws_conn.connect()
    tws_conn.register(error_handler, 'Error')
    tws_conn.registerAll(reply_handler)
    tws_conn.register(historical_data_handler, message.historicalData)
    #######################################
    trans_id = 0
    if durmode == 'd':
        barlist = ['1day']
    if durmode == '5secs':
        barlist =['5secs']
    for sym in symbol_list:
        for bar in barlist:
            fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
            backupTickfiles(fname)
            ##########
            duration = bardict[bar]
            barspaced = bardictspaced[bar]
            contract = ibutiles.create_option_contract(sym,strike)
            ticktype = ticktypedict[sym]
            
            print bar, sym, duration,ticktype, barspaced
            tws_conn.reqHistoricalData(trans_id, contract, '', duration, barspaced, ticktype, 0, 2)
            trans_id = trans_id + 1  
            sleep(3)
    ###############
    print 'disconnecting from ib..'
    tws_conn.disconnect()
    for sym in symbol_list:
        for dura in barlist: 
            throw_out_lastbar(sym,dura,today)
            
