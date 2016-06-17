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
print 'entry sender'
global recentlimit, decimalboost, time_format, timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, nextorderID
##############################
def error_handler(msg):
    if 'connection is OK' in str(msg):
        pass
    else:
        print "Server Error: %s" % msg
##################################
def reply_handler(msg):
    if msg.typeName == 'historicalData':
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        rpu_rp.WriteStringsToFileAppend(replyfname,str(msg))
#################
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
###############################
def create_contract(sym,strike,expiry):
    symib = symdict[sym] 
    ibsecType = typedict[sym] #'CASH'
    ibexchange = exchdict[sym] #'IDEALPRO'
    cashcurr = currdict[sym] #'USD'
    right = optrightdict[sym] #'ignore'
    print symib,ibsecType,ibexchange,cashcurr,expiry,strike,right
    contract = Contract()  
    contract.m_symbol = symib
    contract.m_secType = ibsecType 
    contract.m_exchange = ibexchange
    contract.m_currency = cashcurr
    if ibsecType  == 'FUT':
        expiry = expiredict[sym]
        contract.m_expiry = expiry
        contract.m_tradingClass = sym
    if ibsecType  == 'OPT':
        contract.m_expiry = expiry
        contract.m_strike = strike
        contract.m_right = right
        contract.m_tradingClass = symib
        sleep(1)
    return contract
###############################
def create_order(order_type, quantity, action, limitprice, transmitf, auxprice, stopprice, rptype):
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    order.m_lmtPrice = limitprice
    order.m_transmit = transmitf
    order.m_faGroup = 'rpacct'
##    order.m_faProfile = 'allocateALL'
    order.m_faMethod = 'AvailableEquity'
    if order_type == 'LMT':
        pass
##        order.m_lmtPrice = limitprice
    elif order_type  == 'STP':
        order.m_auxPrice = stopprice
    else:
        print'failing on price in ibutiles..bad order type...need one'
    return order
#####################
'''
can also use OPTION_IMPLIED_VOLATILITY iun historic download
'''
