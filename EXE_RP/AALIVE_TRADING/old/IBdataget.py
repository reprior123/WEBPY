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
####################### 
global mode
mode = 'fullfile'
global symbol_list
symbol_list = ['EUR', 'GBP', 'AUD', 'ES', 'USD']
ibsecType = 'CASH'  
ibexchange = 'IDEALPRO'
cashcurr = 'USD'
expiry = '20150619'
global today
today =  rpu_rp.todaysdateunix()
newDataList = []  
dataDownload = []
#############################
def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg
def reply_handler(msg):
    """Handles of server replies"""
    if msg.typeName == 'historicalData':
        pass
    else:
        print "Server Response: %s, %s" % (msg.typeName, msg)
#################################################
def historical_data_handler(msg):  
    global newDataList  
    #print msg.reqId, msg.date, msg.open, msg.high, msg.low, msg.close, msg.volume
    print msg
    if ('finished' in str(msg.date)) == False:  ### keep building the list
        new_symbol = symbol_list[msg.reqId]  
        dataStr = '%s, %s, %s, %s, %s, %s, %s' % (new_symbol, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close, msg.volume)  
        newDataList = newDataList + [dataStr]  
    else:  
        pass
    return newDataList
     ###########################
def build_qqq_msg(symbol_id,i,ibsecType,ibexchange,cashcurr):
    print i
    qqq = Contract()  
    qqq.m_symbol = i  
    qqq.m_secType = ibsecType 
    qqq.m_exchange = ibexchange
    qqq.m_currency = cashcurr
    if i == 'ES':
        qqq.m_expiry = expiry
    return qqq
####################################
con = ibConnection()
mess1 = build_qqq_msg('0','EUR',ibsecType,ibexchange,cashcurr)
con.register(historical_data_handler, message.historicalData)  
con.connect()  
con.register(error_handler, 'Error')
con.registerAll(reply_handler)
#######################################
def run_fullfile_loop(barsize,duration,ibsecType,ibexchange,cashcurr):
    symbol_id = 1
    for i in symbol_list:
        global mode
        mode = 'fullfile'
        ### if fullmode, remember to delete the tick mode single files before tickmode restart
        mode = 'single'
##        global symbol_list
##        symbol_list = ['EUR', 'GBP', 'AUD', 'ES', 'USD']
        ##symbol_list = ['ES']
        ibsecType = 'CASH'  
        ibexchange = 'IDEALPRO'
        cashcurr = 'USD'
        expiry = '20150619'
        global today
        today =  rpu_rp.todaysdateunix()
                ##########################
        barlist = ['5 secs']#'5 mins', '15 mins', '1 hour', '1 day']
        barlist = ['15 mins', '1 hour', '1 day']
        ##barlist = ['5 mins']
        for bar in barlist:
            print i
            if i == 'EUR':
                ibsecType = 'CASH'  
                ibexchange = 'IDEALPRO'
                cashcurr = 'USD'
            elif i == 'ES':
                ibsecType = 'FUT'  
                ibexchange = 'GLOBEX'
                cashcurr = 'USD'
                expiry = '20150619'
            elif i == 'USD':
                ibsecType = 'CASH'  
                ibexchange = 'IDEALPRO'
                cashcurr = 'CHF'
            else:
                ibsecType = 'CASH'  
                ibexchange = 'IDEALPRO'
                cashcurr = 'USD'
            if bar == '5 mins' or bar == '15 mins':
                duration = '2 D'
                pass
            elif bar == '1 hour':
                duration = '7 D'
                pass
            elif bar == '5 secs':
                duration = '7200 S'
            else:
                duration = '3 M'
            newqqq = build_qqq_msg(symbol_id,i,ibsecType,ibexchange,cashcurr)
            global filename
            filename = 'ibdata.' + barsize.replace(' ','') + '.' + duration.replace(' ','') + '.' + today +'.'+ i + '.csv'
            con.reqHistoricalData(symbol_id, newqqq, '', duration, barsize, 'BID_ASK', 0, 2)  
            symbol_id = symbol_id + 1  
            sleep(20)

            run_fullfile_loop(bar,duration,ibsecType,ibexchange,cashcurr)

print 'disconnecting from ib..'
con.disconnect()

