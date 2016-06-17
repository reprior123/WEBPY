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
import time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
outputarea = TMP
mthlyCBOEfiles = EXE + 'PROJECT.ChooseCBOEStocks/volume data files monthly cboe/'
#######################################
#############################################
## collect CBOE monthly file
## add price and tier information
## show outliers in volume vs tiers and create categories
## category list = callvolume, putvolume, volatility, price, OI, pricelevelSTOCK, STOCKvolume, STOCKBidAskSpread, DivYield, #spikeMoves
#########
##Collect a file
##http://www.cboe.com/Publish/TTMDAvgDailyVol/1404_rank_wosym.xlsx
##1404 represents the month...collect once per month and place in mthlyCBOEfiles
##read the file with 

fname = mthlyCBOEfiles + '1404_rank_wosym.xlsx'
newfname = fname.replace('.xlsx', '.csv') #### this bit put in to avoid a second time consuming conversion to csv
##rputiles.convertXLSXtoCSV(fname)
lines= rputiles.csvToLines(newfname)
count = 1
for line in lines:
        count +=1
        if count <10:
                print line[0]
                for f in line:
                        print f
                print len(line), 'linelen'
print len(lines)

##add tiering

tierfile = 


####### previous code below...
##
##
##infilename = 'ALLCBOESYMBOLS.csv'
##infilename = 'all cboe stock syms.csv'
##
##lines =[]
##newline = 'http://finance.yahoo.com/d/quotes.csv?s='
##end = '&f=snd1t1l1ohgvwdyr'
##
##prevhun = 0
##hundred = int(3)
##bla = ''
##bigcount = 0
##while hundred < 8:
##        hundred += 1 
##        c=0
##        print hundred, prevhun
##        print '====='
##        lines =[]
##        newline = 'http://finance.yahoo.com/d/quotes.csv?s='
##        end = '&f=snd1t1l1ohgvwdyr'
##        with open(infilename, 'r') as afile:
##            lines = afile.readlines()
##            for line in lines:
##                    c +=1
##                    sym = (line.strip()).split(',')[1]      
##                    if c < hundred*100 and c > prevhun*100:
##                            newline = newline + sym + '+'
####                            print sym
##        fullline = newline + end
##        webpage = fullline
####        response = urllib2.urlopen(fullline)
##        bla = requests.get(fullline).content
##        outfilename = 'cboestockswithprices.20140507.' + str(hundred) + '.csv'
##        rputiles.write_file_array(outfilename,bla)
##        time.sleep(3)
####        print bla
####        html = response.readlines()
##        prevhun = hundred
####outfilename = 'cboestockswithprices.20140507.csv'
####rputiles.write_file_to_csvfile(outfilename, bla)
####rputiles.write_file_array(outfilename,bla)   ### this one is for strings not arrays
##
