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
global today
today =  rpu_rp.todaysdateunix()
####################
sym = 'EUR'
arrayin = rpu_rp.grep_Csvfile_to_array('ticksnaps.csv',sym)
##arrayin = rpu_rp.CsvToLines('ticksout.csv')
barticksize = 20
bartimesize =999999
mode = 'fullbar'
bla = rpInd.create_bars_from_snapshots(arrayin,barticksize,bartimesize,mode)
for l in bla:
    print l

'''
from datetime import datetime
fname = 'ticksnaps.csv'
if 'fileisnotthere' == 'fileisnotthere':
    rpu_rp.WriteStringsToFile(fname,'')   
bidstring = 'field=1'
bidstringsize = 'field=0'
askstring = 'field=2'
askstringsize = 'field=3'
bid = ask = bidsize = asksize = 0
global quotearray
quotearray =[1,0,0,0,0,'bla','somedate']
global linearray
linearray =[]
def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg
def reply_handler(msg):
    """Handles of server replies"""
    if msg.typeName == 'tickPrice' or msg.typeName == 'tickSize':
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
    if  msg.typeName != 'tickPricexxx' and msg.typeName != 'tickSizexxx':
        print "Server Response: %s, %s" % (msg.typeName, msg)           
####################
##def parse_tickSnapshot(snapshotmsg):

field 0 =  bidsize, f1 = bid price
field 2 = ask, f3 = asksize
f4 = ?
f6 = hi, f7= low, f9 = last
Server Response: tickPrice, <tickPrice tickerId=2, field=1, price=1.5465, canAutoExecute=1>
Server Response: tickSize, <tickSize tickerId=2, field=0, size=2070000>

###########################
def create_ticksym(symbol_id,sym,ibsecType,ibexchange,cashcurr,expiry):
    contract = Contract()  
    contract.m_symbol = sym
    contract.m_secType = ibsecType 
    contract.m_exchange = ibexchange
    contract.m_currency = cashcurr
    if sym  == 'ES':
        contract.m_expiry = expiry
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
# (The clientId is chosen by us and we will need 
# separate IDs for both the execution connection and
tws_conn = Connection.create(port=7496, clientId=111)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
################
timelimit = 360
timer = 1
global symlist
symlist = ['EUR', 'GBP', 'AUD']
##symlist = ['EUR']
global sym
order_id = 1
while timer < timelimit:
    order_id = 1
    for sym in symlist:        
        print sym
        ibsecType = 'CASH'  
        ibexchange = 'IDEALPRO'
        cashcurr = 'USD'
        expiry = 'none'
        ticksym = create_ticksym(order_id,sym,ibsecType,ibexchange,cashcurr,expiry)
        tws_conn.reqMktData(order_id,ticksym,'BID',True)
        order_id +=1
        cycletime = ((len(symlist))*2)
        sleep(2)
    timer += 1
    sleep(10-cycletime)
    print 'running next loop'
print 'disconnecting..loop is done..'
tws_conn.disconnect()
##reqGlobalCancel()
'''
