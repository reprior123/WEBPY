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
sigarea = EXE + 'IbPy-master/Signals/'
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
#################  control area   ###########
ca = rpu_rp.CsvToLines('controller.txt')[0]
print ca
command = ca[0]
if command == 'autotrade':
    mode = 'trade' # 'notrade'
else:
    mode = 'notrade'
#############################
def error_handler(msg):
    print "Server Error: %s" % msg
##############################
global today
today =  rpu_rp.todaysdateunix()
from datetime import datetime
###########################
libticks = EXE + 'library.snapshotfields.csv'
fielddict = rpu_rp.create_dict(libticks,0,2)
##############################
global nextorderID
rpu_rp.WriteArrayToCsvfile('pricenow',[])
def reply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile('OrderIdsSaved.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile('pricenow',str(float(msg.price)) +',')
##    print "Server Response: %s, %s" % (msg.typeName, msg)
    rpu_rp.WriteStringsToFileAppend('replys',str(msg))
####################
##     Server Response: orderStatus, <orderStatus orderId=33, status=Submitted,
##     filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027016, parentId=0,
##     lastFillPrice=0.0, clientId=100, whyHeld=None 
##    Server Response: openOrder, <openOrder orderId=25, contract=<ib.ext.Contract.Contract object at 0x032F6F70>, order=<ib.ext.Order.Order
##    object at 0x032F6ED0>, orderState=<ib.ext.OrderState.OrderState object at 0x032F6FD0>>
##Server Response: orderStatus, <orderStatus orderId=25, status=Submitted,
##    filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027008, parentId=0, lastFillPrice=0.0, clientId=100, whyHeld=None>
###########################

'''need separate IDs for  execution connection andmarket data connection)
 '''
global tws_conn
tws_conn = Connection.create(port=7496, clientId=66)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.reqAccountUpdates(False,'U87392')
##connectallTWS()
################
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
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = rpsymdict.keys()
###################################
def check_for_entry_fills(profitorder,order_id):
    ordersfname = 'entryorderssent'
    lines = rpu_rp.CsvToLines(ordersfname)
    for l in lines:
        executedf = 'open'
        print l
##        order_id = 22
        filltag = 'orderId=' + str(order_id) + ', status=Filled'
        ## for order id, look fora fill
        for b in rpu_rp.TxtToLines('replys'):
            if 'orderStatus' in str(b) and filltag in str(b):
                print b
                executedf = 'filled'
        print executedf, 'placing prof ord if filled'
        executedf = 'filled'  ##### hack for testing to force the proforder
        if executedf == 'filled':
            print 'sending prof'
            ## cannot use this order, it is stale, need to rebuild order based on the dictionary
            ##created in order creation, tag the orders in the dictionary as entry,profit,filled,open and use this
##            newpoorder = ibutiles.create_order('LMT', tsize, flipside, profprice,True,profprice,profprice,'profit') ## need to add profit amount based ona dictionary created before
            
            tws_conn.placeOrder(order_id + 1, symcontract, profitorder)
###################   
loopamax = 20
loopa = 0
while loopa < loopamax:
    ca = rpu_rp.CsvToLines('controller.txt')[0]
    print ca
    command = ca[0]
    print 'running one loop and sleeping'
    loopa +=1    
    if command == 'stoprunning':
        loopamax = 1
    else:
        if command == 'notrade':
            mode = 'notrade'
        profitticks = 5
##        check_for_entry_fills()
        sigs = rpu_rp.CsvToLines(sigarea + 'sigs.csv')
        sig = rpu_rp.tail_array_to_array(sigs,2)[0]
        sigid = sig[1]+sig[2]+sig[3]+sig[5]
        print sigid
        tws_conn.reqIds(100)
        sleep(2)
        for l in rpu_rp.CsvToLines('OrderIdsSaved.csv'):
            order_id = int(l[0])
            ##################
        print sig # ['13:51:58', 'USD.CAD', '30 secs', '12436.5002', '-0.007', 'negcrossmcd', 'necd']]   
        sym = 'USD.JPY'
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
        ## create contract here   
        symib = symdict[sym] 
        ibsecType = typedict[sym] #'CASH'
        ibexchange = exchdict[sym] #'IDEALPRO'
        cashcurr = currdict[sym] #'USD'
        expiry = expiredict[sym] #'ignore'              
        symcontract = ibutiles.create_ticksym(14,symib, ibsecType, ibexchange, cashcurr,expiry)
        ########  poll for a recent price
        tws_conn.reqMktData(14,symcontract,'BID',True) ## use this to get a valid price
        sleep(1)
        for l in rpu_rp.CsvToLines('pricenow'):
            pricenow = float(l[0])         
        price = round(float((sig[3]))/float(decimalboost),roundfactor)
        sigprice = price
        onetick = float(1/decimalboost)
        tside = 'BUY'
        flipside = 'SELL'
        profprice = round(pricenow + (profitticks * onetick),roundfactor)
        stoptrailprice = round(pricenow - (profitticks * onetick * 3),roundfactor)
        if action == 'negcrossmcd':
            tside = 'SELL'
            flipside = 'BUY'
            profprice = round(pricenow - (profitticks * onetick),roundfactor)
            stoptrailprice = round(pricenow + (profitticks * onetick * 3),roundfactor)
            ###########
        orderstring = str(order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(pricenow)
        print orderstring
        
        entryorder = ibutiles.create_order('LMT', tsize, tside, pricenow,True,pricenow,pricenow,'entry')
        
        profitorder = ibutiles.create_order('LMT', tsize, flipside, profprice,True,profprice,profprice,'profit')
        trailamount = onetick * 8.0
        profitTrailSTP = ibutiles.create_order('TRAIL', tsize, flipside, profprice,True,trailamount,profprice,'trailrp')
        
        if mode == 'notrade':
            print 'flag said do not place!!!!!'
        else:
            if sigid != prevsigid:
                tws_conn.placeOrder(order_id, symcontract, entryorder)
                tws_conn.placeOrder(order_id+1, symcontract, profitTrailSTP)
                prevsigid = sigid
                rpu_rp.WriteStringsToFileAppend('entryorderssent',orderstring)
##                check_for_entry_fills(profitorder,order_id)
                print 'placing order'
            else:
                print 'dupe order, nothing done..'
    sleep(5)
print 'disconnecting.. done..'
tws_conn.disconnect()
####reqGlobalCancel()
## enter a trailstop as profit order...
##        tws_conn.reqPositions(62,1)
    ##    tws_conn.reqExecutions(3,)
    ##    tws_conn.reqAllOpenOrders()
    ##    tws_conn.cancelOrder(order_id)
