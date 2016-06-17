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
#############################
global today
today =  rpu_rp.todaysdateunix()
##ibsecType = 'CASH'  
##ibexchange = 'IDEALPRO'
##cashcurr = 'USD'
newDataList = []
################################
def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg
def reply_handler(msg):
    """Handles of server replies"""
    if '<historicalData' not in str(msg):
        print "Server Response: %s, %s" % (msg.typeName, msg)
    ####################
symbol_list = ['EUR', 'AUD', 'GBP', 'ES', 'USD']
##symbol_list = ['USD']
barlist = ['1 day','5 mins', '15 mins', '1 hour']
barlist = ['5 mins', '15 mins', '1 hour']
#################################################
def historical_data_handler(msg):  
    global newDataList
    fname = today + '.' + sym + '.' + duration + bar+'.csv'
##    print msg.reqId
    if ('finished' in str(msg.date)) == False:  ### keep building the list
        dataStr = '%s, %s, %s, %s, %s, %s, %s' % (sym, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close, msg.volume)  
        newDataList = newDataList + [dataStr]  
    else:
        print 'next list'
        rpu_rp.WriteStringsToFile(fname,'')
##        rpu_rp.WriteStringsToFile(fname,newDataList)
        for a in newDataList:
##            print a
            rpu_rp.WriteStringsToFileAppend(fname,a)
        newDataList = []  
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
con = ibConnection()  
con.register(historical_data_handler, message.historicalData)  
con.connect()  
con.register(error_handler, 'Error')
con.registerAll(reply_handler)
#######################################
trans_id = 0
global sym
global bar
for sym in symbol_list:
    ibsecType = 'CASH'  
    ibexchange = 'IDEALPRO'
    cashcurr = 'USD'
    for bar in barlist:

        print bar, sym
        if bar == '5 mins' or bar == '15 mins':
            duration = '4 D'
            pass
        elif bar == '1 hour':
            duration = '7 D'
            pass
        else:
            duration = '3 M'
            pass
        if sym == 'ES':        
            ibsecType = 'FUT'  
            ibexchange = 'GLOBEX'
            pass
        if sym == 'USD':
            cashcurr = 'CHF'
        newqqq = build_qqq_msg(trans_id, sym, ibsecType, ibexchange, cashcurr)
        con.reqHistoricalData(trans_id, newqqq, '', duration, bar, 'BID_ASK', 0, 2)  
        trans_id = trans_id + 1  
        sleep(10)
###############
print 'disconnecting from ib..'
con.disconnect()
