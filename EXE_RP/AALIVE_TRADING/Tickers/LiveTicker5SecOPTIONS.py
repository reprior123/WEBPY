import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp, rpInd, ibutiles, TicksUtile
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global today, sym, symbol_list, symdict, symbol_list2
symbol_list = symbol_list2
########################################
replyfile = TMP +'reply.options.RTticks'
symTickerIddict ={}
contractdict ={}
reqIDsym=0

expiry_list = ['20151218','20160115','20150219']
c=0
symbol_list=[]
basesym = 'SPY'
####### create symbol list   #####
while c < len(expiry_list):
    expiry = expiry_list[c]
    sym = basesym +'F' + str(c)
    symbol_list.append(sym)   
    c+=1
##############
for sym in symbol_list:
    reqIDsym+=1
    symTickerIddict.update({str(reqIDsym) : sym})
    fname1 = DataDown+ today + '.' + sym  +'.RTticksopts.csv'
    TicksUtile.backupTickfiles(fname1)
    rpu_rp.WriteArrayToCsvfile(fname1,[])   
rpu_rp.WriteArrayToCsvfile(replyfile,[])
#################
onerow =[]
def RTBar_reply_handler(msg):
    if msg.typeName == 'realtimeBar':
        reqid=(((str(msg)).split()[1]).split('=')[1]).replace(',','')
        sym=symTickerIddict[reqid]
        onerow = (str(msg)).split(',')
        cleanonerow = TicksUtile.format_RTTickoneline_to_5secBars(onerow,sym)
        rpu_rp.WriteArrayToCsvfileAppend(DataDown +today+'.'+sym+ '.RTticksopts.csv',[cleanonerow])
        rpu_rp.WriteArrayToCsvfile(DataDown +today+'.'+sym+ '.RTticksoptslastquote.csv',[cleanonerow])
    else:
        print str(msg)
        rpu_rp.WriteStringsToFileAppend(replyfile,str(msg))
#################################
print 'Connecting to Live DATAFEED...please wait'
print 'Collecting 5Second Tick Bars in realtime for the following symbols...'
print symbol_list
tws_conn = Connection.create(port=7496, clientId=166) #need separate IDs for both the execution connection and
tws_conn.connect()
tws_conn.register(ibutiles.error_handler, 'Error')
tws_conn.registerAll(RTBar_reply_handler)
##########################
cycletime = 120 ## will need to be increase for more products because of delay
loopmax = 3 # = allday
loop = 1
################
reqID=1

c=0
while c < len(expiry_list):
    expiry = expiry_list[c]
    sym = symbol_list[c]
    strike = 208.0
    c+=1
    contract = ibutiles.create_contractOPTION(sym,strike,expiry)
    ticktype = 'MIDPOINT' # ticktypedict[sym]
    tws_conn.reqRealTimeBars(reqID,contract,'',ticktype,0)
    reqID +=1        
    sleep(1)
#############
symlist = symbol_list
barlist = barlist_All
rpu_rp.WriteArrayToCsvfile(TMP +'symlistopy.csv',[symlist])
rpu_rp.WriteArrayToCsvfile(TMP+'barlistopt.csv',[barlist])

while loop < loopmax:
    ###############
    loop += 1
    sleep(cycletime) ## careful if this results in neg num, just hangs
    print 'REALTIME TICKER heartbeat is active',loop
    ################
print 'disconnecting..LIVE ticker has stopped !!!!!!!loop is done..'
tws_conn.disconnect()
