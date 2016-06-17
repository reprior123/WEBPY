import zipfile
from zipfile import ZipFile
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import uniq_module
############################
path = os.getcwd() + '/'
drivelet = path[0]+ ':/'
EXE = drivelet + 'EXE/'
DATA = drivelet + 'DATA/'
TMP = drivelet + 'TMP/'
print path
projarea = EXE + 'PROJECT.logfile_scanners/'
projdata = DATA + 'logfile_area/rawlogs/'
zipped_irs = projdata + 'zipped_irs'
unzipped_logs = projdata + 'unzipped_logs'
hitlift_lines = projarea + 'hitlift_lines'
just_trades = projarea + 'just_trades'
###############################
def extractzips():
    rawzips =  sorted(os.listdir(zipped_irs))
##    rawzips = ['AQTOR3.72.2.27_JoshJIR_130326150043.zip']
    for fname in rawzips:
        newname = zipped_irs + '/' + fname
        print fname
        if '.zip' in fname:
            zipTest = ZipFile(newname)
            zipTest.extractall(unzipped_logs)
#######################
mode = 'extract_yes'
mode = 'extract_no'
if mode == 'extract_yes':
    extractzips()
##########################################
def extract_hls():
    fileslist = os.listdir(unzipped_logs)
##    fileslist = ['AQTOR_20130328_1_130328150043.log']
    for filename in fileslist:
        if '.log' in filename:
            print filename 
            filenamefull = open(unzipped_logs + '/' + filename, 'r')
            linesarray =[]
            alllines = []
            hllines =[]
            linesarray = filenamefull.readlines()
            #################
            head = linesarray[:10]
            for lineh in head:
                if 'Node' in lineh:
                    print lineh
            dwords = ['Selected valuation underlying', 'Create HitLift', 'ProductHitLiftSetup', 'Parameter validation']
            dwords = ['Selecg', 'Creift', 'Prodetup', 'Paraion']
            for line in linesarray:
                if '[HL]' in str(line):
                    if  dwords[0] not in str(line):
                        if  dwords[1] not in str(line):
                            if  dwords[2] not in str(line):
                                if  dwords[3] not in str(line):
                                    hllines.append(line)
            fileout = open(hitlift_lines + '/' + filename +'.bla.txt', 'w')
            fileout.writelines(hllines)
            fileout.close()
            filenamefull.close()
            #####################  END ROUTINE  #######
##extract_hls()
#######################
###########
#############
def summarize_hits():        
    hlinesfiles  = os.listdir(hitlift_lines)
##    hlinesfiles = ['AQTOR_20130328_1_130328150043.log.bla.txt']
    ###########################################
    allsumlines =[]
    print 'logdate | #stocks  | # strikes  | firedorders |traded| '
    for hfile in hlinesfiles:
        firedordercount = tradedcount = 0
        
        filenamefull = open(hitlift_lines + '/' + hfile, 'r')
        linesout = []
        hllines =[]
        hl_keys =[]
        summarylines =[]
        singlekey = 'bb'
        hllinesarray = filenamefull.readlines()
            ################################
        for line in hllinesarray:
            logflag = 'bla'
            writeflag = 'no'
            if 'Create HitLift, Key' in line:
                singlekey = str(line.split()[1]) + '_' + str(line.split()[4])
    ##            print singlekey
    ##            print line
                hl_keys.append(singlekey)
    ##            print hl_keys
            if 'order fired' in str(line):
                if 'BBO update' in line:    ###new trigger levels
                    offset = 0
                    logflag = 'bbo_order'
                    writeflag = 'yes'
                elif  'HitLift enabled' in line:
                    offset = 0
                    logflag = 'enablefire_order'
                    writeflag = 'yes'
                else:
                    offset = 1
                    logflag = 'uupdate_order'
                    writeflag = 'yes'
            if writeflag == 'yes':
                firedordercount +=1
                time = line.split()[1]
                stkname = line.split()[4]
                side = line.split()[offset+10]
                date = line.split()[0]
                trigger = line.split()[8]
                qty = line.split()[offset+11]
                price = (line.split('@')[1]).split(',')[0]
                orderid = (line.split(',')[1]).replace(' ID:', '')
                bbo = line.split(',')[3]
                underprice = line.split(',')[4]
                s=' | '
                linesout.append(line)
                tradedflag = 'trade_no'
                for hline in hllinesarray:
                    if orderid in str(hline) and 'order traded' in hline:
    ##                    print hline
                        tradedcount += 1
                        tradedflag = 'trade_yes'
                        linesout.append(hline)
                        ###########
                newline =  date +s+ price +s+ bbo +s+ orderid +s+ stkname +s+ underprice +s+  side +s+  time +s+  trigger +s+ qty +s+ logflag + s+ tradedflag +s+'\n'
                summarylines.append(newline)
                ######################
        allsumlines += summarylines
        strikesnum = len(hl_keys)
    ##    print ' is number of strikes hl created', strikesnum
        newhls = uniq_module.uniq(hl_keys)
    ##    print newhls
        stocksnum = len(newhls)
    ##    print len(newhls), 'number of stocks same time hl created'
    ##    print 'fired orders', firedordercount
    ##    print 'traded', tradedcount
        ### this array needs to be uniqed and listed to check for dupes and restarts etc
        fileout = open(just_trades + '/' +hfile +'.hllines.txt', 'w')
        fileout.writelines(linesout)
        print hfile, stocksnum, strikesnum, firedordercount, tradedcount
        fileout.close()
        filenamefull.close()
        ##################
    ##    fileout = open(just_trades + '/' +hfile +'.summary.txt', 'w')
    ##    fileout.writelines(summarylines)
    ##    fileout.close()
    ##    filenamefull.close()
        ###########
    print 'logdate | #stocks  | # strikes  | firedorders |traded| '
    headerline = ['date|price|bbo|orderid|stk|ubbo|side|time|reason|qty|reason2']	##tradedornot

    fileout = open(just_trades + '/' + 'hltrades.allsummary.txt', 'w')
    fileout.writelines(headerline)
    fileout.writelines(allsumlines)
    fileout.close()
    filenamefull.close()
summarize_hits()
###  end of summarize routine   #####

def rename_a_log(logfilename):
    print logfilename
    nameNdir = unzipped_logs + '/' + logfilename
##    filenamefull = open(unzipped_logs + '/' + logfilename, 'r')
    os.system('head -200000 ' + nameNdir + ' > blahead.txt')
    os.system('tail  ' + nameNdir + ' >> blahead.txt')
    os.system('head -1  blahead.txt > head1')
    os.system('tail -1  blahead.txt >> head1')

    headerfile = open('head1', 'r')
    head_2lines = headerfile.readlines()
    filenamefull = open('blahead.txt', 'r')    
    head_huge = filenamefull.readlines()
    filenamefull.close()
    headerfile.close()
    #################
    lastline = head_2lines[1]
    lasttime = lastline.split()[1]
    firstline = head_2lines[0]
    firsttime = firstline.split()[1]
    macid = 'need'
    nodename = 'need'
    for lineh in head_huge:
        if '=Node' in lineh:
            nodename = (lineh.split()[5]).replace(',','')
        if 'License Machine ID' in lineh:
            macid = lineh.split()[8]
    newlogname = projdata + logfilename + '.' + macid + '.' + nodename + '.' + firsttime + '.' +lasttime + '.renamed.log'
    print newlogname
    os.system('cp ' + nameNdir + ' ' + newlogname)

######   end of rename routine  ####
##    rename triggered here!!!!
##fileslist = os.listdir(unzipped_logs)
####fileslist = ['AQTOR_20130328_1_130328150043.log']
##for filename in fileslist:
##    if '.log' in filename:
##        rename_a_log(filename)
##################################################









    
##130328 130653834 5D4 SysAct  HIMX    [HL] order fired (BBO update)
##Buy 40 HIMX.SEP13.6.C @ 0.6, ID:5ACC7F58, Level:40 0.6 0.75 40, BBO:0.55 0.6, UBBO:5.2 5.21, IIOTime:45
##130328 083001588 BE0 SysAct  IMOS    [HL] order fired (HitLift enabled)
##    Buy 2 IMOS.APR13.12:5.C @ 0.45, ID:299181C0, Level:20 0.45 0.75 20, BBO:0.5 0.45, UBBO:12.35 12.5, IIOTime:0
##130328 093610665 31C SysAct  YPF     [HL] order fired (underlying update (fast))
##    Sell 10 YPF.APR13.15.P @ 0.85, ID:451D63E0, Level:20 0.55 0.9 20, BBO:0.85 0.95, UBBO:14.59 14.6, IIOTime:0

##turnonflag = '[HL] Create HitLift for'
##createflag = 'creator=HL'
##enableflag = 'HitLift enabled,'
##for line in lines:
##    print line
##    if turnonflag not in line and createflag in line and 'OLT' in line:
##        print line

##                            newfile = string.replace(filen,'.zip','')
##                            age=time.time() -os.path.getctime(logfile_repos + '\\' + filen)            
##                            try:
##                                if age<24 * 60 * 60  :
##                                    print 'Filename:'+ logfile_repos + '\\' + name + '\\' + newfile
##                                    print "created: %s" % time.ctime(os.path.getctime(logfile_repos + '\\' + name + '\\' + newfile + '.zip'))
##                                    outfile = open(logfile_repos + '\\' + name + '\\' + newfile + '_' + 'targetlogfileoutfile.log.txt', 'w')
##                                    file = zipfile.ZipFile(logfile_repos + '\\' + name + '\\' +  newfile + '.zip', "r")
##                                    # list filenames
##orders = []
##for line in lines:
##    if turnonflag not in line and enableflag in line:
##        bla =  (line.split()[8]).replace(']:', '')
##        orders.append(bla)
##
##for order in orders:
##    for line in lines:
##        if order in str(line):
##            print line

#130128 101054554 F08 SysAct  SR      [HL] fired order [2F2D7D30]: Buy 1 SR.FEB13.0:9.P @ 0.65, HitLift enabled,
####        levels: 1 0.65 0.75 1, BBO: 0.19 0.22, UBBO: 0.771 0.774, IIO time: 0.
##count  = 0
##orders = []
##for line in lines:
##    if turnonflag not in line and '[HL] fired order' in line and  enableflag not in line and 'underlying update' in line:
##        bla =  (line.split()[8]).replace(']:', '')
##        count += 1
##        orders.append(bla)
##print count
##for order in orders:
##    for line in lines:
##        if order in str(line):
##            print line
##print count            
###################
##count  = 0
##orders = []
##for line in lines:
##    if turnonflag not in line and '[HL] fired order' in line and  enableflag not in line and 'BBO update' in line:
##        bla =  (line.split()[8]).replace(']:', '')
##        count += 1
##        orders.append(bla)
##print count
##for order in orders:
##    for line in lines:
##        if order in str(line) and 'fired' in line:
##            print line
##print count            
##############################
##count  = 0
##orders = []
##for line in lines:
##    if turnonflag not in line and '[HL]' in line and  enableflag not in line and 'traded:on' in line:
##        bla =  (line.split()[8]).replace(']:', '')
##        count += 1
##        orders.append(bla)
##print count
##for order in orders:
##    for line in lines:
##        if order in str(line):
##            print line
##print count            
