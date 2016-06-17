# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash + '/'
sys.path[0:0] = [EXEnoslash]
prevsigid = ''
########################
timeFormat = "%Y%m%d %H:%M:%S"
dateFormat = "%Y%m%d"
#################
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
import  rpu_rp, rpInd, ibutiles  #########remove after test
#############################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
global today
today =  rpu_rp.todaysdateunix()
from datetime import datetime
##############################
def reply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile('OrderIdsSaved.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile('pricenow',str(float(msg.price)) +',')
##    print "Server Response: %s, %s" % (msg.typeName, msg)
    rpu_rp.WriteStringsToFileAppend('replys',str(msg))
####################
global tws_conn
tws_conn = Connection.create(port=7496, clientId=66)
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(ibutiles.reply_handler)
##tws_conn.reqAccountUpdates(False,'U87392')
##connectallTWS()
################
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)
libsyms = EXE + 'library.syms.csv'
rpsymdict = rpu_rp.create_dict(libsyms,0,1)
exchdict = rpu_rp.create_dict(libsyms,0,2)
typedict = rpu_rp.create_dict(libsyms,0,5)
currdict = rpu_rp.create_dict(libsyms,0,3)
expiredict = rpu_rp.create_dict(libsyms,0,4)
dboostdict = rpu_rp.create_dict(libsyms,0,6)
tickdict = rpu_rp.create_dict(libsyms,0,8)
tsizedict = rpu_rp.create_dict(libsyms,0,7)
roundfactordict = rpu_rp.create_dict(libsyms,0,9)
entrywiderdict = rpu_rp.create_dict(libsyms,0,10)
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()
###################################
def check_for_entry_fills(profitorder,order_id):
    ordersfname = 'entryorderssent'
    lines = rpu_rp.CsvToLines(ordersfname)
    for l in lines:
        print l
###################
global nextorderID
def get_orderid():
    tws_conn.reqIds(100)
    for l in rpu_rp.CsvToLines('OrderIdsSaved.csv'):
        order_id = int(l[0])
    return order_id
#####################
profitticks = 4
#################        
loopamax = 2000
loopa = 0
global command
sigs = rpu_rp.CsvToLines(sigarea + today +'.sigs.csv')
while loopa < loopamax:
    loopa +=1
    ###########
    mode = (rpu_rp.CsvToLines(DataDown+'controller.txt')[0])[0]   
    tranflag = False
    if mode != 'NOTRANSMIT-setting':
        tranflag = True   
    if mode == 'STOP-RUN-setting':
        print 'got the order to exit program....!!! <<<'
        sys.exit()
        loopamax = 1
    sig = rpu_rp.tail_array_to_array(sigs,12)[0]
    sigid = sig[1]+sig[2]+sig[3]+sig[5]
    print sigid
    sigprice = sig[3]
    sym = sig[1]
    action = sig[5]
    dur = sig[2]   
    if dur == '30 secs':
        tfactor = float(0.5) 
    else:
        tfactor = float(1.0)     
    tsize = int(int(tsizedict[sym]) * tfactor)
    decimalboost = float(dboostdict[sym])
    onetick = float(tickdict[sym])
    roundfactor = int(roundfactordict[sym])
    addamt = onetick * int(entrywiderdict[sym])
    onetick = float(1/decimalboost)
    tickrounder = roundfactor
    if roundfactor == 0:
        tickrounder = 0.25     
    ## create contract here   
    symib = symdict[sym]            
    symcontract = ibutiles.create_ticksym(14,sym)
    ########  poll for a recent price
    tws_conn.reqMktData(14,symcontract,'BID',True) ## use this to get a valid price
    rpu_rp.WriteArrayToCsvfile('pricenow',[])
    for l in rpu_rp.CsvToLines('pricenow'):
        pricebid =  float(l[0])
    ##################
    if sigid == prevsigid:
        tranflag = False
        #########################
    order_id = get_orderid()
    prevsigid = sigid
    print sigprice, decimalboost, 'is sigprice'
    pricebid = float(sigprice)/float(decimalboost)
    if tickrounder == 0:
        pricenow = round(pricebid,roundfactor)
    else:
        pricenow =  round(pricebid / tickrounder) * tickrounder
    print pricenow
    ########################################################
    sigprice = round(float((sig[3]))/float(decimalboost),roundfactor)
    ########################
    ordermode = 'entry'
    if 'entry'  == 'entry': # always true remove after new version
        tside = 'BUY'
        flipsign = int(-1)
        flipside = 'SELL'
        if action == 'negcrossmcd':
            tside = 'SELL'
            flipsign = int(1)
            flipside = 'BUY'
        entryprice = pricenow + (flipsign * addamt) 
        profprice = orderprice - (profitticks * onetick *flipsign) - (flipsign *addamt)
        stopprice = orderprice + (profitticks * onetick *flipsign) + (flipsign *addamt)
        ###########
    orderstring = str(order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(orderprice)
    print orderstring

    entryorder = ibutiles.create_order('LMT', tsize, tside, orderprice,tranflag,orderprice,orderprice,'entry')       
    profitorder = ibutiles.create_order('LMT', tsize, flipside, profprice,tranflag,profprice,profprice,'profit')
    stoporder = ibutiles.create_order('STPLMT', tsize, flipside, stopprice,tranflag,stopprice,stopprice,'stop')
    
    if mode == 'NOTRADE-setting':
        print 'flag said do not place!!!!!'
    else:
        tws_conn.placeOrder(order_id, symcontract, entryorder)
        tws_conn.placeOrder(order_id+1, symcontract, profitorder)
        rpu_rp.WriteStringsToFileAppend('entryorderssent',orderstring)
        print 'placing order'
    sleep(5)
print 'disconnecting.. done..'
tws_conn.disconnect()
####reqGlobalCancel()
## enter a trailstop as profit order...
##        tws_conn.reqPositions(62,1)
    ##    tws_conn.reqExecutions(3,)
    ##    tws_conn.reqAllOpenOrders()
    ##    tws_conn.cancelOrder(order_id)
