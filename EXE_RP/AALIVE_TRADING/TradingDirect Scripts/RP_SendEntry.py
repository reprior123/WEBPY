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
global recentlimit, time_format,today,timedate_format, nextorderID
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot
import glob, csv, subprocess, datetime, shutil, time, os.path
from datetime import datetime
import ctypes 
print 'entry sender'
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import  rpu_rp, rpInd, ibutiles, TicksUtile
#######################
cpfname = EXE + 'entrycontroller.txt'
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    rpu_rp.WriteStringsToFileAppend(TMP + 'entryreplys',str(msg))
    print str(msg)
####################
testmode ='online'
print 'mode is ' + testmode
if testmode == 'online':
    global tws_conn
    tws_conn = Connection.create(port=7496, clientId=55)
    tws_conn.connect()
    tws_conn.register(ibutiles.error_handler, 'Error')
    tws_conn.registerAll(localreply_handler)
###################
def get_orderid():
    tws_conn.reqIds(100)
    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
    return order_id
###################################
def get_latest_tick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)[0]
    for f in tickline:
        if 'close' in str(f):                        
            lasttick = f.split('=')[1]
    return lasttick
#############################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
loopmax = 1
loop = 0
##recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 22 #int(read_vars('CycleTime',cpfname))
########################
import datetime as dt
################################
rpu_rp.WriteStringsToFile(TMP +'Entry.orders.Sent.csv','')
sizemult = 1
##############################
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
##libsyms = EXE + 'library.syms.csv'
##symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
######################
print 'starting entry sender...'
##print
symcontrdict = {}
counter = 0
agelimit = 1200
print symbol_list
for sym in symbol_list:
    counter +=1
    strike = '2'
    expiry ='20154'
    symcontract =  ibutiles.create_contract(sym,strike,expiry)
    print sym, counter
    sleep (1)
    dict2 = {sym : symcontract}
    symcontrdict.update(dict2)
    print 'adding to dict', sym
    #################
print 'done with dict'
while loop < loopmax:   
    siglistfile = sigarea + today +'.recentsigsexec.csv'
    if os.path.isfile(siglistfile):
        recentsigs =  rpu_rp.CsvToLines(siglistfile)
        print recentsigs
        sigfileage = check_for_CP_change(siglistfile)
        if sigfileage < (cycledelay + agelimit) :
##            rpu_rp.beep(soundarea + 'OrderFilled')
            pass
            if testmode == 'online':                    
                order_id = get_orderid()
            else:
                order_id = '888'
                #################3
            for  lastsig in recentsigs:
                print lastsig
                ##['ES', 'BUY', 'ROC.15mins.BUY.ROC15.rules.csv', ' 2015-10-08 15:21:05', 'ES', '1980.5', '1981.0', ' 2015-10-08 15:21:51', 'ESBUY0minsROC.15mins.BUY.ROC15.rules.csv']
                sym = lastsig[0]
                showdecimal = int(showdecimaldict[sym])
                tside = lastsig[1]
##                tsize = (int(tsizedict[sym])* sizemult
                tfactor = float(0.5)
                tsize = int(max(1,(int(tsizedict[sym]) * tfactor))) * sizemult
                ttype = 'LIM'
                limitprice = float(lastsig[5])
                addamt = 0
                tickvalue = float(tickvaluedict[sym]) 
                ##################################
                symcontract = symcontrdict[sym]
                ##################################
######                create_contract(sym,strike,expiry)
                pricenow = limitprice
                ########################
                treverseside = 'SELL'
                if tside == 'SELL':
                    treverseside = 'BUY'
                    entrybuffer = addamt
                else:
                    entrybuffer = addamt * int(-1)
                entryprice = pricenow + entrybuffer
                #################################
                tranflag = False  ### <<<<<<<<<this needs to be flipped for transmits.....!!!!!!
                #################################
                orderstring = str(order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(entryprice)
                rpu_rp.WriteStringsToFileAppend(TMP +'Entry.orders.Sent.csv',orderstring)    
                entryorder = ibutiles.create_order('LMT', tsize, tside, entryprice,tranflag,entryprice,entryprice,'entry')
                bracketorder = ibutiles.create_bracket_order('LMT', tsize,treverseside, entryprice + 1.0 ,tranflag,entryprice,entryprice,'entry', order_id)
                bracketorderSTP = ibutiles.create_bracket_order('STP', tsize,treverseside, entryprice + 1.0 ,tranflag,entryprice-2,entryprice-2,'entry', order_id)
                if testmode == 'online':
                    tws_conn.placeOrder(order_id, symcontract, entryorder)
                    tws_conn.placeOrder(order_id+1, symcontract, bracketorder) 
                    tws_conn.placeOrder(order_id+2, symcontract, bracketorderSTP) 
                print 'placing order', orderstring
                order_id = order_id +3
                sleep(3)
                if os.path.isfile(siglistfile):
                    shutil.copyfile(siglistfile, 'temp')
                    os.remove(siglistfile)
            ##########  end of if clause sig file changed
        loop +=1

        print 'entry trader hbeat.',loop, loopmax
        sleep(cycledelay)
        #############
print 'finished ',loopmax,' loops  by Signal Creator...dead since..'
print 'disconnecting.. done..'
if testmode == 'online':
    tws_conn.disconnect()
#############
##['SIG - ES', 'BUY', 'ROC.15mins.BUY.ROC15.rules.csv', ' 2015-10-08 15:21:05', 'ES', '1980.5', '1981.0', ' 2015-10-08 15:21:51', 'ESBUY0minsROC.15mins.BUY.ROC15.rules.csv']
