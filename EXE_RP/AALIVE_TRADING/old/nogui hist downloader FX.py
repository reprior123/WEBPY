
from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message  
import _mysql  

## new_symbolinput = ['MMM','ACE','AES','AFL','GAS','T','ABT','ANF','ACN','ADBE','AMD','AET','A','APD','ARG','AKAM','AA','ALXN','ATI','AGN','ALL','ANR','ALTR','MO','AMZN','AEE','AEP','AXP','AIG','AMT','AMP','ABC','AMGN','APH','APC','ADI','AON','APA','AIV','APOL','AAPL','AMAT','ADM','AIZ','AN','AZO','ADSK','ADP','AVB','AVY','AVP','BBT','BMC','BHI','BLL','BAC','BCR','BAX','BEAM','BDX','BBBY','BMS','BRK B','BBY','BIG','BIIB','BLK','HRB','BA','BWA','BXP','BSX','BMY','BRCM','BF B','CA','CBG','CBS','CF','CHRW','CMS','CNX','CSX','CVS','CVC','COG','CAM','CPB','COF','CAH','CFN','KMX','CCL','CAT','CELG','CNP','CTL','CERN','CHK','CVX','CME','CMG','CB','CI','CINF','CTAS','CSCO','C','CTXS','CLF','CLX','COH','KO','CCE','CTSH','CL','CMCSA','CMA','CSC','CAG','COP','ED','STZ','CBE','GLW','COST','CVH','COV','CCI','CMI','DTV','DTE','DHR','DRI','DVA','DV','DF','DE','DELL','DNR','XRAY','DVN','DO','DFS','DISCA','DLTR','D','RRD','DOV','DOW','DPS','DD','DUK','DNB','ETFC','EMC','EOG','EQT','EMN','ETN','ECL','EIX','EW','EA','EMR','ETR','EFX','EQR','EL','EXC','EXPE','EXPD','ESRX','XOM','FFIV','FLIR','FMC','FTI','FDO','FAST','FDX','FII','FIS','FITB','FHN','FSLR','FE','FISV','FLS','FLR','F','FRX','FOSL','BEN','FCX','FTR','GME','GCI','GPS','GD','GE','GIS','GPC','GNW','GILD','GS','GR','GT','GOOG','GWW','HCP','HAL','HOG','HAR','HRS','HIG','HAS','HCN','HNZ','HP','HSY','HES','HPQ','HD','HON','HRL','DHI','HSP','HST','HCBK','HUM','HBAN','ITW','IR','TEG','INTC','ICE','IPG','IBM','IFF','IGT','IP','INTU','ISRG','IVZ','IRM','JDSU','JPM','JBL','JEC','JNJ','JCI','JOY','JNPR','KLAC','K','KEY','KMB','KIM','KMI','KSS','KFT','KR','LLL','LSI','LH','LRCX','LM','LEG','LEN','LUK','LXK','LIFE','LLY','LTD','LNC','LLTC','LMT','L','LO','LOW','MTB','M','MRO','MPC','MAR','MMC','MAS','MA','MAT','MKC','MCD','MHP','MCK','MJN','MWV','MDT','MRK','MET','PCS','MCHP','MU','MSFT','MOLX','TAP','MON','MCO','MS','MOS','MSI','MUR','MYL','NKE','NRG','NYX','NBR','NDAQ','NOV','NTAP','NFLX','NWL','NFX','NEM','NWSA','NEE','NI','NE','NBL','JWN','NSC','NU','NTRS','NOC','NUE','NVDA','ORLY','OKE','OXY','OMC','ORCL','OI','PCAR','PCG','PNC','PPG','PPL','PLL','PH','PDCO','PAYX','BTU','JCP','PBCT','POM','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD','PBI','PCL','PX','PCP','PCLN','PFG','PLD','PG','PGN','PGR','PRU','PEG','PSA','PHM','QEP','QCOM','PWR','DGX','RL','RRC','RTN','RHT','RF','RSG','RAI','RHI','ROK','COL','ROP','ROST','RDC','R','SAI','SCG','SLM','SWY','CRM','SNDK','SLE','SLB','SCHW','SNI','SEE','SHLD','SRE','SHW','SIAL','SPG','SJM','SNA','SO','LUV','SWN','SE','S','STJ','SWK','SPLS','SBUX','HOT','STT','SRCL','SYK','STI','SUN','SYMC','SYY','TROW','TEL','TE','TJX','TGT','THC','TDC','TER','TSO','TXN','TXT','BK','WMB','TMO','TIF','TWC','TWX','TIE','TMK','TSS','TRV','TRIP','TYC','TSN','USB','UNP','UPS','X','UTX','UNH','UNM','URBN','VFC','VLO','VAR','VTR','VRSN','VZ','VIAB','V','VNO','VMC','WPX','WMT','WAG','DIS','WPO','WM','WAT','WPI','WLP','WFC','WDC','WU','WY','WHR','WFM','WIN','WEC','WYN','WYNN','XL','XEL','XRX','XLNX','XYL','YHOO','YUM','ZMH','ZION','EBAY']  
new_symbolinput = ['GBP','EUR','AUD']
new_symbolinput = ['USD']

newDataList = []  
dataDownload = []  

def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg

def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)
##The following two functions wrap the creation of the Contract and Order objects, setting their respective parameters. The function docs describe each parameter individually:
barsize = '5 mins'
cashcurr = 'JPY'
##cashcurr = 'USD'
duration = '2 D'
rundate = '20150430' #strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date)))
filenameroot = 'ibdata.' + barsize.replace(' ','') + '.' + duration.replace(' ','') + '.' + rundate +'.'

def historical_data_handler(msg):  
    global newDataList  
    #print msg.reqId, msg.date, msg.open, msg.high, msg.low, msg.close, msg.volume  
    if ('finished' in str(msg.date)) == False:  
     new_symbol = new_symbolinput[msg.reqId]  
     dataStr = '%s, %s, %s, %s, %s, %s, %s' % (new_symbol, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close, msg.volume)  
     newDataList = newDataList + [dataStr]  
    else:  
     new_symbol = new_symbolinput[msg.reqId]  
     filename = filenameroot + new_symbol + '.csv'  
     csvfile = open(filename,'wb')  
     for item in newDataList:  
       csvfile.write('%s \n' % item)  
     csvfile.close()  
     newDataList = []  
     global dataDownload  
     dataDownload.append(new_symbol)  

con = ibConnection()  
con.register(historical_data_handler, message.historicalData)  
con.connect()  

# Assign the error handling function defined above
# to the TWS connection
con.register(error_handler, 'Error')

# Assign all of the server reply messages to the
# reply_handler function defined above
con.registerAll(reply_handler)

symbol_id = 0  
for i in new_symbolinput:  
    print i  
    qqq = Contract()  
    qqq.m_symbol = i  
    qqq.m_secType = 'CASH'  
    qqq.m_exchange = 'IDEALPRO'  
    qqq.m_currency = cashcurr 
    con.reqHistoricalData(symbol_id, qqq, '', duration, barsize, 'BID_ASK', 0, 2)  
    symbol_id = symbol_id + 1  
    sleep(10)  

print dataDownload  
filename = 'downloaded_symbols.csv'  
csvfile = open(filename,'wb')  
for item in dataDownload:  
    csvfile.write('%s \n' % item)  
csvfile.close()

"""
Again, you need certain modules imported. Python-MySQL and IbPy, being the most important.
Here's alpha code v0.01:

from time import sleep, strftime, localtime  
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message  
from Tkinter import *  
import _mysql  
import csv  
import string  

class App:    
def __init__(self, master):  

self.newDataList = []  
self.new_symbolinput = []  
self.j=0  

#connect here to prevent double connections later on...  
self.con = ibConnection()  
self.con.register(self.historical_data_handler, message.historicalData)  
self.con.connect()  

frame = Frame(master)  
frame.pack()  

self.mysqlinfo_label = Label(frame, text='MySQL fields:')  
self.mysqlinfo_label.grid(row=0)  

self.label_host = Label(frame, text='Host:')  
self.label_host.grid(row=1)  

host_text = StringVar()  
host_text.set("127.0.0.1")  

self.entry_host = Entry(frame, textvariable=host_text)  
self.entry_host.grid(row=1, column=1)  

self.label_user = Label(frame, text='User:')  
self.label_user.grid(row=2)  

user_text = StringVar()  
user_text.set("root")  

self.entry_user = Entry(frame, textvariable=user_text)  
self.entry_user.grid(row=2, column=1)  

self.label_password = Label(frame, text='Password:')  
self.label_password.grid(row=3)  

self.entry_password = Entry(frame, show="*")  
self.entry_password.grid(row=3, column=1)  

self.label_database = Label(frame, text='Database:')  
self.label_database.grid(row=4)  

database_text = StringVar()  
database_text.set("stocks")  

self.entry_database = Entry(frame, textvariable=database_text)  
self.entry_database.grid(row=4, column=1)  

self.label_empty = Label(frame, text='')  
self.label_empty.grid(row=5)   

self.label_twsfields = Label(frame, text='TWS fields:')  
self.label_twsfields.grid(row=6)  

self.label_server = Label(frame, text='Server:')  
self.label_server.grid(row=7)  

twsserver_text = StringVar()  
twsserver_text.set("127.0.0.1")  

self.entry_server = Entry(frame, textvariable=twsserver_text)  
self.entry_server.grid(row=7, column=1)  

self.label_empty = Label(frame, text='')  
self.label_empty.grid(row=8)   

self.label_twscontractinfo = Label(frame, text='TWS contract info:')  
self.label_twscontractinfo.grid(row=9)  

self.label_symbol = Label(frame, text='Symbol:')  
self.label_symbol.grid(row=10)  

self.entry_symbol = Entry(frame)  
self.entry_symbol.grid(row=10, column=1)  

self.label_barsize = Label(frame, text='Bar Size:')  
self.label_barsize.grid(row=11)  

self.barsize_selected = StringVar(frame)  
self.barsize_selected.set("1 min")  

self.optionmenu_barsize = OptionMenu(frame, self.barsize_selected, "30 secs", "1 min", "5 mins", "10 mins", "15 mins", "1 hour", "4 hours", "1 day")  
self.optionmenu_barsize.grid(row=11, column=1)  

self.label_duration = Label(frame, text='Duration:')  
self.label_duration.grid(row=12)  

self.duration_selected = StringVar(frame)  
self.duration_selected.set("1 W")  

self.optionmenu_duration = OptionMenu(frame, self.duration_selected, "1 H", "4 H", "1 D", "1 W", "1 M", "1 Y")  
self.optionmenu_duration.grid(row=12, column=1)  
  

self.label_empty = Label(frame, text='')  
self.label_empty.grid(row=13)      

self.button_download = Button(frame, text="Download", command=self.tws_connect)  
self.button_download.grid(row=14, column=1)  

self.button_import = Button(frame, text="Import", command=self.mysql_connect)  
self.button_import.grid(row=15, column=1)  

self.label_empty = Label(frame, text='')  
self.label_empty.grid(row=16)   

def say_hi(self):  
print "loading data..."  

def tws_connect(self):  
print "connecting to tws..."  
print "tws server: " + self.entry_server.get()  

self.new_symbolinput = string.split(self.entry_symbol.get(), ',')  

#print raw_symbol_input  
print self.new_symbolinput  

print self.j  

for i in self.new_symbolinput:  
  print i  
  qqq = Contract()  
  qqq.m_symbol = i  
  qqq.m_secType = 'STK'  
  qqq.m_exchange = 'SMART'  
  qqq.m_currency = 'USD'  
  endtime = strftime('%Y%m%d %H:%M:%S')  
  durationreq = '%s' % self.duration_selected.get()  
  barsizereq = '%s' % self.barsize_selected.get()  
  self.con.reqHistoricalData(0, qqq, '', durationreq, barsizereq, 'TRADES', 1, 2)  

def mysql_connect(self):   
#write newDataList to csv file  
csvfile = open('minutetrades2.csv','wb')  
for item in self.newDataList:  
  csvfile.write('%s \n' % item)  

csvfile.close()  

print "Printing dataList..."  
print self.newDataList  
print "connecting to mysql..."  
  
print "MySQL host: " + self.entry_host.get()  
print "MySQL user: " + self.entry_user.get()  
print "MySQL database: " + self.entry_database.get()  

self.contract_info()  

def contract_info(self):  
print "contract info..."  
print "Symbol: " + self.entry_symbol.get()  
print "Bar size: " + self.barsize_selected.get()  

def historical_data_handler(self, msg):  
print msg.date, msg.open, msg.high, msg.low, msg.close, msg.volume  
if ('finished' in str(msg.date)) == False:  
  new_symbol = self.new_symbolinput[self.j]
##      new_symbol = 'GBP.USD' ### rpline
  dataStr = '%s, %s, %s, %s, %s, %s, %s' % (new_symbol, strftime("%Y-%m-%d %H:%M:%S", localtime(int(msg.date))), msg.open, msg.high, msg.low, msg.close, msg.volume)  
  #prevent addition of 'finished...' statement to newDataList  
  self.newDataList.append(dataStr)  
else:  
  self.j = (self.j)+1  
  print self.j  

root = Tk()  
root.title('Historical Data: Download and Import')  
app = App(root)  

root.mainloop() 
"""
