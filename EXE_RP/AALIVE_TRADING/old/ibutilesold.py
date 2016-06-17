# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
########################
import  rpu_rp, rpInd
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today
today =  rpu_rp.todaysdateunix()
from datetime import datetime
###########################
def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg
def reply_handler(msg):
    """Handles of server replies"""
    if msg.typeName == 'tickPrice' or msg.typeName == 'tickSize':
##        ibutiles.parse_tickSnapshot(msg,sym,today,fname)
        pass
        print "Server Response: %s, %s" % (msg.typeName, msg)           
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
'''
read dictsnapfields....library.snapshotfields.csv

field 0 =  bidsize, f1 = bid price  field 2 = ask, f3 = asksize  f4 = ? f6 = hi, f7= low, f9 = last
Server Response: tickPrice, <tickPrice tickerId=2, field=1, price=1.5465, canAutoExecute=1>
Server Response: tickSize, <tickSize tickerId=2, field=0, size=2070000>
'''
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
#################################
def create_order(order_type, quantity, action, limitprice):
    ''''MKT', 'LMT'  '''
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_lmtPrice = limitprice
    return order
###############################
def create_mainorder(order_type, quantity, action, limitprice,transmitf,auxprice,stopprice,rptype):
    order1 = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_lmtPrice = limitprice
    order.m_transmit = transmitf
    if rptype == 'profittake':
        pass
    if rptype == 'stopbracket':
        pass
    
    return order1
#####################
if ordernumx == 'filled':
    launch profittake and stopbracket with ocaGroup
    pass
#
reqIds()
orderStatus()
ParentID
ocaType
ocaGroup

###############################
datahandler for snapshots
reqmktdata live data
req live recent bars


PlaceOrder(entryorder)
if entryorder filled:
    PlaceOrder(profitorder)
    get orderid
    PlaceOrder(profitorder by number, transmit)
    PlaceOrder(stopbracket) # with transmit true
    
#####################
    def requestorderidafternotransmit():
        pass
#####################    
    '''
if a bracket order need parentId, and to not transmit until the order is sent, an id received and attached to the brackets, and then send

    order.m_transmit = false
    return order
##############################
def process_snaps(lineormsg):
    priceTicks = {1: 'bid', 2: 'ask', 4: 'last', 6: 'high', 7: 'low', 9: 'close', 14: 'open'}
    timeFormat = "%Y%m%d %H:%M:%S"
    dateFormat = "%Y%m%d"
'''
######################################
    ########## move  this after testing  ####
import  rpu_rp, rpInd, ibutiles
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
def error_handler(msg):
    print "Server Error: %s" % msg
def reply_handler(msg):
    print "Server Response: %s, %s" % (msg.typeName, msg)
##############################
'''The __main__ function initially creates a Connection object to Trader Workstation,
which must be running for the code to function.
Subsequently an order_id variable is
defined. In a production system this must be incremented for each trade order.
'''
##################################
# Connect to the Trader Workstation (TWS) running on the
# usual port of 7496, with a clientId of 100
# (The clientId is chosen by us and we will need 
# separate IDs for both the execution connection and
# market data connection)
tws_conn = Connection.create(port=7496, clientId=100)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
################
timelimit = 2
timer = 1
while timer < timelimit:   
    print 'running next loop'     
    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = timer
    symcontract = ibutiles.create_ticksym(14,'EUR', 'CASH', 'IDEALPRO', 'USD','ignoreexp')
    sym_order = ibutiles.create_order('LMT', 100000, 'SELL', 1.1498)
    tws_conn.reqMktData(14,symcontract,'BID',True)
    # Use the connection to the send the order to IB
    tws_conn.placeOrder(order_id, symcontract, sym_order)
    sleep(5)
    tws_conn.cancelOrder(order_id)
    timer += 1 
    sleep(5)

# Disconnect from TWS
print 'disconnecting..loop is done..'
tws_conn.disconnect()

##reqGlobalCancel()
