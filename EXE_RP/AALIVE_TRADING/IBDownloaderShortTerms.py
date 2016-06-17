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
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
import Mod_TicksUtile, Mod_ibutiles
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   #
############################################
global  sym, fname, barlist, bar
####################################
fname = DataDown+ today + '.' + 'tempdlfile' +'.ddload.csv'
rpu_rp.WriteStringsToFile(fname,'') #flush the file
replyfname = TMP + 'replysdloader.csv'
def reply_handler(msg):
    replyfname = TMP + 'replysdloader.csv'
    if msg.typeName == 'historicalData':
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        rpu_rp.WriteStringsToFileAppend(replyfname,str(msg))
        #########
#####################
def historical_data_handler(msg):  
    global newDataList
    sym = 'tempdlfile'
    fname = DataDown+ today + '.' + sym +'.ddload.csv'
    if ('finished' in str(msg.date)) == False:  ### keep building the list
        fstring = "%Y-%m-%d %H:%M:%S"
        dateold = localtime(int(msg.date))
        tdate = strftime(fstring, dateold)
        if len(msg.date) == 8 :
            tdate = (str((int(msg.date))))[0:4] + '-' + str((int(msg.date)))[4:6]+ '-' + str((int(msg.date)))[6:8] + ' 23:59:58'
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
newDataList = []
print 'connecting hdownload flex'
tws_conn = Connection.create(port=7496, clientId=125)
tws_conn.connect()
tws_conn.register(Mod_ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.register(historical_data_handler, message.historicalData)
    #######################################
def dload(symlist,barlist,strikelist,expirylist):
    print symlist,barlist
    global bar, sym
    trans_id = 0
    strikelist = [1]
    expirylist  = [1]
    for sym in symlist:
        print sym
        for bar in barlist:
            for strike in strikelist:
                for expiry in expirylist:
                    fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
                    Mod_TicksUtile.backupTickfiles(fname)
                    ##########
                    duration = bardict[bar]
                    barspaced = bardictspaced[bar]
                    contract = Mod_ibutiles.create_contract(sym,strike,expiry)
                    ticktype = ticktypedict[sym]
                    print bar, sym, duration,ticktype, barspaced, strike, expiry
                    tws_conn.reqHistoricalData(trans_id, contract, '', duration, barspaced, ticktype, 0, 2)
                    trans_id = trans_id + 1  
                    sleep(20)
                    
                    tmp = DataDown+ today + '.' + 'tempdlfile' + '.ddload.csv'
                    fname = DataDown+ today + '.' + sym + '.'  + bar+'.ddload.csv'
                    shutil.copyfile(tmp,fname)
                    Mod_TicksUtile.throw_out_lastbar(fname)
    ###############
##blist = bardictweekly.keys()
##blist=['1daylong']
doall = 'n' # raw_input('do all syms? ')
if doall == 'y':
    slist = ['ES','FDAX'] #symlistAll
else:
    symtodo = 'ES' #raw_input('enter sym here ')
    slist = [symtodo]
############
doallbars = 'y' # raw_input('do all bars? ')
if doallbars == 'y':
    blist = ['5secs','1min','3mins','5mins','15mins','1hour','1day'] #barlist_Allw5sec
    blist = ['5secs','1min','3mins','5mins','15mins','1hour'] #barlist_Allw5sec
    blist = ['5secs','1min','3mins'] #barlist_Allw5sec
else:
    bartodo = raw_input('enter bar here ..eg. 1min ')
    blist = [bartodo]
##############
strikelist = ['1'] #rpu_rp.CsvToLines('strikelist.csv')[0]            
explist = ['1'] #rpu_rp.CsvToLines('expirylist.csv')[0]
############
dload(slist,blist,strikelist,explist)
print 'disconnecting hdownload flex'
tws_conn.disconnect()
