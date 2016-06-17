# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
from datetime import datetime
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]

localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
#######################################
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import  rpu_rp, rpInd, ibutiles
from datetime import datetime
import ctypes 
#######################
timedateFormat = "%Y%m%d %H:%M:%S"
time_format = "%H:%M:%S"
dateFormat = "%Y%m%d"
##############################
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)
libbars = EXE + 'library.bars.csv'
libsyms = EXE + 'library.syms.csv'
bardict = rpu_rp.create_dict(libbars,0,1)
secdict = rpu_rp.create_dict(libbars,0,4)
modedict = rpu_rp.create_dict(libbars,0,5)
symdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
tickdict = rpu_rp.create_dict(libsyms,0,8)
tsizedict = rpu_rp.create_dict(libsyms,0,7)
roundfactordict = rpu_rp.create_dict(libsyms,0,9)
entrywiderdict = rpu_rp.create_dict(libsyms,0,10)
profticksdict = rpu_rp.create_dict(libsyms,0,12)
symbol_list = symdict.keys()
##################
prevsigid = ''
mode = 'livescan'
print 'scanning for fills to send profit orders....mode is:'
print mode
today =  rpu_rp.todaysdateunix()
yesterday ='20150609'
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
def read_vars(): ##read variables from the control panel file
    cpfile = TMP + 'signalcontroller.txt'
    paramlines = rpu_rp.CsvToLines(cpfile)
    varstrings = ['TimeLimitRecentSigs','SignalsToShow','DurationToShow']
    var = {}
    for varstring in varstrings:
        for line in paramlines:
            if len(line) > 0:
                if line[0] == varstring:
                    var[varstring] = line[1]
    return int(var['TimeLimitRecentSigs'])
############################
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile(TMP +'pricenow',str(float(msg.price)) +',')
    rpu_rp.WriteStringsToFileAppend(TMP + 'FillScanner.replys',str(msg))
global tws_conn
tws_conn = Connection.create(port=7496, clientId=77)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(localreply_handler)
###################
def get_orderid():
    tws_conn.reqIds(100)
    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
    return order_id
#####################
def scan_for_fills():
    entrysSentFile = TMP +  'Entry.orders.Sent.csv'
    filledNoProfFile =  TMP + 'Entry.orders.FilledNoProf.csv'
    filledNProfSentFile = TMP +  'Entry.orders.FilledNProfSent.csv'
    ProfSentFile = TMP + 'Profit.orders.Sent.csv'
    openarray = []
    fillNoProf = []
    filledNProfSent = []
    replys = rpu_rp.CsvToLines( TMP + 'entryreplys') ## this reads the replies from the sigcreate login
    for l in  rpu_rp.CsvToLines(entrysSentFile):
        if len(l) > 0:
            print l
            status ='open'
            listordid = l[0]
            #poll for status
            tws_conn.orderStatus(listordid)
            sleep(3) ### give it time to read list
    ##        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
            for rep in replys:
                ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
                if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
                    print 'found a fill in entry orders', listordid
##                    status='filled'
                if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##                    print 'found a fill in entry orders', listordid
                    status='cxld'
            if status  == 'filled':
                fillNoProf.append(l)
                pass
            elif status == 'cxld':
##                print 'was cxld, deleting from list',l
                pass
            else:
                openarray.append(l)
##                print 'is open still',l
    rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
    ## enter proforders if any
    profsneeded = rpu_rp.CsvToLines(filledNoProfFile)
    profsplaced = []
    profitticks = 3
    stopticks = 14
    profmult = 1
    for entryorder in profsneeded:
        print profsneeded
        print 'those were all the profs needed'
        flipsign = int(1)
        tside = 'BUY'
        if entryorder[1] == 'BUY':
            tside  = 'SELL'
            flipsign = int(-1)
        tsize = int(entryorder[2])
        sym = entryorder[3]
        profitticks = int(profticksdict[sym])
        print 'original signal order = ', entryorder
        orderprice = float(entryorder[4])        
        decimalboost = float(dboostdict[sym])
        onetick = float(tickdict[sym])
        addamt = onetick * int(entrywiderdict[sym])
        
        tranflag = False
        profprice = orderprice - (profmult * profitticks * onetick *flipsign) - (flipsign *addamt)
        stopprice = orderprice + (stopticks * onetick *flipsign) + (flipsign *addamt)
##        print profprice,stopprice
        profitorder = ibutiles.create_order('LMT', tsize, tside, profprice,tranflag,profprice,profprice,'profit')
        stoporder = ibutiles.create_order('STP', tsize, tside, stopprice,tranflag,stopprice,stopprice,'stop')
        order_id = get_orderid()
        symcontract = ibutiles.create_ticksym(23,sym)  ## might need to vary this number at some point
        tws_conn.placeOrder(order_id, symcontract, profitorder)
        tws_conn.placeOrder(order_id+1, symcontract, stoporder)
        print 'placed a profit and stop order here '
        print sym, tside, str(tsize), str(profprice),'PROFITORDER'
        profsplaced.append(entryorder)
        sleep(4)
    rpu_rp.WriteArrayToCsvfileAppend(filledNProfSentFile,profsplaced)
    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,[])
#################        
loopmax = 2000
loop = 0
########################

cycledelay = 10
while loop < loopmax:
    print 'profit scanner...'
    loop +=1
    scan_for_fills()
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by fill scanner...dead since..'
print 'disconnecting.. done..'
tws_conn.disconnect()
