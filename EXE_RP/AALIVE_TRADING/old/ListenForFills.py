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
sigarea = EXE + 'IbPy-master/Signals/'
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
today =  rpu_rp.todaysdateunix()
from datetime import datetime
##############################
def reply_handler(msg):
    print "Server Response: %s, %s" % (msg.typeName, msg)
    rpu_rp.WriteStringsToFileAppend('ibreplys',str(msg))
####################
##     Server Response: orderStatus, <orderStatus orderId=33, status=Submitted,
##     filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027016, parentId=0,
##     lastFillPrice=0.0, clientId=100, whyHeld=None 
##    Server Response: openOrder, <openOrder orderId=25, contract=<ib.ext.Contract.Contract object at 0x032F6F70>, order=<ib.ext.Order.Order
##    object at 0x032F6ED0>, orderState=<ib.ext.OrderState.OrderState object at 0x032F6FD0>>
##Server Response: orderStatus, <orderStatus orderId=25, status=Submitted,
##    filled=0, remaining=25000, avgFillPrice=0.0, permId=1410027008, parentId=0, lastFillPrice=0.0, clientId=100, whyHeld=None>
###########################
global tws_conn
tws_conn = Connection.create(port=7496, clientId=77)
tws_conn.connect()
tws_conn.register(error_handler, 'Error')
tws_conn.registerAll(reply_handler)
tws_conn.reqAccountUpdates(False,'U87392')
sleep(500)
tws_conn.disconnect()
####reqGlobalCancel()
## enter a trailstop as profit order...
##        tws_conn.reqPositions(62,1)
    ##    tws_conn.reqExecutions(3,)
    ##    tws_conn.reqAllOpenOrders()
    ##    tws_conn.cancelOrder(order_id)
