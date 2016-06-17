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
##def localreply_handler(msg):
##    if msg.typeName == 'nextValidId':
##        nextorderID = msg.orderId
##        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
##    rpu_rp.WriteStringsToFileAppend(TMP + 'entryreplys',str(msg))
##    print str(msg)
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
def scan_for_fills():
    entrysSentFile = TMP +  'Entry.orders.Sent.csv'
    filledNoProfFile =  TMP + 'Entry.orders.FilledNoProf.csv'
    filledNProfSentFile = TMP +  'Entry.orders.FilledNProfSent.csv'
    ProfSentFile = TMP + 'Profit.orders.Sent.csv'
    openarray = []
    fillNoProf = []
    filledNProfSent = []
    replys = rpu_rp.CsvToLines( TMP + 'entryreplys') ## this reads the replies from the sigcreate login
    for l in  rpu_rp.CsvToLines(entrysSentFile):
        if len(l) > 0:
            print l
            status ='open'
            listordid = l[0]
            #poll for status
            tws_conn.orderStatus(listordid)
            sleep(3) ### give it time to read list
    ##        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
            for rep in replys:
                ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
                if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
                    print 'found a fill in entry orders', listordid
##                    status='filled'
                if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##                    print 'found a fill in entry orders', listordid
                    status='cxld'
            if status  == 'filled':
                fillNoProf.append(l)
                pass
            elif status == 'cxld':
##                print 'was cxld, deleting from list',l
                pass
            else:
                openarray.append(l)
##                print 'is open still',l
    rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
    ## enter proforders if any
    profsneeded = rpu_rp.CsvToLines(filledNoProfFile)
    profsplaced = []
    profitticks = 3
    stopticks = 14
    profmult = 1
    for entryorder in profsneeded:
        print profsneeded
        print 'those were all the profs needed'
        flipsign = int(1)
        tside = 'BUY'
        if entryorder[1] == 'BUY':
            tside  = 'SELL'
            flipsign = int(-1)
        tsize = int(entryorder[2])
        sym = entryorder[3]
        profitticks = int(profticksdict[sym])
        print 'original signal order = ', entryorder
        orderprice = float(entryorder[4])        
        decimalboost = float(dboostdict[sym])
        onetick = float(tickdict[sym])
        addamt = onetick * int(entrywiderdict[sym])
        
        tranflag = False
        profprice = orderprice - (profmult * profitticks * onetick *flipsign) - (flipsign *addamt)
        stopprice = orderprice + (stopticks * onetick *flipsign) + (flipsign *addamt)
##        print profprice,stopprice
        profitorder = ibutiles.create_order('LMT', tsize, tside, profprice,tranflag,profprice,profprice,'profit')
        stoporder = ibutiles.create_order('STP', tsize, tside, stopprice,tranflag,stopprice,stopprice,'stop')
        order_id = get_orderid()
        symcontract = ibutiles.create_ticksym(23,sym)  ## might need to vary this number at some point
        tws_conn.placeOrder(order_id, symcontract, profitorder)
        tws_conn.placeOrder(order_id+1, symcontract, stoporder)
        print 'placed a profit and stop order here '
        print sym, tside, str(tsize), str(profprice),'PROFITORDER'
        profsplaced.append(entryorder)
        sleep(4)
    rpu_rp.WriteArrayToCsvfileAppend(filledNProfSentFile,profsplaced)
    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,[])
    #####################################3
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    if msg.typeName == 'tickPrice' and 'field=1,' in str(msg) :
        rpu_rp.WriteStringsToFile(TMP +'pricenow',str(float(msg.price)) +',')
    rpu_rp.WriteStringsToFileAppend(TMP + 'FillScanner.replys',str(msg))
    ###############################
loopmax = 3000
loop = 0
global command
command = read_vars('Setting',cpfname)
recentlimit = int(read_vars('TimeLimitRecentSigs',cpfname))
cycledelay = 15 #int(read_vars('CycleTime',cpfname))
########################
import datetime as dt
################################
##rpu_rp.WriteStringsToFile(TMP +'Entry.orders.Sent.csv','')
sizemult = 2
print 'starting prof sender...'
##############################
libsyms = EXE + 'library.syms.csv'
symdict = rpu_rp.create_dict(libsyms,0,1)
symbol_list = symdict.keys()
######################

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
##########################3
while loop < loopmax:
    scan_for_fills()
    
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
