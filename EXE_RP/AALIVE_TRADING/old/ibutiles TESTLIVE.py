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
global nextorderID
def reply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile('OrderIdsSaved.csv',str(nextorderID)+ ',')
        print 'the next #############is  ', nextorderID, '   #######'
    if msg.typeName ==   'orderStatus':
        pass
##     Server Response: orderStatus, <orderStatus orderId=33, status=Submitted,
##     filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027016, parentId=0,
##     lastFillPrice=0.0, clientId=100, whyHeld=None
# parse snapshots    
##        ibutiles.parse_tickSnapshot(msg,sym,today,fname)
    print "Server Response: %s, %s" % (msg.typeName, msg)
##    Server Response: openOrder, <openOrder orderId=25, contract=<ib.ext.Contract.Contract object at 0x032F6F70>, order=<ib.ext.Order.Order
##    object at 0x032F6ED0>, orderState=<ib.ext.OrderState.OrderState object at 0x032F6FD0>>
##Server Response: orderStatus, <orderStatus orderId=25, status=Submitted,
##    filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027008, parentId=0, lastFillPrice=0.0, clientId=100, whyHeld=None>
####################
def parse_tickSnapshot(snapshotmsgline):
    if msg.field == 1:
        quotearray[1] = msg.price
    if bidstringsize in str(msg):
        quotearray[2] = msg.size
    if askstring in str(msg):
        quotearray[3] = msg.price
    if askstringsize in str(msg):
        quotearray[4] = msg.size
        sym = symlist[msg.tickerId-1]
        quotearray[5] = sym
        quotearray[6] = today
    if msg.typeName == 'tickSnapshotEnd':
        quotearray[0] = datetime.now().time().isoformat()
        linearray = []
        linearray.append(quotearray)
        rpu_rp.WriteArrayToCsvfileAppend(fname,linearray)
        pass
##read dictsnapfields....library.snapshotfields.csv
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
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_lmtPrice = limitprice
    order.m_transmit = transmitf
    if rptype == 'profittake':
        pass
    if rptype == 'stopbracket':
        pass    
    return order
#####################
##if ordernumx == 'filled':
##    launch profittake and stopbracket with ocaGroup
    pass
#
##reqIds()
##orderStatus()
##ParentID
##ocaType
##ocaGroup
###############################
##datahandler for snapshots
##reqmktdata live data
##req live recent bars

##
##PlaceOrder(entryorder)
##if entryorder filled:
##    PlaceOrder(profitorder)
##    get orderid
##    PlaceOrder(profitorder by number, transmit)
##    PlaceOrder(stopbracket) # with transmit true
##    
#####################
def requestorderidafternotransmit():
    pass
#####################    
    '''
if a bracket order need parentId, and to not transmit until the order is sent, an
id received and attached to the brackets, and then send
    order.m_transmit = false
    return order
##############################
def process_snaps(lineormsg):
    priceTicks = {1: 'bid', 2: 'ask', 4: 'last', 6: 'high', 7: 'low', 9: 'close', 14: 'open'}
    timeFormat = "%Y%m%d %H:%M:%S"
    dateFormat = "%Y%m%d"
######################################
The __main__ function initially creates a Connection object to Trader Workstation,
which must be running for the code to function.
Subsequently an order_id variable is
defined. In a production system this must be incremented for each trade order.
'''
##################################
# Connect to the Trader Workstation (TWS) running on the
# usual port of 7496, with a clientId of 69
# (The clientId is chosen by us and we will need 
# separate IDs for both the execution connection and
# market data connection)
##global tws_conn
##def connectallTWS():
tws_conn = Connection.create(port=7496, clientId=69)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)    
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
            profprice = round(price + (3 * onetick),roundfactor)
        else:
            tside = 'SELL'
            flipside = 'BUY'
            profprice = round(price - (3 * onetick),roundfactor)
        print 'enter trade'     
        # Create an order ID which is 'global' for this session.....
        symib = symdict[sym] 
        ibsecType = typedict[sym] #'CASH'
        ibexchange = exchdict[sym] #'IDEALPRO'
        cashcurr = currdict[sym] #'USD'
        expiry = expiredict[sym] #'ignore'
        tsize = tsizedict[sym] #'ignore'
        
        symcontract = create_ticksym(14,symib, ibsecType, ibexchange, cashcurr,expiry)
        sym_order = create_order('LMT', tsize, tside, price,True,price,price,'entry')
        profitorder = create_order('LMT', tsize, flipside, profprice,True,profprice,profprice,'profit')
        ordtxt = 'LMT '+ str(tsize)+  str(tside)+  str(price)+'False'+ str(price)+ str(price)+ str('entry')
        print ordtxt
    ##    create_order(order_type, quantity, action, limitprice,transmitf,auxprice,stopprice,rptype)  
    ##    tws_conn.reqMktData(14,symcontract,'BID',True) ## use this to get a valid price    
        ans = 'y'
##        raw_input('continue to place order?')
##        import ctypes  # An included library with Python install.
##        def Mbox(title, text, style):
##            ctypes.windll.user32.MessageBoxA(0, text, title, style)
##        ans = Mbox('continue to place order?', ordtxt, 3)
        print ans
##        put a timer above this to timeout if no response and bail and disconnect
        if ans == 'y':
            tws_conn.placeOrder(order_id, symcontract, sym_order)
            tws_conn.placeOrder(order_id +1, symcontract, profitorder)
##            sleep(1)
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
##reqGlobalCancel()
## enter a trailstop as profit order...
