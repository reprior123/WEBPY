import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
############################

blasym = ' €'
localtag = '_RNR'
##################2##############
path = os.getcwd() + '/'
blapath = path.replace('EXE','|')
print blapath.split('|')[1]
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import HVARs ,rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
##########################################
acctfile = 'C:/users/bob/Google Drive/EXE_RNR/20140526.sf.Accounts.csv'
acctfile = 'C:/users/bob/Google Drive/EXE_RNR/20140526.sf.Assets.csv'
lines = rputiles.CsvToLines(acctfile)
co=0
for line in lines:
    if '00120000000AxdYAAS' in line:
        co+=1
        if co < 3:
            print co         
            c = 0
            clen = len(line)
            while c < clen:
                print line[c]
                c+=1
##    print line

##    
##
##def grep_to_txtfile(infilename,greppattern,outfilename):
##    try:
##        outfile = open(outfilename, 'w')
##        lines =[]
##        with open(infilename, 'r') as afile:
##            lines = afile.readlines()
##            for line in lines:
##                if greppattern in str(line):
##                    print line.strip('d')
##                    outfile.write(str(line))
##            outfile.write('\n')
##            outfile.close()
##    except:
##        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
##########################################
##greppattern = 'def'
##grep_to_txtfile('rputiles.py',greppattern,'dukwout.txt')
