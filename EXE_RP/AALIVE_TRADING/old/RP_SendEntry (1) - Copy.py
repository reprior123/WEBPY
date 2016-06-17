# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, os.path
from datetime import datetime
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
DataDown = 'C:/TS/TSIBData/'
DataDownNoSlash = 'C:/TS/TSIBData'
sigarea = DataDown + 'Signals/'
soundarea = path + 'sounds/'
#######################################
print 'entry sender'
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
import  rpu_rp, rpInd, ibutiles, TicksUtile
from datetime import datetime
import ctypes 
#######################
cpfname = EXE + 'entrycontroller.txt'
##################
today =  rpu_rp.todaysdateunix()
##########################################
def read_varlist(cpfname): ##read variables from the control panel file
    paramlines = rpu_rp.CsvToLines(cpfname)
    lista =[]
    for line in paramlines:    
        varstring = line[0]
        lista.append(varstring)
    return lista
#########################3
def read_vars(varstringin,cpfname): ##read variables from the control panel file
##    cpfile = TMP + 'signalcontroller.txt'
    paramlines = rpu_rp.CsvToLines(cpfname)
    for line in paramlines:
##        print line
        varstring = line[0]
        if len(line) > 1 and varstring == varstringin:
            varvalue =line[1]
    return varvalue
#########################3
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    rpu_rp.WriteStringsToFileAppend(TMP + 'entryreplys',str(msg))
    print str(msg)
####################
testmode = read_vars('testmode',cpfname)
##testmode ='0ffline'
print 'mode is ',testmode
if testmode == 'online':
    global tws_conn
    tws_conn = Connection.create(port=7496, clientId=55)
    tws_conn.connect()
    tws_conn.register(ibutiles.error_handlerenter, 'Error')
    tws_conn.registerAll(localreply_handler)
else:
    pass
###################
def get_orderid():
    tws_conn.reqIds(100)
    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
    return order_id
###################################
def check_for_CP_change(fname): ##read timestamp from the control panel file
##    from datetime import datetime
    fstring = '%a %b %d %H:%M:%S %Y'
    now_epoch = time.time() 
    filetime = time.ctime(os.path.getmtime(fname))
    filetime_ep = int(time.mktime(time.strptime(filetime, fstring)))
    diff = now_epoch - filetime_ep
    return diff
#########################3
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
loopmax = 3000
loop = 0
global command
command = read_vars('Setting',cpfname)
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 15 #int(read_vars('CycleTime',cpfname))
########################
import datetime as dt
################################
rpu_rp.WriteStringsToFile(TMP +'Entry.orders.Sent.csv','')
sizemult = 2
##############################

libsyms = EXE + 'library.syms.csv'
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
######################
print 'starting entry sender...'
##print
symcontrdict = {}
counter = 0
for sym in symbol_list:
    counter +=1
    symcontract =  ibutiles.create_ticksym(counter,sym)
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
##        print recentsigs
        sigfileage = check_for_CP_change(siglistfile)
        if sigfileage < (cycledelay + 100) :
            rpu_rp.beep(soundarea + 'OrderFilled')
            if testmode == 'online':                    
                order_id = get_orderid()
            else:
                order_id = '888'
                #################3
            for  lastsig in recentsigs:
                print lastsig
                sym = lastsig[0]
                showdecimal = int(lastsig[1])
                tside = lastsig[2]
                tsize = (int(lastsig[3]))* sizemult
                ttype = lastsig[4]
                limitprice = float(lastsig[5])
                addamt = float(lastsig[6])
                tickvalue = float(lastsig[9]) 
                ##################################
                symcontract = symcontrdict[sym]
                ##########################################
                pricenow = limitprice
                ########################
                if tside == 'SELL':
                    entrybuffer = addamt
                else:
                    entrybuffer = addamt * int(-1)
                entryprice = pricenow + entrybuffer
                ##################################
                tranflag = False  ### <<<<<<<<<this needs to be flipped for transmits.....!!!!!!
                ########################################################
                orderstring = str(order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(entryprice)
                rpu_rp.WriteStringsToFileAppend(TMP +'Entry.orders.Sent.csv',orderstring)    
                entryorder = ibutiles.create_order('LMT', tsize, tside, entryprice,tranflag,entryprice,entryprice,'entry')        
                if testmode == 'online':
                    tws_conn.placeOrder(order_id, symcontract, entryorder)         
                print 'placing order'
                order_id = order_id +1
                sleep(4)
            ##########  end of if clause sig file changed
        loop +=1
        shutil.copyfile(siglistfile, 'temp')
        os.remove(siglistfile)
        print 'entry trader heartbeat..',loop, loopmax
        sleep(cycledelay)
        #############
print 'finished ',loopmax,' loops  by Signal Creator...dead since..'
print 'disconnecting.. done..'
if testmode == 'online':
    tws_conn.disconnect()
#############
