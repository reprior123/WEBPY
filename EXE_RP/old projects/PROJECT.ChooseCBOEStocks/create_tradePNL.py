# -*- coding: utf-8 -*-
import os, sys
############################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_RNR'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
########################
import HVARs, rputiles, rputilesPIV
import glob, csv, subprocess, datetime, shutil, subprocess
##import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
GSarea = DATA + 'GS/'
downloads = 'C:\Users\bob\downloads'      
###########################################
outputarea = TMP
fname = DATA + 'etfs.sorted.txt'
custnum = 'C132482'
todaydate = '20140625'
#######################################

for f in (glob.glob(downloads + 'GBLACTIVITY' + todaydate + '*.csv')):
        print f
        print 'this file needs to automv to GS'
        
for f in (glob.glob(GSarea + 'GBLACTIVITY' + todaydate + '*.csv')):
        tradefile = f
for f in (glob.glob(GSarea + 'GBLPOSITIONAT' + todaydate + '*.csv')):
        GSposfile = f
time = ''
##tradefile = DATA + 'GS/' + 'GBLACTIVITY' + todaydate +  '194445' +custnum +'.csv'
##GSposfile = DATA + 'GS/' +'GBLPOSITIONAT' +  todaydate + '181948' +custnum +'.csv'
##GBLPOSITIONAT20140625181948C132482
tradelist = rputiles.CsvToLines(tradefile)

##todays trades
##today SOD position = yesterday EOD
##today EOD position
##mark all positions of SOD today to nightly close prices = position pnl
##tradelist.today is marked against today.EOD prices = tradepnl
##
##create a dictionary of closing prices
##one for tradepnl and one for positionpnl
##check if SOD == EOD position
g =[]
bla =[]
alllines = [['sym','pnl','trdp','clp','qty','bysell','usym','tdate','spareflag']]

for line in rputiles.CsvToLines(GSposfile):
        if 'Trade' not in line[1]:
                g.append(line[1])
datelist = rputiles.uniqArray(g)

for tradingdate in datelist:
##        print tradingdate
        for line in rputiles.CsvToLines(GSposfile):
                if line[1] == tradingdate:
                        g.append(line)
        rputiles.WriteArrayToCsvfile('tmpdict.csv',g)
        todayTradeEODprices = rputiles.create_dict(path  +'tmpdict.csv',2,4)
        ##############################################
        for trade in tradelist:       
                buysell = trade[1]
                mult = 1
                symraw = trade[2]
                usym = (symraw[0:4]).replace(' ' ,'')
                symbol = symraw.replace(' ','.')
                tradedate = trade[3]
                
                if len(symraw) > 4:
                        mult = 100        
                if tradedate == tradingdate:
##                        print tradedate
                        try:
                                tradeprice = float(trade[8])
                                GScloseprice = float(todayTradeEODprices[symraw])
                                tradeqty = float(trade[6])
                        except:
                                tradeprice = GScloseprice =  tradeqty = 1.0
                                print trade
                                print 'could not process the above'
                        blotter =trade[7]
                        pnl = (tradeprice - GScloseprice)*tradeqty*mult*(-1)                   
        ##                print symbol, pnl, str(tradeprice), str(GScloseprice), str(tradeqty), buysell, usym
                        bla.append(symbol)
                        bla.append(pnl)
                        bla.append(str(tradeprice))
                        bla.append(str(GScloseprice))
                        bla.append(str(tradeqty))
                        bla.append(buysell)
                        bla.append(usym)
                        bla.append(tradedate)
                        bla.append('spareflag')
                        alllines.append(bla)
                        bla =[]
##print alllines
print 'go check ' + path + 'pnl.csv'
rputiles.WriteArrayToCsvfile(path + 'pnl.csv',alllines)

##########   Run all DETAILS first at both BASE and CHF CURRENCY    ########
##alllines = [['sym','pnl','trdp','clp','qty','bysell','usym','tdate']]
fname = path + 'pnl.csv'
patternINheader = 'clp'
sumcatH = 'usym'
fheader1 = 'spareflag'
fpattern1 = 'spareflag'
fheader2 = fheader1
fpattern2 = fpattern1
sumcat1 = 'tdate'    
sumcat2 = sumcat1
fheader3 = fheader2
fpattern3 = fpattern2
sumvalue ='pnl'
##        ##########################################
finalpiv = rputilesPIV.pivotloop(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader)
##for line in finalpiv:
##        print line
##############################################
######### POSITION PNL  ##########
#####################################
##load pos file as EOD today
##load pos file yesterday as SOD
##yestSOD=todayEOD
##yestEOD=prevSOD
##20140624EODpos
##20140625EODpos
##graph 25prices to 24file and compute for 24
##yest
##today
##compute for yest
filedate = '20140626'

print datelist
for prevdate in datelist:
        gspredate = prevdate
        gsdate =
date = '20140625'
prevdate = '20140605'
gsdate = date[4:6] + '/' +  date[6:8]  + '/' + date[0:4]
gsprevdate = prevdate[4:6] + '/' +  prevdate[6:8]  + '/' + prevdate[0:4]
print gsdate
######################################################
for f in (glob.glob(GSarea + 'GBLPOSITIONAT' + filedate + '*.csv')):
        todayposfile = f
poslist =     rputiles.CsvToLines(todayposfile)
bposlist =    rputiles.CsvToLines(todayposfile)
#####################################################
##grep prevdates from todayposfile
todaypos =[]
for p in bposlist:
        if p[1] == gsdate:
                todaypos.append(p)
rputiles.WriteArrayToCsvfile('todayposprices.csv',todaypos)
todayEODprices = rputiles.create_dict('todayposprices.csv',2,4)
##############################################
##Account Number	3FF61209
##Trade Date	06/17/2014
##Symbol/Description	CCJ
##Quantity	0
##Base Currency Market Price	19.64
##Base Currency Market Value	0
##Base Currency OTE	0
##Base Currency Daily Total Net P&L	0
##Base Currency MTD Total Net P&L	0.62
##Base Currency YTD Total Net P&L	0.62

alllines = []
bla =[]
alllines = [['sym','pnl','trdp','clp','qty','bysell','usym','tdate','spareflag']]
for pos in poslist:
        longshort = pos[0]
        mult = 1
        symraw = pos[2]
        usym = (symraw[0:4]).replace(' ' ,'')
        symbol = symraw.replace(' ','.')
        posdate = pos[1]
##        print posdate, gsprevdate
        if len(symraw) > 4:
                mult = 100        
        if posdate == gsprevdate:
##                        print tradedate
                try:
                        markprice = float(pos[4])
                        prevmarkprice = float(todayEODprices[symraw])
                        GScashpnl = 1.0#float(pos[4])
                        posqty = float(pos[3])
                except:
                        markprice = prevmarkprice =  posqty = 1.0
                        print pos
                        print 'could not process the above'
                blotter =pos[7]
                pnl = (markprice - prevmarkprice)*posqty*mult*(-1)                   
##                print symbol, pnl, str(tradeprice), str(GScloseprice), str(tradeqty), buysell, usym
                bla.append(symbol)
                bla.append(pnl)
                bla.append(str(markprice))
                bla.append(str(prevmarkprice))
                bla.append(str(posqty))
                bla.append(longshort)
                bla.append(usym)
                bla.append(posdate)
                bla.append('spareflag')
                alllines.append(bla)
                bla =[]

##print alllines
print 'go check ' + path + 'pospnl.csv'
rputiles.WriteArrayToCsvfile(path + 'pospnl.csv',alllines)

##########   Run all DETAILS first at both BASE and CHF CURRENCY    ########
##alllines = [['sym','pnl','trdp','clp','qty','bysell','usym','tdate']]
fname = path + 'pospnl.csv'
patternINheader = 'clp'
sumcatH = 'usym'
fheader1 = 'spareflag'
fpattern1 = 'spareflag'
fheader2 = fheader1
fpattern2 = fpattern1
sumcat1 = 'tdate'    
sumcat2 = sumcat1
fheader3 = fheader2
fpattern3 = fpattern2
sumvalue ='pnl'
##        ##########################################
finalpiv = rputilesPIV.pivotloop(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader)
##for line in finalpiv:

        ############################
##                print trade
##        closeprice = todayTradeEODprices[symbol]
##        closeprice = trade[8]
##        symbol = stk +'.' + expiry + '.' + strike + '.' + cp 
##volumereport = DATA +'volume_report-complete-2014-06-06.csv'
##fnamefile=open(volumereport, 'r')
##fnamefile=open(fname, 'r')
##lines = fnamefile.readlines()
##stocklist =[]
##count = 1
##for line in lines:
##        count +=1
##        if count < 3:
##                stock = (line.split('|')[1]).upper()
##                stocklist.append(stock)
####                for f in line.split('|'):
####                        print f
####                print len(line.split('|')), 'linelen'
##print len(lines)
##
##fnamefile.close()
##
##baselink = 'https://www.cboe.com/DelayedQuote/QuoteTable.aspx?TICKER='
##baselinkyahoo = 'http://finance.yahoo.com/q/os?s='
####ACWI
##yahoopart2 = '&m='
##month ='2014-06'
##
##linkpart2 ='&ALL=2'
##
##for stock in stocklist:
##        fullline = baselink+stock+linkpart2
##        fullline = baselinkyahoo + stock + yahoopart2 + month
##        ###########################        response = urllib2.urlopen(fullline)
####        bla = requests.get(fullline).content
##        print fullline
##        outfilename = stock + '.openintyahoo.csv'
####        rputiles.write_file_array(outfilename,bla)
##        newf = open(outfilename, 'r')
####        time.sleep(1)
##        newbla = newf.read()
##        from bs4 import BeautifulSoup
####        from urllib2 import urlopen
##        soup = BeautifulSoup(newbla)
####        print soup
####        lines = (soup.prettify()).split()
####        for line in lines:
####                if 'yfnc_tabledata1' in line:
####                        print line
####        print(soup.get_text())
####        for link in soup.find_all('td'):
####            print(link.get('href'))
####                print link
####        print soup.b
##        table = soup.findAll('table', attrs={ "class" : "yfnc_tabledata1"})
##        print table
##        newf.close()
####        print bla
##
##        
####lines =[]
####new
