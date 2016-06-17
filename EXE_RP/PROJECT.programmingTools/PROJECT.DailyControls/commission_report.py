
import os, sys, glob, csv, subprocess, datetime, shutil, difflib
#from difflib_data import *
path = os.getcwd() + '/'
test = path + 'test/'
print path
##############################
todaystring = str(datetime.date.today().strftime('%Y%m%d'))
################################  hard coded text lines   ################
sfreal = path + 'DATA/SFDATA/'
searchdate = '201204'
month = searchdate[0:6]
sfmonth = sfreal + '/' + month + '/'
ysfmonth = sfreal + '/' + ymonth + '/'
listing = os.listdir(sfmonth)
listing = ['20120402']
#print listing

#########  SELECT a file ###################
ftypes = ['assets', 'accounts', 'products', 'contacts']
ftypes =['assets']
for ftype in ftypes:
    datelist=[]
    dcount = 0
    for date in listing:
        dcount += 1
        if '2012' in date and dcount < 6:
            ymonth = month = date[0:6]
            print date, ydate
            sfdatefile1 = sfmonth + '/' + date + '/' + date + '.sf.' + ftype + '.csv'

commission_calc_date = '20120401'

for asset in assets:
    commishEND = asset[137]
    commishSTART = asset[135]
##test if commission end date is before the calc date
    if commishEND > commission_calc_date:
        test1 = 'pass'
        days1 = 90
        
        else
        do nothing
    
    if test1 = 'pass' and commishSTART >
## then test if the commission start date is before the calc date and how many days, max 90

##calculate the number of days in this quarter valid if passes first two tests..

###########
    sfdata = path + 'DATA/SFDATA/' + month + '/' + filedate + '/' + filedate + '.sf.'
    accountfile = open(sfdata + 'Accounts.csv', 'r')
    assetfile = open(sfdata + 'assets.csv', 'r')
    productfile = open(sfdata + 'products.csv', 'r')
###############################################
def csvPRODUCTSToLines():
    csvr = csv.reader( productfile )
    productlines = []
    for row in csvr:
        productlines.append( row )
    productfile.close()
    return productlines
productlines = csvPRODUCTSToLines ()
###############################################
def csvACCOUNTSToLines():
    print ' loading accounts'
    csvr = csv.reader( accountfile )
    accountlines = []
    dcount = 0 
    for row in csvr:
        dcount += 1
        status = str(row[35])
        #status = 'Client'
        if status == 'Client' :
            accountlines.append( row )
    print len(accountlines)
    accountfile.close()
    print 'done with accounts'         
    return accountlines
accountlines =  csvACCOUNTSToLines ()
###################################################
##def csvASSETSToLines():
##    csvr = csv.reader( assetfile )
##    assetlines = []
##    for row in csvr:
##        if row[0] == acctid:
##            assetlines.append( row )
##    assetfile.close()        
##    return assetlines
###############################################
###############################################
actcount = 0
for line in accountlines:
    actcount += 1
    if actcount < 6:
        count = 0
        status = line[35]
        territory = line[34]
        sagecode = line[95]
        currency = line[23]
        nameacct = line[3]
        acctid = line[0]
        ##########################
        assetfile = open(sfdata + 'assets.csv', 'r')
        csvr = csv.reader( assetfile )
        assetlines = []
        #print acctid
        for row in csvr:
            if row[2] == acctid :
                assetlines.append( row )
        assetfile.close()
        print len(assetlines)
        print ' that was assetlines found'
        ######################
        #assetlines = csvASSETSToLines (acctid)
        print   sagecode, nameacct, territory
        billrule = line[115]
        status = line[35]
        billingcycle = line[103]
        payabledate = line[124]
        currencyBillable = line[23]
        outstandings = line[117]
        ItemRate = 1
        custaddrblock = '\n' + line[3] + '\n' + line[7] + '\n' + line[8] + '\n' + line[9] + line[10] + ' ' + line[11]## <--- I did changes here - MACIEJ
        contactblock = 'CONTACT: ' + line[105] + '\n' + 'email: ' + line[106] + '\n'
        invoiceDateBlock = 'Invoice Number: ' + '09231-IN <-- test number' + '\n' + 'Invoice Date:  ' + filedate
        payableBlock = 'Invoice Due Date: ' + 'Payable Upon Receipt' + '; ' + 'Payable: ' + '30 Days' + '\n'
        customerBlock = 'Customer code: ' + line[95]
        formathead = "%9s, %9s, %9s, %9s, %9s, %9s, %s, %s\n"
        LineItemHeader =  (formathead % ('Machine ID','Item/Description','License','Start Date','End Date','Stocks','Rate','Total'))
        outfilename = test + '/' +  filedate + '.' + sagecode + '.' + '1' + '.' + 'EU' + '.csv'
        outfile = open(outfilename, 'w')
        outfile = open(outfilename, 'a')
        outfile.write('\n\n' + actantheader)
        outfile.write('\n\n' + custaddrblock)
        outfile.write('\n\n' + contactblock)
        outfile.write('\n\n' + invoiceDateBlock)
        outfile.write('\n\n' + payableBlock)
        outfile.write('\n\n' + customerBlock)
        outfile.write('\n\n' + LineItemHeader)
        billinglines = billinglines2 = LineItemFooter = ' '
        AssetProductName = 'bla'

    #################################
        for aline in assetlines:
            AssetProductID = aline[3]
            count = count + 1
            assetstatus = aline[17]
            machineid = aline[20]
            expiration = aline[21]
            exchanges = aline[27]
            assetrole = aline[41]
            license = aline[42]
            name = aline[12]
            product = aline[69]
            startdate = aline[135]
            enddate = aline[136]
            rate = 0
            total = 0
            if aline[134] != '':                    
                rate = float(aline[134])      
            assetclasses = aline[62]
            if assetclasses is None:
                assetclasses = 0
                print assetclasses + 'assetclasses'          
            for bline in productlines:
                ProductProductID = bline[0]
                if AssetProductID == ProductProductID:
                    AssetProductName = bline[1]
            if assetstatus == 'Production': ### <--- I made changes here (MACIEJ)
                total = rate + total
                format = "%13s, %19s, %9s, %9s, %9s, %9s, %d %s\n"
                #print format % (machineid, billrule, license, startdate, enddate, assetclasses, rate)
                billinglines2 = billinglines2 + (format % (sagecode, AssetProductName, license, startdate, enddate, assetclasses, rate, total))            
    ######################
        print billinglines2 


