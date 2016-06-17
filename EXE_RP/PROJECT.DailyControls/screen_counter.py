
import subprocess as S
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
test = path + 'test/'
print path
##############################
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
print todaystring
todaystring = '20120319'
################################  hard coded text lines   ################
actantheader = 'Actant AG \nBahnhofstrasse 10 \n6300 Zug \nSwitzerland \nVAT-No. CHE -104.529.180 MWST\n'
#actantfooter = 'Actant USA, here is going to be the address of Actant bank account'
payrequest = 'We kindly ask you to pay the oustanding balance in full by January 31 2012 to our bank as follows: \n\nAccount Name, Actant AG \n\nBank Address: \nUBS Zug \nBaarerstrasse 14a \n6300 Zug, Switzerland \nAccount Number: 273-225290.7G X \nBIC: UBSWCHZH80A \nIBAN: CH97 0027 3273 2252907G X \n\nAny queries regarding this invoice or the oustanding balance please contact Patricia Ulrich at +41 41 729 5601 or patricia.ulrich@actant.com'
payrequest2 = 'TEST TEST TEST ==== here is going to populate the EU footer with the pay request and bank details ==== TEST TEST TEST'

#####################################
filedate = todaystring
sfdata = path + 'DATA/SFDATA/' + filedate + '/' + filedate + '.sf.'
accountfile = open(sfdata + 'accounts.csv', 'r')
assetfile = open(sfdata + 'assets.csv', 'r')
###################################################
def csvASSETSToLines():
    csvr = csv.reader( assetfile )
    assetlines = []
    for row in csvr:
        assetlines.append( row )
    return assetlines
assetlines = csvASSETSToLines ()
###############################################
###############################################
def csvACCOUNTSToLines():
    csvr = csv.reader( accountfile )
    accountlines = []
    for row in csvr:
        accountlines.append( row )
    return accountlines
accountlines =  csvACCOUNTSToLines ()

outfilename = path + '/' +  filedate + '.' + '.' + '1' + '.' + 'EU' + '.csv'
outfile = open(outfilename, 'w')
###############################################
for line in accountlines:
    count = 0
    status = line[35]
    territory = line[34]
    territory = 'US'
    sagecode = line[95]
    #if status == 'Client':
    if sagecode == 'MAVENDER':
        print line
        print sagecode
        currency = line[23]
        nameacct = line[3]
        acctid = line[0]
        print acctid
        billrule = line[115]
        status = line[35]
        billingcycle = line[103]
        payabledate = line[124]
        currencyBillable = line[23]
        outstandings = line[117]
        ItemRate = 1
        custaddrblock = '\n' + line[3] + '\n' + line[7] + '\n' + line[8] + '\n' + line[9] + line[10] + ' ' + line[11]## <--- I did changes here - MACIEJ
        print custaddrblock
        contactblock = 'CONTACT: ' + line[105] + '\n' + 'email: ' + line[106] + '\n'
        print contactblock
        invoiceDateBlock = 'Invoice Number: ' + '09231-IN <-- test number' + '\n' + 'Invoice Date:  ' + filedate
        payableBlock = 'Invoice Due Date: ' + 'Payable Upon Receipt' + '; ' + 'Payable: ' + '30 Days' + '\n'
        customerBlock = 'Customer code: ' + line[95]
        #LineItemHeader = '\nBillingdate    description    unit price    units     Total price\n'
        #LineItemHeader = '\nItem/Description License Start Date End Date  Stocks Rate   Total'
        LineItemHeader = 'Machine ID' + ',' + 'Item/Description' + ',' 'License' + ',' + 'Start Date' + ',' + 'End Date' + ','  + 'Stocks' + ',' + 'Rate' + ',' + 'Total'
        billinglines = '\n'
       
        outfile = open(outfilename, 'a')
        outfile.write('\n\n' + actantheader)
        billinglines = billinglines2 = ' '
        ###add indiv description asset lines
#################################
        for aline in assetlines:
            assetstatus = aline[17]
            if acctid in aline and assetstatus == 'Production': ### <--- I made changes here (MACIEJ)
                count = count + 1
                sumTotalPrice = str(ItemRate * count)
                sum_units = str(count)
                LineItemFooter = '\nTotals    ' + sum_units + '    ' +   sumTotalPrice + ' '  + currencyBillable
                assetrole = aline[41]
                assetclasses = aline[62]
                startdate = aline[135]
                enddate = aline[136]
                rate = aline[134]
                #floatAC = float(assetclasses)
                #floatR = float(rate)
                #total = floatAC * floatR
                #total = str(assetclassesint * rateint))
                #total = int('assetclasses') * int('rate')
                machineid = aline[20]
                expiration = aline[21]
                exchanges = aline[27]
                assetrole = aline[41]
                license = aline[12]
                name = aline[12]
                product = aline[69]
                product = aline[]
                assetstatus = aline[103]
                billinglines = billinglines + sagecode + billrule + assetrole + exchanges + '\n'
                format = "%9s, %9s, %9s, %9s, %9s, \n"
                print format % (sagecode, product, assetclasses, rate, expiration)
##################################
        outfile.write('\n\n' + billinglines2)
        outfile.write('\n\n' + LineItemFooter)
        if territory == 'US':
            footerfile = open(path + '/footer.eu.txt', 'r')
        else:
            footerfile = open(path + '/footer.usa.txt', 'r')
        outfile.close()
        newout = open(outfilename, 'a')
        shutil.copyfileobj(footerfile, newout)
        newout.close()
        footerfile.close()
######################
