# -*- coding: utf-8 -*-
import os, sys, bs4
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
import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
outputarea = TMP
#######################################
fname = DATA + 'etfs.sorted.txt'

fnamefile=open(fname, 'r')
lines = fnamefile.readlines()
stocklist =[]
count = 1
for line in lines:
        count +=1
        if count < 3:
                stock = (line.split('|')[1]).upper()
                stocklist.append(stock)
##                for f in line.split('|'):
##                        print f
##                print len(line.split('|')), 'linelen'
print len(lines)

fnamefile.close()

baselink = 'https://www.cboe.com/DelayedQuote/QuoteTable.aspx?TICKER='
baselinkyahoo = 'http://finance.yahoo.com/q/os?s='
##ACWI
yahoopart2 = '&m='
month ='2014-06'

linkpart2 ='&ALL=2'

for stock in stocklist:
        fullline = baselink+stock+linkpart2
        fullline = baselinkyahoo + stock + yahoopart2 + month
        ###########################        response = urllib2.urlopen(fullline)
##        bla = requests.get(fullline).content
        print fullline
        outfilename = stock + '.openintyahoo.csv'
##        rputiles.write_file_array(outfilename,bla)
        newf = open(outfilename, 'r')
##        time.sleep(1)
        newbla = newf.read()
        from bs4 import BeautifulSoup
##        from urllib2 import urlopen
        soup = BeautifulSoup(newbla)
##        print soup
##        lines = (soup.prettify()).split()
##        for line in lines:
##                if 'yfnc_tabledata1' in line:
##                        print line
##        print(soup.get_text())
##        for link in soup.find_all('td'):
##            print(link.get('href'))
##                print link
##        print soup.b
        table = soup.findAll('table', attrs={ "class" : "yfnc_tabledata1"})
        print table
        newf.close()
##        print bla

        
##lines =[]
##new
