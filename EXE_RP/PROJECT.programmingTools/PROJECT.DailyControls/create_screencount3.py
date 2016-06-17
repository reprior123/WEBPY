
import subprocess as S
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, sets
path = os.getcwd() + '/'
print path
test = path + 'test'
##############################
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
print todaystring
todaystring = '20120323'
todaystring = 'shortfile'
filedate = todaystring
#path = 'Y://EXE/'
sfdata = path + 'DATA/SFDATA/' + filedate + '/' + filedate + '.sf.'
SFAREA = path + 'DATA/SFDATA/'
fname = 'screens.txt'
bla = path + '/bla.txt'
outfile = open(path + '/' + fname, 'w')
outfile = open(path + '/' + fname, 'a')
targetcsvfile = open(path + '/accounts.clients_only.csv', 'w')
accountfile = open(sfdata + 'accounts.csv', 'r')
assetfile = open(sfdata + 'assets.csv', 'r')
##################################
###############################################
def csvACCOUNTSToLines():
    csvr = csv.reader( accountfile )
    accountlines = []
    filecsvwriter = csv.writer(targetcsvfile)
    counter = 0
    for row in csvr:
        counter = counter + 1
        status = row[35]
        if status == 'Client':
            accountlines.append( row )
            #print status
            filecsvwriter.writerow( row )
    return accountlines
accountlines =  csvACCOUNTSToLines ()
###############################################
def csvASSETSToLines():
    csvr = csv.reader( assetfile )
    assetlines = []
    for row in csvr:
        assetlines.append( row )
    return assetlines
assetlines = csvASSETSToLines ()
###############################################
def f6():
#Not order preserving    
    set = Set(blalist)
    return list(set)
##############################################
def grabAssetlines():
    assetlinesset =[]
    for aline in assetlines:
        assetstatus = aline[17]
        assetrole = aline[41]
        #if acctid in aline and assetstatus == 'Production':
        if acctid in aline and assetstatus != 'Expired':
            assetlinesset.append(aline)
    #print assetlinesset
    return assetlinesset
#assetlinessetb = grabAssetlines()
######################
outfile = open(path + '/' + fname, 'w')
for line in accountlines:
    assetlinessetb = grabAssetlines()
    count = 0
    status = line[35]
    territory = line[34]
    #territory = 'US'
    sagecode = line[95]
    if status == 'Client':
    #if sagecode == 'CUTLERGR':
        #print line
        #print sagecode
        currency = line[23]
        assetclasses = 0
        nameacct = line[3]
        acctid = line[0]
        billrule = line[115]
        status = line[35]
        billingcycle = line[103]
        payabledate = line[124]
        currencyBillable = line[23]
        outstandings = line[117]
        ItemRate = 1
        ###add indiv description asset lines
#################################
        blafile = open(bla, 'w')
        blafile = open(bla, 'a')
        blalist = []
        for aline in assetlinessetb:
            assetstatus = aline[17]
            assetrole = aline[41]
            #assetrole = aline[20]
            #if acctid in aline and assetstatus == 'Production': ### <--- I made changes here (MACIEJ)
            blafile.write(str(assetrole) + '\\n')
            if assetrole != 'ffff':
                blalist.append(str(assetrole))
                #print blalist
            count = count + 1
            #sumTotalPrice = str(ItemRate * count)
            sum_units = str(count)
            #assetclasses =  assetclasses + int(aline[62])
            assetclasses = 0
            #if not assetclasses.isdigit():
            #   print (assetclasses, 'is not a valid input')
            #startdate = aline[135]
            #enddate = aline[136]
            #rate = aline[134]
            #floatAC = float(assetclasses)
            #floatR = float(rate)
            #total = floatAC * floatR
            #total = str(assetclassesint * rateint))s
            #total = int('assetclasses') * int('rate')
            total = '44'
            #total = int('assetclasses') * int('rate')
            machineid = aline[20]
            expiration = aline[21]
            exchanges = aline[27]
            license = aline[12]
            name = aline[12]
            product = aline[69]
            assetstatusnew = aline[103]
        #print blalist
        setone = set(blalist)
        lsttwo = list(setone)
        print lsttwo
        rcount = 0
        for role in lsttwo:
            rcount = 0
            for aline in assetlinessetb:
                assetstatus = aline[17]
                assetrole = aline[41]
                #assetrole = aline[20]
                if role == assetrole:
                    rcount = rcount +  1
            print role, rcount
        linestr = str(line)
        status = line[35]
        sagecode = line[95]
        format = "%9s, %29s %5d \n"
        format2 = " %4d %9s, %9s, %5d, %5s, %5s, %3s, %s \n"
        #outfile.write(format % (sagecode, nameacct, count))
        #print (format % (sagecode, nameacct, count))
        print (format2 % (count, sagecode, assetrole, count, product, nameacct, expiration, status))
        outfile.write(format2 % (count, sagecode, assetrole, count, product, nameacct, expiration, status))
    ###### this uniqs the blafile .  ######
        newj = getUniqueSynset(blalist)
        print newj
import sys
outfile = open(path + '/' + fname, 'r')
linesb = outfile.readlines()
linesb.sort(reverse=True)
#map(sys.stdout.write, linesb)
outfile = open(path + '/' + fname, 'w')
outfile = open(path + '/' + fname, 'a')
map(outfile.write, linesb)
outfile.close()

print 'done'



