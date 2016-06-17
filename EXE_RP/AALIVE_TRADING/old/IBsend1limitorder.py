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
