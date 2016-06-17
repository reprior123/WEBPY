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
import ctypes
###################################
print 'entry sender'
global recentlimit, decimalboost, time_format,today,timedate_format, nextorderID
####################
online = 'online'
if online == 'online':
    repliesfile = TMP + 'entryreplys'
    pass
else:
    repliesfile =  TMP + 'entryreplys.test.txt'
###############
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#######################
def localreply_handler(msg):
    if msg.typeName == 'nextValidId':
        nextorderID = msg.orderId
        rpu_rp.WriteStringsToFile(TMP +'OrderIdsSavedlocalsigcreate.csv',str(nextorderID)+ ',')   
    rpu_rp.WriteStringsToFileAppend(repliesfile,str(msg))
    print str(msg)
####################
print 'mode is ' + online
if online == 'online':
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
def get_orderidfromfile():
##    tws_conn.reqIds(100)
##    sleep(1)
    for l in rpu_rp.CsvToLines(TMP + 'OrderIdsSavedlocalsigcreate.csv'):
        order_id = int(l[0])
    return order_id
###################################
def get_latest_tick(sym):
    RecentTickFile = DataDown + today + '.' + sym + '.RTtickslastquote.csv'
    tickline = rpu_rp.tail_array_to_array(rpu_rp.CsvToLines(RecentTickFile),1)
    for f in tickline:
        if '2016' in str(f):
##            print f
            lasttick = f[5]
    return lasttick
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
global entryordsstatus_dict,entryordside_dict,entryordsym_dict
###############################
def check_status():
    print entryordsstatus_dict.keys()
    for ordid in entryordsstatus_dict.keys():
        ordsym = entryordsym_dict[ordid]
        ordside = entryordside_dict[ordid]
        currstatus = entryordsstatus_dict[ordid]
        for l in  rpu_rp.grep_Csvfile_to_array(repliesfile,'orderStatus orderId=' + str(parent_order_id)):
##            print 'xxx',l
            newstatus= l[1]
            filledstatus= l[2]
            avgprice = l[4]
#####['<orderStatus orderId=133', ' status=None', ' filled=None', ' remaining=None', ' avgFillPrice=None', ' permId=None',' parentId=None', ' lastFillPrice=None', ' clientId=None', ' whyHeld=None>']
        print newstatus, filledstatus, avgprice, ordid, ordsym, ordside, currstatus
        entryordsstatus_dict[ordid] = newstatus
    print entryordsstatus_dict
##    print entryordside_dict
##    print entryordsym_dict
######################
print 'starting entry sender...'
################
def create_con_dict():
    symcontrdict = {}
    counter = 0
    symbol_list = symbol_listall
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
    print 'done with dict'
    return symcontrdict
####################
global symcontrdict
symcontrdict = {}
if online == 'online':
    symcontrdict = {}
    symcontrdict = create_con_dict()
##################
entryordsstatus_dict ={}
entryordside_dict ={}
entryordsym_dict ={}
loopmax = 300
agelimit = 1200
loop = 0
cycledelay = 2
################################
rpu_rp.WriteStringsToFile(TMP +'Entry.orders.Sent.csv','')
############
sizemult = 3
#################
while loop < loopmax:
    loop +=1
    check_status()
    print 'entry trader hbeat.',loop, loopmax
    sleep(cycledelay)   
    siglistfile = sigarea + today +'.recentsigsexecHARD.csv'
    if os.path.isfile(siglistfile):
        sigfileage = check_for_CP_change(siglistfile)
        pass
    else:
        sigfileage = 99999999
    if os.path.isfile(siglistfile) and  sigfileage < (cycledelay + agelimit):
        recentsigs =  rpu_rp.CsvToLines(siglistfile)
        if online == 'online':                    
            parent_order_id = get_orderidfromfile()
        else:
            parent_order_id = '888'
            #################3
        for  lastsig in recentsigs:
            sym = lastsig[0]
            showdecimal = int(showdecimaldict[sym])
            tside = lastsig[1]
            if sym =='ES':
                profsig = 2
                pass
            else:
                profsig = 2
##            profsig = int(lastsig[10])
##            stopsig = profsig * 4
##            stopsig = int(lastsig[11])
##                tsize = (int(tsizedict[sym])* sizemult
            tfactor = float(0.5)
            tsize = int(max(1,(int(tsizedict[sym]) * tfactor))) * sizemult
            ttype = 'LIM'
            print 'get latest price'
            print sym
            pricenow = float(get_latest_tick(sym))
            tickvalue = float(tickvaluedict[sym]) 
            ##################################
            print symcontrdict
            if online == 'online':
                symcontract = symcontrdict[sym]
                pass
            else:
                symcontract = 'bla'
            ##################################
######                create_contract(sym,strike,expiry)
            ########################
            profmult = 1
            stpmult = 3  ###   <<<<<<<<<
            treverseside = 'SELL'
            absfadeamount = 9
            if tside == 'SELL':
                treverseside = 'BUY'
                profadd = profmult * (-1) * profsig
                fadeamount = absfadeamount
            else:
                fadeamount = absfadeamount * int(-1)
                profadd = profmult * 1 * profsig
            fadedentryprice = pricenow + fadeamount
            mktentryprice = pricenow 
            #################################
            tranflag =  False #  True # True  ### <<<<<<<<<this needs to be flipped for transmits.....!!!!!!
            #################################
            orderstring = str(parent_order_id) + ',' + tside + ',' + str(tsize)  + ',' + sym  + ',' + str(fadedentryprice)
            print 'placing order', orderstring
            rpu_rp.WriteStringsToFileAppend(TMP +'Entry.orders.Sent.csv',orderstring)    
            fadedentryorder = ibutiles.create_order('LMT', tsize, tside, fadedentryprice,tranflag,fadedentryprice,fadedentryprice,'entry')
            mktentryorder = ibutiles.create_order('LMT', tsize, tside, mktentryprice,tranflag,mktentryprice,mktentryprice,'entry')
            stopprice = mktentryprice - (stpmult*profadd)
            profprice = mktentryprice + profadd
            bracketorder = ibutiles.create_bracket_order('LMT', tsize,treverseside,profprice,tranflag,profprice,profprice,'profittxt', parent_order_id)
            bracketorderSTP = ibutiles.create_bracket_order('STP', tsize,treverseside,stopprice,tranflag,stopprice,stopprice,'stoptxt', parent_order_id)
            if online == 'online':
                tws_conn.placeOrder(parent_order_id, symcontract, fadedentryorder)
                tws_conn.placeOrder(parent_order_id+1, symcontract, bracketorder)
                tws_conn.placeOrder(parent_order_id+2, symcontract, bracketorderSTP)
                sleep(1)
                tws_conn.placeOrder(parent_order_id, symcontract, mktentryorder)
                tws_conn.orderStatus(parent_order_id)
                
                entryordsstatus_dict[parent_order_id] = 'openstatus'
                entryordside_dict[parent_order_id] = tside #{}
                entryordsym_dict[parent_order_id] =  sym #{}
                entryordsym_dict[parent_order_id] =  sym #{}
                get_orderid() ### simply asks the reply file for next valid number [not read here]
            if os.path.isfile(siglistfile):
                shutil.copyfile(siglistfile, 'temp')
                os.remove(siglistfile)
            ##########  end of if clause sig file changed
print 'finished ',loopmax,' loops  by Signal Creator...dead since..'
print 'disconnecting.. done..'
if online == 'online':
    tws_conn.disconnect()
#############
########def scan_for_fills():
########    openarray = []
########    fillNoProf = []
########    filledNProfSent = []
########    replys = rpu_rp.CsvToLines( TMP + 'entryreplys') ## this reads the replies from the sigcreate login
########    for l in  rpu_rp.CsvToLines(entrysSentFile):
########        if len(l) > 0:
########            print l, 'checking for this in entries with a status poll'
########            status ='open'
########            listordid = l[0]
########            #poll for status
########            tws_conn.orderStatus(listordid)
########            sleep(1) ### give it time to read list
########    ##        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
########            for rep in replys:
########                ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
########                if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
########                    print 'found a fill in entry orders', listordid
########                    status='filled'
########                if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##########                    print 'found a fill in entry orders', listordid
########                    status='cxld'
########            if status  == 'filled':
########                fillNoProf.append(l)
########                pass
########            elif status == 'cxld':
##########                print 'was cxld, deleting from list',l
########                pass
########            else:
########                openarray.append(l)
##########                print 'is open still',l
########    rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
########    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
########
########    ##########
########def scan_for_fillsfromfile():
########    openarray = []
########    fillNoProf = []
########    filledNProfSent = []
########    replys = rpu_rp.CsvToLines( repliesfile) ## this reads the replies from the sigcreate login
########    status ='open'
########    listordid = parent_order_id
########
##########        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
########    for rep in replys:
########        ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
########        if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
########            print 'found a fill in entry orders', listordid
########            status='filled'
########        if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##########                    print 'found a fill in entry orders', listordid
########            status='cxld'
########    if status  == 'filled':
########        fillNoProf.append(l)
########        pass
########    elif status == 'cxld':
##########                print 'was cxld, deleting from list',l
########        pass
########    else:
########        openarray.append(l)
##########                print 'is open still',l
##########rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
##########rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
