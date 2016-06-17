import zipfile
from zipfile import ZipFile
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
import uniq_module
############################
path = os.getcwd() + '/'
drivelet = path[0]+ ':/'
EXE = drivelet + 'EXE_RNR/'
DATA = drivelet + 'DATA_RNR/'
TMP = drivelet + 'TMP_RNR/'
print path
projarea = EXE + 'PROJECT.logfile_scanners/'
projdata = DATA + 'logfile_area/rawlogs/'
zipped_irs = projdata + 'zipped_irs'
processed_zips = projdata + 'alreadydonezips'
unzipped_logs = projdata + 'unzipped_logs'
unzip_renamed = projdata + 'unzip_renamed_logs'
hitlift_lines = projarea + 'hitlift_lines'
just_trades = projarea + 'just_trades'
###############################
def extractzips():
    rawzips =  sorted(os.listdir(zipped_irs))
    print rawzips
##    rawzips = ['AQTOR3.72.2.27_JoshJIR_130326150043.zip']
    for fname in rawzips:
        newname = zipped_irs + '/' + fname
        print fname
        print newname
        if '.zip' in fname:
##            zipTest = ZipFile(newname)
            with ZipFile(newname, 'r') as zipTest:
                zipTest.extractall(unzipped_logs)
                time.sleep(1)
    ##            ZipFile.close()
    ##            fh = open(newname, 'rb')
    ##            z = zipfile.ZipFile(fh)
    ##            for name in z.namelist():
    ##                print name
    ##                if '.log' in name:
    ##                    data = z.read(name)
    ##                    outfile = open(unzipped_logs + name, 'wb')
    ##                    outfile.write('fffff')
    ##                    outfile.close()
    ##                fh.close()
                shutil.copy(newname, processed_zips)
### end extractzips  ####
##########################################
def extract_hls(logs_dir):
    logslist = os.listdir(logs_dir)
    logslist = ['AQTOR_20130403_1_130403162610.log.DS7TJQBA3CMOG.CBOE-AQ-SE-233.091607823.162613993.renamed.log']
    for filename in logslist:
        if 'renamed.log' in filename:
            print filename 
            filenamefull = open(targetdir + '/' + filename, 'r')
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
            fileout = open(hitlift_lines + '/' + filename +'.hllines.txt', 'w')
            fileout.writelines(hllines)
            fileout.close()
            filenamefull.close()
#####################  END  extract_hls ROUTINE  #######
#############
def summarize_hits():
##    AQTOR_20130227_1_130227120326.log.P3BBERYOCAMOG.TOROCBOE07.071823991.120332619.renamed.log
    hlinesfiles  = os.listdir(hitlift_lines)   ####change this to the new renamed files area when ready
##    hlinesfiles = ['AQTOR_20130328_1_130328150043.log.bla.txt']
    ###########################################
    allsumlines =[]
    print 'logdate | #stocks  | # strikes  | firedorders |traded| '
    for hfile in hlinesfiles:
        if '.txt' in str(hfile):
            firedordercount = tradedcount = 0
            print hfile
            nacid = 'bla'
            macid = hfile.split('.')[2]
            print macid      
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
                    s='  '
                    linesout.append(line)
                    tradedflag = 'trade_no'
                    for hline in hllinesarray:
                        if orderid in str(hline) and 'order traded' in hline:
        ##                    print hline
                            tradedcount += 1
                            tradedflag = 'trade_yes'
                            linesout.append(hline)
                            ###########
                    newline =  '\n' +macid + s+ date +s+ price +s+ bbo +s+ orderid +s+ stkname +s+ underprice +s+  side +s+  time +s+  trigger +s+ qty +s+ logflag + s+ tradedflag +s
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
        print 'macid | logdate | #stocks  | # strikes  | firedorders |traded| '
        headerline = ['macid user date price bbo bboask orderid stk ubbo ubboask side time reason qty reason2 tradedornot']	##tradedornot

        fileout = open(just_trades + '/' + 'hltrades.allsummary.txt', 'w')
        fileout.writelines(headerline)
        fileout.writelines(allsumlines)
        fileout.close()
        filenamefull.close()
###  end of summarize routine   #####
########################################    
def rename_a_log(targetdir):
    fileslist = os.listdir(targetdir)
##    fileslist = ['AQTOR_20130328_1_130328150043.log']
##    AQTOR_20130326_1_130326150052.log
    for logfilename in fileslist:
        if '.log' in logfilename:
            print logfilename
            nameNdir = targetdir + '/' + logfilename
        ##    filenamefull = open(unzipped_logs + '/' + logfilename, 'r')
            os.system('head -300000 ' + nameNdir + ' > blahead.txt')
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
            newlogname = unzip_renamed + '/' + logfilename + '.' + macid + '.' + nodename + '.' + firsttime + '.' +lasttime + '.renamed.log'
            print newlogname
##            os.system('cp ' + nameNdir + ' ' + newlogname)
            shutil.move(nameNdir, newlogname)
######   end of rename routine  ####

def extract_hlsnew(logs_dir):
    logslist = os.listdir(logs_dir)
##    logslist = ['AQTOR_20130403_1_130403162610.log.DS7TJQBA3CMOG.CBOE-AQ-SE-233.091607823.162613993.renamed.log']
##    logslist = ['AQTOR_20130418_1_130418103155.log.DS7TZZJF3BMOG.CBOE-AQ-SE-225.090226539.103215469.renamed.log']
    for filename in logslist:
        if 'renamed.log' in filename:
            print filename 
##            filenamefull = open(logs_dir + '/' + filename, 'r')
            os.system('grep HL ' + logs_dir + '/' + filename + ' > temphl')
            print 'done with grep'
            filenamefull = open('temphl', 'r')
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
            fileout = open(hitlift_lines + '/' + filename +'.hllines.txt', 'w')
            fileout.writelines(hllines)
            fileout.close()
            filenamefull.close()
###########
##   trigger routines here #####
#######################
##extractzips()
##rename_a_log(unzipped_logs)
##extract_hls(unzip_renamed)
##extract_hlsnew(unzip_renamed)
summarize_hits()
##################################################

##Still to do:
##
##determin time of file and decide whether to unzip etc.
##     age=time.time() -os.path.getctime(logfile_repos + '\\' + filen)            
####                            try:
####                                if age<24 * 60 * 60  :
##
##
##extract ordernumber from fireds to try and pair fills and misses with fires to dtermine whihc stocks got filled more than others
##rembembre to use enable flag as a possible trigger....

         
