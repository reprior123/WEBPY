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
##    print var
    locals()[var] = nd[var]
####################
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
from datetime import datetime
import ctypes 
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import ibutiles
#######################
######timedateFormat = "%Y%m%d %H:%M:%S"
######time_format = "%H:%M:%S"
######dateFormat = "%Y%m%d"
#########
##################
prevsigid = ''
mode = 'livescan'
print 'scanning for fills to send profit orders....mode is:'
print mode
today =  rpu_rp.todaysdateunix()
current_time = datetime.now().time()
print current_time.isoformat()
##########################################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
############################
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'ProfOrderIds.csv',str(nextorderID)+ ',')   
##    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
##        rpu_rp.WriteStringsToFile(TMP +'profpricenow',str(float(msg.price)) +',')
    rpu_rp.WriteStringsToFileAppend(TMP + 'FillScanner.replys',str(msg))
############
global tws_conn
tws_conn = Connection.create(port=7496, clientId=77)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(localreply_handler)
###################
def get_orderid():
    tws_conn.reqIds(900)
    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'ProfOrderIds.csv'):
        order_id = int(l[0])
    return order_id
#####################
entrysSentFile = TMP +  'Entry.orders.Sent.csv'
filledNoProfFile =  TMP + 'Entry.orders.FilledNoProf.csv'
filledNProfSentFile = TMP +  'Entry.orders.FilledNProfSent.csv'
ProfSentFile = TMP + 'Profit.orders.Sent.csv'
#########
def scan_for_fills():
    openarray = []
    fillNoProf = []
    filledNProfSent = []
    replys = rpu_rp.CsvToLines( TMP + 'entryreplys') ## this reads the replies from the sigcreate login
    for l in  rpu_rp.CsvToLines(entrysSentFile):
        if len(l) > 0:
            print l, 'checking for this in entries with a status poll'
            status ='open'
            listordid = l[0]
            #poll for status
            tws_conn.orderStatus(listordid)
            sleep(1) ### give it time to read list
    ##        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
            for rep in replys:
                ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
                if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
                    print 'found a fill in entry orders', listordid
                    status='filled'
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
def send_prof_orders():    
    ## enter proforders if any
    profsneeded = rpu_rp.CsvToLines(filledNoProfFile)
    profsplaced = []
    profitticks = 3
    stopticks = 14
    profmult = 1
##    print profsneeded
##    print 'those were all the profs needed'
    for entryorder in profsneeded:
##        print entryorder, 'entryorder'
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
        print sym, tside, str(tsize), str(profprice),'PROFITORDER',order_id
        profsplaced.append(entryorder)
        sleep(2)
        rpu_rp.WriteArrayToCsvfileAppend(filledNProfSentFile,profsplaced)
    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,[])
#################        
loopmax = 2000000
loop = 0
########################
cycledelay = 10
while loop < loopmax:
    print 'profit scanner...'
    loop +=1
    scan_for_fills()
    send_prof_orders()
    sleep(cycledelay)
print 'finished ',loopmax,' loops  by fill scanner...dead since..'
print 'disconnecting.. done..'
tws_conn.disconnect()
