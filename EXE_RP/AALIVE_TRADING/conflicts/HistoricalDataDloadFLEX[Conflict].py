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
##    print var
    locals()[var] = nd[var]
####################
    
import  glob, csv, subprocess, datetime, shutil, subprocess, time
import rpu_rp, rpInd, ibutiles, TicksUtile
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   #
############################################
global today, sym, fname, barlist, bar
####################################
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
##    print msg
    global newDataList
    sym = 'blaf'
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
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.register(historical_data_handler, message.historicalData)
    #######################################
def dload(symlist,barlist,strikelist,expirylist):
    print symlist
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
                    TicksUtile.backupTickfiles(fname)
                    ##########
                    duration = bardict[bar]
                    barspaced = bardictspaced[bar]
                    contract = ibutiles.create_contract(sym,strike,expiry)
                    ticktype = ticktypedict[sym]
                    print bar, sym, duration,ticktype, barspaced, strike, expiry
                    tws_conn.reqHistoricalData(trans_id, contract, '', duration, barspaced, ticktype, 0, 2)
                    trans_id = trans_id + 1  
                    sleep(6)
                    tmpf = DataDown + today + '.' + 'blaf' + '.ddload.csv'
##                    fname = DataDown+ today + '.' + sym + '.'  + bar.replace(' ','')+'.ddload.csv'
                    shutil.copyfile(tmpf,fname)
                    TicksUtile.throw_out_lastbar(fname)
    ###############
##blist = bardictweekly.keys()
##blist=['1daylong']
slist = rpu_rp.CsvToLines(TMP+'symlist.csv')[0]
##slist = ['ES']       

blist = rpu_rp.CsvToLines(TMP+'barlist.csv')[0]
blist= barlist_Allw5sec
##blist = ['1min']       

strikelist = rpu_rp.CsvToLines('strikelist.csv')[0]            
explist = rpu_rp.CsvToLines('expirylist.csv')[0]            
dload(slist,blist,strikelist,explist)
######            HistoricalDataDloadFLEXa.dload(symlist,barlist,contractsdict)            

print 'disconnecting hdownload flex'
tws_conn.disconnect()


