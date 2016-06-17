import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
############################
path = os.getcwd() + '/'
drivelet = path[0]+ ':/'
EXE = drivelet + 'EXE/'
DATA = drivelet + 'DATA/'
TMP = drivelet + 'TMP/'
test = path + 'test/'
SageOut = path + 'SageOut/'
config = path + 'billing_config_files/'
gdrive = 'C:/Documents and Settings/rob.prior/My Documents/Google Drive/Allopts'
SageOut = gdrive
print path
##########
sfarea = DATA + 'SFDATA/'
os.system(EXE + 'today.in.unix.py ' )
todayunix = (((open(TMP + 'today.txt', 'r')).read()).split())[1]
(open(TMP + 'today.txt', 'r')).close()
print 'today is ...', todayunix
dateloop = [todayunix]
##dateloop = ['20120930', '20120904']
##dateloop = ['20130322']
ownername = 'need'
############################
######  dates set here   #############################
from datetime import timedelta
from datetime import datetime
import datetime
#################################
def csvToLines(afile):
    csvr = csv.reader( afile )
    lines = []
    for row in csvr:
        lines.append( row )
    afile.close()
    return lines
#####################################
fname = SageOut  +  todayunix + '.ALLopps.tsv'
print fname
outfile = open(fname, 'w')
for filedate in dateloop:
    month = filedate[0:6]
    sfmonth = sfarea + month + '/'
    sfdata = sfmonth + filedate + '/' + filedate + '.sf.'
    print filedate
    usersfile = open(sfdata + 'Users.csv', 'r')
    oppfile = open(sfdata + 'Opportunities.csv', 'r')
###############################################
    opplines = csvToLines (oppfile)
    userlines = csvToLines (usersfile)
    opplinescount = str(len(opplines))
    print ' this is opplines all'
    print str(opplinescount)
    counto = 0
    lines = []
    for line in opplines:
        counto += 1
        #cehck for 'Dead' as well
        if 'Lost' not in line[6] and ('2012'in str(line) or '2013' in str(line)):
            #print str(line).replace(',', '\n')
            lines.append( line )            
    totalines = str(len(lines))
    print totalines, 'made it through to next level'
    countl = 1
    #################################
    total = rate = totalClasses = assetclasses = totalProdAssets = 0
    billinglines = 'close date \t close month \t yearly amount \t\
    CURRENCY\topportunity name\tstage \tdate billable\t billable month\tOne\
    -off amount\tmthly amount (CHF)\ttrial v live \t duration \t owner \tpercent\tprob amt\tsegment\treportdate\n'
    for aline in lines:
        countl += 1
        oppID = aline[0]
        billable = aline[52]
##        print billable
        if billable == '':
            billable = '2013-09-01'
        acctid = aline[2]
        oppname = aline[4]
        ownerIDC = aline[21]
        percfield = aline[8]
        amtCHFnew = aline[7]
        for oline in userlines:
            if ownerIDC == str(oline[0]):
                ownername = oline[2]
        stage = aline[6]
        if countl > 2 and  percfield != '' and ' ' not in percfield :
            prob_percent = float(percfield)
        else:
            prob_percent = float(0.0)
        if countl > 2 and  amtCHFnew != '' and ' ' not in amtCHFnew :
            amountC = float(amtCHFnew)
        else:
            amountC = 0.0
        closedate = aline[11]
        lastmoddate = aline[24]
        lastmodid = aline[27]
        exchange = aline[33]
        oppcurr = aline[18]
        if oppcurr == 'EUR':
            crate = 1.2
        elif oppcurr == 'USD':
            crate = .9
        else:
            crate = 1
        date_format = "%d-%m-%Y"
        from datetime import timedelta
        from datetime import datetime
        startcheckdate = '20120601'
        date_format = "%Y%m%d"
        mformat = "%Y%m"
        sfdate_format = "%Y-%m-%d"
        sdate = datetime.strptime(startcheckdate, date_format)
        fullformat = "%Y-%m-%dT%H:%M:%S.000Z"
        #2012-02-10T17:28:25.000Z
        if 'LASTMOD' in lastmoddate:
            lastmod = datetime.strptime(startcheckdate, date_format)
        else:                        
            lastmod = datetime.strptime(lastmoddate, fullformat)      
        lastmodstr = lastmod.strftime(date_format)
##        cycleend = (pstart + timedelta(days=80)).strftime(date_format)
        #delta = pendpartial - pstart
        #partialmth = ('%3.1f' %((delta.days / 30)))
        if '20' in closedate:
            closedatedate = (datetime.strptime(closedate, sfdate_format))
        else:
            closedatedate = (datetime.strptime('2015-01-01', sfdate_format))         
        closemonth = closedatedate.strftime(mformat)
        if '201' in billable and len(billable) < 14 :
            billdatedate = (datetime.strptime(billable, sfdate_format))
        else:
            billdatedate = (datetime.strptime('2015-01-01', sfdate_format))
        billdatedate = closedatedate + timedelta(days=45)
        billmonth = billdatedate.strftime(mformat)
        #count = count + 1    
        oneoff = ' '
        mthlyCHF = (float(amountC) / 12 ) * crate
        trialvslive = 'need'
        duration = 'need'
        segment = 'Quote'
        if 'AE' in oppname or 'AX' in oppname:
            segment = 'ExStream'
            
        prob_amt = prob_percent * mthlyCHF *.01
        if closedatedate > sdate:
            format = "%-11s \t%-20s\t %-8s\t %-8s\t %6s\t %5s \t%-20s\t %-8s\t %-8s\t %6s\t %5s \t %s\t%s\t%s\t%s\t%s\t%s\n"
            billingline = (format % (closedate, closemonth, amountC, oppcurr, oppname, stage, billable, billmonth,\
                                     oneoff, str(mthlyCHF), trialvslive, duration, ownername, prob_percent, prob_amt, segment, filedate ))
            billinglines = billinglines + billingline
##    print billinglines
##    print 'done..here is last line...'
##    print billingline

    outfile = open(fname, 'a')
    outfile.write(billinglines)
    outfile.close()
#################
#os.system('emailrp_with_attach.py ' + fname)
