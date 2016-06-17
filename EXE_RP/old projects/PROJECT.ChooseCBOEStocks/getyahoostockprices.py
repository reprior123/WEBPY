# -*- coding: utf-8 -*-
import os, sys
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
invoice_proj_area =  EXE + 'PROJECT.INVOICING/'
invoice_output_area_noslash = DATA + 'invoice_runs_raw'
logoarea = invoice_proj_area + 'logoFiles/'
invoice_output_area = invoice_output_area_noslash + '/'
bconfig = invoice_proj_area + 'billing_config_files/'
sagearea = EXE + 'PROJECT.SageFlash/'
sageconfig = sagearea   + 'config_sage/'
sfarea = DATA + 'SFDATA/'
SFDATA = sfarea
SAGE_EXPORTS = rootpath + 'SAGE_EXPORTS/'
##def grep_to_txtfile(infilename,greppattern,outfilename):
##    try:
##        outfile = open(outfilename, 'w')
##        lines =[]
##        with open(infilename, 'r') as afile:
##            lines = afile.readlines()
##            for line in lines:
##                if greppattern in line:
##                    print 'MATCH'
##                    outfile.write(str(line))
##            outfile.write('\n')
##            outfile.close()
##    except:
##        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
##        pass
##    print 'outfile is in ...', outfilename
####greppattern = 'output'
####grep_to_txtfile('Script1.py',greppattern,'dukwout.txt')

infilename = 'ALLCBOESYMBOLS.csv'
infilename = 'all cboe stock syms.csv'

lines =[]
newline = 'http://finance.yahoo.com/d/quotes.csv?s='
end = '&f=snd1t1l1ohgvwdyr'

prevhun = 0
hundred = int(3)
bla = ''
bigcount = 0
while hundred < 8:
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
        bla = requests.get(fullline).content
        outfilename = 'cboestockswithprices.20140507.' + str(hundred) + '.csv'
        rputiles.write_file_array(outfilename,bla)
        time.sleep(3)
##        print bla
##        html = response.readlines()
        prevhun = hundred
##outfilename = 'cboestockswithprices.20140507.csv'
##rputiles.write_file_to_csvfile(outfilename, bla)
##rputiles.write_file_array(outfilename,bla)   ### this one is for strings not arrays

