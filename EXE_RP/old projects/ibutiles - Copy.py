# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
EXE = EXEnoslash +'/'
TMP = rootpath + 'TMP' + localtagSLASH

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
global today
global nextorderID
today =  rpu_rp.todaysdateunix()
from datetime import datetime
##############################
def error_handler(msg):
    if  'historicalData' in str(msg):
        print 'error probably pacing hist data'
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        print "Server Error: %s" % msg
##################################
def error_handlerenter(msg):
    if  'historicalData' in str(msg):
        print 'error probably pacing hist data'
        pass
    elif 'connection is OK' in str(msg):
        pass
    else:
        print "Server Error: %s" % msg
################################## 
def reply_handler(msg,replyfname):
    replyfname = TMP +'replys'
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
###########################
def create_ticksym(symbol_id,sym):
    libsyms = EXE + 'library.syms.csv'
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
    symib = symdict[sym] 
    ibsecType = typedict[sym] #'CASH'
    ibexchange = exchdict[sym] #'IDEALPRO'
    cashcurr = currdict[sym] #'USD'
    expiry = expiredict[sym] #'ignore'  
    contract = Contract()  
    contract.m_symbol = symib
    contract.m_secType = ibsecType 
    contract.m_exchange = ibexchange
    contract.m_currency = cashcurr
    if ibsecType  == 'FUT':
        contract.m_expiry = expiry
        sleep(2)
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
#####################
