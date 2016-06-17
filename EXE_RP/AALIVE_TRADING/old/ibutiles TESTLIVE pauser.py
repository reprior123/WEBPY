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
########################
timeFormat = "%Y%m%d %H:%M:%S"
dateFormat = "%Y%m%d"
#################
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
import  rpu_rp, rpInd#, ibutiles  #########remove after test
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
        print 'the next #############is  ', nextorderID, '   #######'      
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        pricenow = float(msg.price)
        bla = str(pricenow) +','
        rpu_rp.WriteStringsToFile('pricenow',bla)
        sleep(1)
    print "Server Response: %s, %s" % (msg.typeName, msg)           
####################
##     Server Response: orderStatus, <orderStatus orderId=33, status=Submitted,
##     filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027016, parentId=0,
##     lastFillPrice=0.0, clientId=100, whyHeld=None 
##    Server Response: openOrder, <openOrder orderId=25, contract=<ib.ext.Contract.Contract object at 0x032F6F70>, order=<ib.ext.Order.Order
##    object at 0x032F6ED0>, orderState=<ib.ext.OrderState.OrderState object at 0x032F6FD0>>
##Server Response: orderStatus, <orderStatus orderId=25, status=Submitted,
##    filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027008, parentId=0, lastFillPrice=0.0, clientId=100, whyHeld=None>
###########################
def create_ticksym(symbol_id,sym,ibsecType,ibexchange,cashcurr,expiry):
    contract = Contract()  
    contract.m_symbol = sym
    contract.m_secType = ibsecType 
    contract.m_exchange = ibexchange
    contract.m_currency = cashcurr
    if ibsecType  == 'FUT':
        contract.m_expiry = expiry
    return contract
###############################
def create_order(order_type, quantity, action, limitprice, transmitf, auxprice, stopprice, rptype):
    order = Order()
    order.m_action = action
    order.m_totalQuantity = quantity
    order.m_transmit = transmitf
    order.m_orderType = order_type
    if order_type == 'LMT':
        order.m_lmtPrice = limitprice
        pass
    elif order_type  == 'STP':
        order.m_stpPrice = stopprice
        pass
    else:
        print'failing on price...need one'
    return order
#####################
##if ordernumx == 'filled':
##    launch profittake and stopbracket with ocaGroup
##reqIds()
##orderStatus()
##ParentID
##ocaType
##ocaGroup
###############################
##datahandler for snapshots
##reqmktdata live data
##req live recent bars
##PlaceOrder(entryorder)
##if entryorder filled:
##    PlaceOrder(profitorder)
##    get orderid
##    PlaceOrder(profitorder by number, transmit)
##    PlaceOrder(stopbracket) # with transmit true 
    '''
##################################
# Connect to  (TWS) on theusual port of 7496, with a clientId of 69
 clientId we need separate IDs for  execution connection andmarket data connection)
 '''
tws_conn = Connection.create(port=7496, clientId=69)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.reqAccountUpdates(True,'U87392')

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
timelimit = 2
timer = 1
#################
while timer < timelimit:
    sigs = rpu_rp.CsvToLines('sigs.csv')
    onesig = rpu_rp.tail_array_to_array(sigs,2)
    for sig in onesig:
        tws_conn.reqIds(100)
        sleep(1)
        for l in rpu_rp.CsvToLines('OrderIdsSaved.csv'):
            order_id = int(l[0])
            ##################
        print sig # ['13:51:58', 'USD.CAD', '30 secs', '12436.5002', '-0.007', 'negcrossmcd', 'necd']]   
        sym = sig[1]
        action = sig[5]
        decimalboost = float(dboostdict[sym])
        onetick = float(tickdict[sym])
        roundfactor = int(roundfactordict[sym])
        print decimalboost, onetick, roundfactor
        price = round(float((sig[3]))/float(decimalboost),roundfactor)
        onetick = float(1/decimalboost)
        if action == 'poscrossmcd':
            tside = 'BUY'
            flipside = 'SELL'
            profprice = round(price + (2 * onetick),roundfactor)
        else:
            tside = 'SELL'
            flipside = 'BUY'
            profprice = round(price - (2 * onetick),roundfactor)
        print 'enter trade'     
        # Create an order ID which is 'global' for this session.....
        symib = symdict[sym] 
        ibsecType = typedict[sym] #'CASH'
        ibexchange = exchdict[sym] #'IDEALPRO'
        cashcurr = currdict[sym] #'USD'
        expiry = expiredict[sym] #'ignore'
        tsize = tsizedict[sym] #'ignore'
        
        symcontract = create_ticksym(14,symib, ibsecType, ibexchange, cashcurr,expiry)
        tws_conn.reqMktData(14,symcontract,'BID',True) ## use this to get a valid price
        sleep(1)
        for l in rpu_rp.CsvToLines('pricenow'):
            pricenow = float(l[0])
            print pricenow
        if tside == 'BUY':
            profprice = round(pricenow + (2 * onetick),roundfactor)
        else:
            profprice = round(pricenow - (2 * onetick),roundfactor)
        entryorder = create_order('LMT', tsize, tside, pricenow,True,pricenow,pricenow,'entry')
        print('LMT', tsize, tside, pricenow,True,pricenow,pricenow,'entry')
        profitorder = create_order('LMT', tsize, flipside, profprice,True,profprice,profprice,'profit')
        print('LMT', tsize, flipside, profprice,True,profprice,profprice,'profit')

##        profitTrailSTP = create_order('TRAIL', tsize, flipside, profprice,True,profprice,profprice,'TRAIL',trailamount)

    ##    create_order(order_type, quantity, action, limitprice,transmitf,auxprice,stopprice,rptype)  
        ans = 'y'
##        ans = raw_input('continue to place order?')
##        import ctypes  # An included library with Python install.
##        def Mbox(title, text, style):
##            ctypes.windll.user32.MessageBoxA(0, text, title, style)
##        ans = Mbox('continue to place order?', ordtxt, 3)
        print ans
##        put a timer above this to timeout if no response and bail and disconnect
        if ans == 'y':
            print 'placing order'
##            tws_conn.placeOrder(order_id, symcontract, entryorder)
##            tws_conn.placeOrder(order_id +1, symcontract, profitorder)
##            sleep(1)
            
            tws_conn.reqPositions(62,1)
##            tws_conn.OrderStatus(order_id)
        else:
            print 'doing nothing..back into loop..'
        sleep (5)
    ##    rpu_rp.WriteStringsToFileAppend('OrderIdsSaved.csv','1')
    ##    tws_conn.reqExecutions(3,)
    ##############    tws_conn.reqAllOpenOrders()
    ##    tws_conn.cancelOrder(order_id)
    timer += 1
print 'disconnecting..loop is done..'
tws_conn.disconnect()
####################reqGlobalCancel()
## enter a trailstop as profit order...
