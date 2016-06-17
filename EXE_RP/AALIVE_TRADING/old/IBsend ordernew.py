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
import rputiles, rpu_rp, rpInd
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
'''
global today
today =  rpu_rp.todaysdateunix()
##ibsecType = 'CASH'  
##ibexchange = 'IDEALPRO'
##cashcurr = 'USD'
newDataList = []
################################
'''
from datetime import datetime
fname = 'ticksnaps.csv'
if 'fileisnotthere' == 'fileisnottherexxx':
    rpu_rp.WriteStringsToFile(fname,'')   
bidstring = 'field=1'
bidstringsize = 'field=0'
askstring = 'field=2'
askstringsize = 'field=3'
bid = ask = bidsize = asksize = 0
global quotearray
quotearray =[1,0,0,0,0]
global linearray
linearray =[]
def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg
def reply_handler(msg):
    """Handles of server replies"""
    if '<historicalData' not in str(msg):
        print "Server Response: %s, %s" % (msg.typeName, msg)
    if msg.typeName == 'tickPrice' and bidstring in str(msg):
        quotearray[1] = msg.price
    if bidstringsize in str(msg):
        quotearray[2] = msg.size
    if askstring in str(msg):
        quotearray[3] = msg.price
    if askstringsize in str(msg):
        quotearray[4] = msg.size
    if 'SnapshotEnd' in str(msg):
        quotearray[0] = datetime.now().time().isoformat()
        print quotearray
##        fullline= str(quotearray)
##        print fullline
        linearray = []
        linearray.append(quotearray)
        rpu_rp.WriteArrayToCsvfileAppend(fname,linearray)
        linearray = []
    ####################
'''
Server Response: tickPrice, <tickPrice tickerId=14, field=1, price=1.1172, canAutoExecute=1>
Server Response: tickSize, <tickSize tickerId=14, field=0, size=8179000>
Server Response: tickPrice, <tickPrice tickerId=14, field=2, price=1.11725, canAutoExecute=1>

     ###########################
def build_qqq_msg(symbol_id,sym,ibsecType,ibexchange,cashcurr):
    print sym
    qqq = Contract()  
    qqq.m_symbol = sym  
    qqq.m_secType = ibsecType 
    qqq.m_exchange = ibexchange
    qqq.m_currency = cashcurr
    if sym  == 'ES':
        qqq.m_expiry = '20150619'
    return qqq
####################################

trans_id = 0
ibsecType = 'CASH'  
ibexchange = 'IDEALPRO'
cashcurr = 'USD'
##################################
'''
##The following two functions wrap the creation of the Contract and Order objects,
##setting their respective parameters. The function docs describe each parameter individually:
def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.
    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract
#################################
def create_order(order_type, quantity, action, limitprice):
    """Create an Order object (Market/Limit) to go long/short.
    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_lmtPrice = limitprice
    return order
##############################
'''The __main__ function initially creates a Connection object to Trader Workstation,
which must be running for the code to function. The error and reply handler functions
are then registered with the connection object. Subsequently an order_id variable is
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
timelimit = 100
timer = 1
while timer < timelimit:   
    print 'running next loop'     
    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = timer
    goog_contract = create_contract('EUR', 'CASH', 'IDEALPRO', 'IDEALPRO', 'USD')
    goog_order = create_order('LMT', 100000, 'SELL', 1.1198)
    tws_conn.reqMktData(14,goog_contract,'BID',True)
    # Use the connection to the send the order to IB
##    tws_conn.placeOrder(order_id, goog_contract, goog_order)
##    sleep(5)
##    tws_conn.cancelOrder(order_id)
    timer += 1 
    sleep(5)

# Disconnect from TWS
print 'disconnecting..loop is done..'
tws_conn.disconnect()


##reqGlobalCancel()
