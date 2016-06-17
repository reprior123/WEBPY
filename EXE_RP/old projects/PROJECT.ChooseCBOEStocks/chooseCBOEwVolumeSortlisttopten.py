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
import HVARs, rputiles
import glob, csv, subprocess, datetime, shutil, subprocess
##import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
outputarea = TMP
#######################################
fname = DATA + 'etfs.sorted.txt'
##Tier	Ticker	CBOE%	PHLX%	9DAYVOLUME	AVGCBOEVOLUME	AVGPHLXVOLUME	9 DAY AVG VOLUME	MIN VOLUME	MAX VOLUME	05/23/2014	05/27/2014	05/28/2014	05/29/2014	05/30/2014	06/02/2014	06/03/2014	06/04/2014	06/05/2014	FIRST 6 DAY AVG	 LAST 3 DAY AVG	 % CHG
##A	AA	18.8	15.5	142014	        2972	        2441	15779	9530	26357	13982	12833	15847	9530	12451	14859	14710	21445	26357	13250	20837	57.3
##
choosearea = DATA + 'ChoosingStocksIssues/'
rptarea = choosearea  +  'sumo volume reports/'
tiers = rputiles.create_dict(choosearea +'symbolsWtiers.csv', 0,1)
htbs = rputiles.create_dict(choosearea +'namesWHTB.csv', 0,1)
sectors = rputiles.create_dict(choosearea +'symbolsWsectors.csv', 0,3)
pricelist = rputiles.create_dict(choosearea +'symbolsWprices.csv', 0,1)

##need a dictionary for:
##        ETFs
##        index stocks
##        dividend yields
##        deal flag
##        open interest
##        number of strikes
##        weeklies yes or no
##        pennies yes or no

sumodate = '2014-06-20'

volumereport = rptarea +'volume_report-complete-' + sumodate + '.csv'

## new lists based on latest volume rport
tiers = rputiles.create_dict(volumereport, 1,0)

##fnamefile=open(volumereport, 'r')
lines = rputiles.CsvToLines(volumereport)
stocklist =[]
count = 1
pricebin = 'no'

## total volumes and avg tier volumes and categorize and create_dicts
tierlist = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
tierlist = ['C']
count = totalvol =0
tieravgs = []
for tierq in tierlist:
        print tierq
        for line in lines:
                aline =[]
                tier = 'bla'
                tier = line[0]
        ##        print line
                symbol = line[1]
                cboeperc = line[2]
                cboevol = line[5]
                if tierq == tier:
                        count +=1
                        totalvol += float(cboevol)
                        avgtiervol = totalvol/count
        string = tierq + ',' + str(avgtiervol)
        aline.append(tierq)
        aline.append(avgtiervol)
        aline.append(totalvol)
        
        tieravgs.append(aline)
print tieravgs
rputiles.WriteArrayToCsvfile('tieravgs.csv', tieravgs)
tiervol_dict = rputiles.create_dict('tieravgs.csv', 0,1)
tiertotvol_dict = rputiles.create_dict('tieravgs.csv', 0,2)
        
for line in lines:
        tier = 'C'
##        print line
        symbol = line[1]
        cboeperc = line[2]
        try:
                cboevol = float(line[5])
        except:
                cboevol = 1.0
        cboeavg = tiervol_dict[tier]
        try:
                tier = tiers[symbol]
        except:
                tier = 'needtier'
        try:
                htb = htbs[symbol]
        except:
                htb = 'needhtb'
        try:
                sector = sectors[symbol]
        except:
                sector = 'needsect'
        try:
                price = float(pricelist[symbol])
        except:
                price = 'needprice'
        if price > 5 and price < 60 :
                pricebin = 'medium'
        try:        
                cboeavg = tiervol_dict[tier]
        except:
                cboeavg = float(50)
        try:        
                cboetiertot = float(tiertotvol_dict[tier])
        except:
                cboetiertot = float(50)
                
        perc = float(cboevol / cboetiertot)
        if tier == 'G' and pricebin == 'medium':
                if  cboevol > (1.0*float(cboeavg)) and perc > float(0.02): 
                        count +=1
                        print symbol, tier, price,htb, sector, cboeperc, cboevol, cboeavg
        tier = 'bla'
                                                               
print count, 'is number of hits' 
##        print line
##        symbol = line[1]
##        cboeperc = line[2]
##        cboevol = line[5]
##        try:
##                tier = tiers[symbol]
##        except:
##                tier = 'needtier'
##        try:
##                htb = htbs[symbol]
##        except:
##                htb = 'needhtb'
##        try:
##                sector = sectors[symbol]
##        except:
##                sector = 'needsect'
##        try:
##                price = float(pricelist[symbol])
##        except:
##                price = 'needprice'
##        if price >20 and price <60:
##                pricebin = 'medium'
##        if tier == 'A' and pricebin == 'medium'  and cboevol > avgtiervol:
##
##                print symbol, tier, price,htb, sector, cboeperc, cboevol       
##create_dict('symbolsWtiers.csv', 0,1)
##create_dict('symbolsWtiers.csv', 0,1)
##create_dict('symbolsWtiers.csv', 0,1)
##Tier	A	A
##Ticker	AA	AAPL
##CBOE%	20	23.1
##PHLX%	15.5	12.6
##9 DAY VOLUME	244281	9092279
##AVG CBOE VOLUME	5430	233820
##AVG PHLX VOLUME	4212	127187
##9 DAY AVG VOLUME	27142	1010253
##MIN VOLUME	14558	586115
##MAX VOLUME	52047	1401860
##06/09/2014	31688	1380319
##06/10/2014	20023	1401860
##06/11/2014	14558	1056269
##06/12/2014	20030	1360995
##06/13/2014	52047	1395003
##06/16/2014	15245	673854
##06/17/2014	18339	594597
##06/18/2014	41141	586115
##06/19/2014	31210	643267
##FIRST 6 DAY AVG	25599	1211383
## LAST 3 DAY AVG	30230	607993
## % CHG	18.1	-49.8

##
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
