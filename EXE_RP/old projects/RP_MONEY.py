# -*- coding: utf-8 -*-
import os, sys

##  1. gather all download files on all systems and rename with source and date and acctid
##  2.enter all transactions into a dbase with categories or quickbooks...
##  3. summarize all data by month and year and accounts and categories
##  4. create a spreadsheet to transfer creditcard pdf only data into trans format

## list of all sources
## CS, UBS, UBSccard, CSccard, SwissAirccardvisa, SwissAmex, ChaseRP, BOANP, IBKRU87392, IBUK194, IBUKFrpadv]
## list of all accounts
## UBS:    .   start spreadsheet

############################
blasym = ' €'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]

localtag = '_RNR'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
print EXEnoslash
import HVARs, rputiles
import glob, csv, subprocess, datetime, shutil, subprocess, time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
projectarea = EXE + 'PROJECT.SageFlash/'
config = projectarea + 'config_sage/'
nasarea =  rootpath 
SAGE_EXPORTS = TMP
outputarea = TMP
#######################################

##def grep_to_txtfile(infilename,greppattern,outfilename):

####grep_to_txtfile('Script1.py',greppattern,'dukwout.txt')

infilename = 'ALLCBOESYMBOLS.csv'
infilename = 'all cboe stock syms.csv'

lines =[]
newline = 'http://finance.yahoo.com/d/quotes.csv?s='
end = '&f=snd1t1l1ohgvwdyr'

prevhun = 0
hundred = int(0)
bla = ''
bigcount = 0
while hundred < 16:
        hundred += 1 
        c=0
        print hundred, prevhun
        print '====='
        lines =[]
        newline = 'http://finance.yahoo.com/d/quotes.csv?s='
        end = '&f=snd1t1l1ohgvwdyr'
        with open(infilename, 'r') as afile:
            lines = afile.readlines()
            for line in lines:
                    c +=1
                    sym = (line.strip()).split(',')[1]      
                    if c < hundred*100 and c > prevhun*100:
                            newline = newline + sym + '+'
##                            print sym
        fullline = newline + end
        webpage = fullline
##        response = urllib2.urlopen(fullline)
        bla += requests.get(fullline).content
        time.sleep(2)
##        print bla
##        html = response.readlines()
        prevhun = hundred
outfilename = 'cboestockswithprices.csv'
##rputiles.write_file_to_csvfile(outfilename, bla)
rputiles.write_file_array(outfilename,bla)   ### this one is for strings not arrays

