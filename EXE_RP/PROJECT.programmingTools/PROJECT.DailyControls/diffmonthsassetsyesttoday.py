
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
test = path + 'test/'
print path
ypath = 'Y:/EXE/'
##############################
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
################################  hard coded text lines   ################
actantheader = 'Actant AG \nBahnhofstrasse 10 \n6300 Zug \nSwitzerland \nVAT-No. CHE -104.529.180 MWST\n'
#actantfooter = 'Actant USA, here is going to be the address of Actant bank account'
payrequest = 'We kindly ask you to pay the oustanding balance in full by January 31 2012 to our bank as follows: \n\nAccount Name, Actant AG \n\nBank Address: \nUBS Zug \nBaarerstrasse 14a \n6300 Zug, Switzerland \nAccount Number: 273-225290.7G X \nBIC: UBSWCHZH80A \nIBAN: CH97 0027 3273 2252907G X \n\nAny queries regarding this invoice or the oustanding balance please contact Patricia Ulrich at +41 41 729 5601 or patricia.ulrich@actant.com'
payrequest2 = 'TEST TEST TEST ==== here is going to populate the EU footer with the pay request and bank details ==== TEST TEST TEST'
#####################################
sfreal = path + 'DATA/SFDATA/'
sfreal = ypath + 'DATA/SFDATA/'
listing = os.listdir(sfreal)
datelist=[]
dcount = 0
yest = '20120402'
for date in listing:
    print dcount
    dcount += 1
    
    if '201204' in date:
        sfdata = sfreal + date + '/' + date + '.sf.'
        sfdatay = sfreal + yest + '/' + yest + '.sf.'
        accountfile = sfdata + 'cases.csv'
        accountfiley = sfdatay + 'cases.csv'
        newfile = path + 'newfile.' + yest + '.csv'
        subprocess.Popen('cat ' + accountfile + ' ' + accountfiley + ' > ' + newfile ,shell=True)
        yest = date
        datelist.append(date)
        open(newfile,'r').close()
        #############
    print datelist
##
##subprocess.Popen('ls  ' + var + '* > newfilea',shell=True)
##sfdata = path
##for date in datelist:
##    print date
##    sfdata = sfreal + date + '/' + date + '.sf.'
##    print os.listdir(sfreal + '/' + date)
##    accountfile = open(sfdata + 'accounts.csv', 'r')
##    productfile = open(sfdata + 'products.csv', 'r')
##    assetfile =   open(sfdata + 'assets.csv', 'r')
##    contactsfile =   open(sfdata + 'contacts.csv', 'r')
##    passetsfile =   open(sfdata + 'prodassets.csv', 'w')
##    ###############################################
##    def csvContactsToLines():
##        csvr = csv.reader( contactsfile )
##        contactslines = []
##        for row in csvr:
##            contactslines.append( row )
##        return contactslines
##    contactslines = csvContactsToLines ()
##    print len(contactslines)
##    print ' is number of contacts'
##    ###############################################
##    ###############################################
##    def csvPRODUCTSToLines():
##        csvr = csv.reader( productfile )
##        productlines = []
##        for row in csvr:
##            productlines.append( row )
##        productfile.close()
##        return productlines
##    productlines = csvPRODUCTSToLines ()
##    print len(productlines)
##    print 'products'
##    ###############################################
##    def csvACCOUNTSToLines():
##        print ' loading accounts'
##        csvr = csv.reader( accountfile )
##        accountlines = []
##        for row in csvr:
##            status = str(row[35])
##            #status = 'Client'
##            #if status == 'Client' :
##            if 'CUTLERGR' in str(row):
##                accountlines.append( row )
##        print len(accountlines)
##        accountfile.close()
##        print 'done with accounts'         
##        return accountlines
##    accountlines =  csvACCOUNTSToLines ()
##    print len(accountlines)
##    print ' accounts' 
########################################################
##    def csvProductionAssetsToLines():
##        csvr = csv.reader( assetfile )
##        productionassetlines = []
##        filecsvwriter = csv.writer(passetsfile)
##        counter = 0
##        for row in csvr:
##            if row[17] == 'Production' :
##                productionassetlines.append( row )
##                counter = counter + 1
##                filecsvwriter.writerow( row )
##        return productionassetlines
##        #assetfile.close()
##        passetsfile.close()
##    productionassets = csvProductionAssetsToLines()
##    print len(productionassets)
##    print 'pro assets' 
##    
##    ###################################################
##    ##def csvASSETSToLines():
##    ##    csvr = csv.reader( assetfile )
##    ##    assetlines = []
##    ##    for row in csvr:
##    ##        if row[0] == acctid:
##    ##            assetlines.append( row )
##    ##    assetfile.close()        
##    ##    return assetlines
##    ###############################################
##    ###############################################
##    for line in accountlines:
##        nameacct =  line[3]
##        sagecode = line[95]
##        acctid = line[0]
##        
##        ##########################
##        #csvr = csv.reader( assetfile )
##        assetlines = []
##        for row in productionassets:
##            if row[2] == acctid :
##                assetlines.append( row )
##        assetfile.close()
##        ######################
##        billrule = line[115]
##        status = line[35]
##        billingcycle = line[103]
##        payabledate = line[124]
##        currencyBillable = line[23]
##        outstandings = line[117]
##        ItemRate = 1
##        custaddrblock = '\n' + line[3] + '\n' + line[7] + '\n' + line[8] + '\n' + line[9] + line[10] + ' ' + line[11]
##        formathead = "%9s, %9s, %9s, %9s, %9s, %9s, %s, %s\n"
##        LineItemHeader =  (formathead % ('Machine ID','Item/Description','License','Start Date','End Date','Stocks','Rate','Total'))
##        outfilename = test + '/' +  date + '.' + sagecode + '.' + '1' + '.' + 'EU' + '.csv'
##        outfile = open(outfilename, 'w')
##        outfile = open(outfilename, 'a')
##        outfile.write('\n\n' + actantheader)
##        AssetProductName = 'bla'
##        totalassetclasses = 0
##        billinglines2 = ''
##        count = 0
##        alluserslist=[]
##    #################################
##        for aline in assetlines:
##            AssetProductID = aline[3]
##            assetstatus = aline[17]
##            machineid = aline[20]
##            expiration = aline[21]
##            exchanges = aline[27]
##            assetrole = aline[41]
##            license = aline[42]
##            name = aline[12]
##            product = aline[69]
##            startdate = aline[135]
##            enddate = aline[136]
##            username = aline[1]
##            for row in contactslines:
##                if username == row[0]:
##                    cusername =  row[7]
##                    both = cusername + ' ' + row[0]
##                    alluserslist.append(both)
##            rate = assetclassesint = 0
##            total = 0
##            if aline[134] != '':                    
##                rate = float(aline[134])  
##            assetclasses = aline[62]
##            if aline[62] != '':
##                assetclassesint = int(float(aline[62]))
##                
##  
##            for bline in productlines:
##                ProductProductID = bline[0]
##                if AssetProductID == ProductProductID:
##                    AssetProductName = bline[1]
##            totalassetclasses = totalassetclasses + assetclassesint 
##            count += 1 
##            total = rate + total
##            format = "%13s, %19s, %9s, %9s, %9s, %9s, %d %s %s\n"
##            billinglines2 = billinglines2 + (format % (sagecode, AssetProductName, license, startdate, enddate, assetclasses, rate, total,cusername))
##    ######################
##        for user in alluserslist:
##            for aline in assetlines:
##                if aline[1] == user:
##                    print user,aline[0]
##        #print billinglines2
##        formattot = "%10s %30s | totalclasses = %3d| total rates = %9.2f %d \n"
##        totalline = (formattot % (sagecode, nameacct, totalassetclasses, total, count))
##        outfile.write('\n' +  totalline + billinglines2 + 3*'\n\n')
##        print totalline
##    contactsfile.close()
##    productfile.close()
##    assetfile.close()
##    contactsfile.close() 
##    passetsfile.close() 
##
