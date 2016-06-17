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
tiers = rputiles.create_dict(DATA +'symbolsWtiers.csv', 0,1)
htbs = rputiles.create_dict(DATA +'namesWHTB.csv', 0,1)
sectors = rputiles.create_dict(DATA +'symbolsWsectors.csv', 0,3)
pricelist = rputiles.create_dict(DATA +'symbolsWprices.csv', 0,1)

volumereport = DATA +'volume_report-complete-2014-06-06.csv'

##fnamefile=open(volumereport, 'r')
lines = rputiles.CsvToLines(volumereport)
stocklist =[]
count = 1
for line in lines:
        tier = 'bla'
##        print line
        symbol = line[1]
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
                price = pricelist[symbol]
        except:
                price = 'needprice'
        print symbol, tier, price,htb, sector
        
##create_dict('symbolsWtiers.csv', 0,1)
##create_dict('symbolsWtiers.csv', 0,1)
##create_dict('symbolsWtiers.csv', 0,1)

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
