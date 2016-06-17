
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#####   looper can kick this off with two args sage n biildate  #######
######


#########
numargs = len(sys.argv)
if numargs > 1:
    print 'args there'
    print numargs
    sagehard = sys.argv[1]
    periodstart = sys.argv[2]
    cmode = sys.argv[3]
    billmode = sys.argv[4]
else:
    print 'Arguments are required and can be entered from commandline or here'
    sagehard = raw_input(' Enter Sagecode here: ')
    periodstart = raw_input('start date of billing cycle [ex. 13-02-2012] ')
    cmode = raw_input('country_mode[ex. US or EU]: ')
    billmode = raw_input('puimode[normal or pui]: ')
# testing overrides  ####
cmode = 'EU'
sagehard = 'ABR'
periodstart = '01-05-2012'
billmode = 'normal' 
#########
###################
path = os.getcwd() + '/'
test = path + 'test/'
config = path + 'billing_config_files/'
print path
#########
sfarea = path + 'DATA/SFDATA/'
AssetProductName = 'bla'
##############################
date_format = "%d-%m-%Y"
today = datetime.date.today()
todayf = today.strftime(date_format)
old_date_format = "%Y%m%d"
todayoldf = today.strftime(old_date_format)
todaystring = str(todayf)
dateToCheck = '20120614'
prevdate = todaystring
month = dateToCheck[0:6]
############################
######  dates set here   #############################
from datetime import timedelta
from datetime import datetime
#hard codes for testing #########
print sagehard
##########################
invoiceharddate = todaystring
invoice_sequence = sagehard + '.' + periodstart + '.01'
specialperiodend = '01-08-2012'
paybyDAYS = 20
import datetime
#################################
filedate = dateToCheck
sfmonth = sfarea + month + '/'
sfdata = path + 'DATA/SFDATA/' + month + '/' + filedate + '/' + filedate + '.sf.'
##############################
accountfile = open(sfdata + 'Accounts.csv', 'r')
assetfile = open(sfdata + 'assets.csv', 'r')
productfile = open(sfdata + 'products.csv', 'r')
contactsfile = open(sfdata + 'contacts.csv', 'r')
###############################################
def csvPRODUCTSToLines():
    csvr = csv.reader(productfile)
    productlines = []
    for row in csvr:
        productlines.append( row )
    productfile.close()
    return productlines
    productfile.close()
productlines = csvPRODUCTSToLines ()
###############################################
def csvACCOUNTSToLines():
    print ' loading accounts'
    csvr = csv.reader( accountfile )
    accountlines = []
    dcount = 0
    for row in csvr:
        dcount += 1
        sage = str(row[95])
        if sage == sagehard:
            accountlines.append( row )
    print len(accountlines)
    accountfile.close()
    print 'done with accounts'
    return accountlines
    accountfile.close()
accountlines =  csvACCOUNTSToLines ()
###################################################
def csvCONTACTSToLines():
    csvr = csv.reader( contactsfile )
    contactlines = []
    for row in csvr:
        contactlines.append( row )
    contactsfile.close()
    return contactlines
    contactsfile.close()
contactlines = csvCONTACTSToLines ()
####################################################
def csvASSETSToLines(afile):
    csvr = csv.reader( afile )
    assetlinesCC = []
    for row in csvr:
        assetlinesCC.append( row )
    assetfile.close()
    return assetlinesCC

#############################
actcount = 0
for line in accountlines:
    actcount += 1
    if actcount < 100:
        count = 0
        status = line[35]
        territory = line[34]
        sagecode = line[95]
        currency = line[23]
        nameacct = line[3]
        acctid = line[0]
        billrule = line[115]
        status = line[35]
        ItemRate = 1
        ##########################
        dateloop = '20120615 20120614'
        month ='201206'
        for date in dateloop:
            billinglines = ' ' 
            sfmonth = sfarea + month + '/'
            sfdata = path + 'DATA/SFDATA/' + month + '/' + filedate + '/' + filedate + '.sf.'
            assetfile = open(sfdata + 'assets.csv', 'r')
            assetlinesCC = csvASSETSToLines (assetfile)
            totalinesCC = str(len(assetlinesCC))
            assetlines = []
            for row in assetlinesCC:
                if row[2] == acctid :
                    assetlines.append( row )
            totalines = str(len(assetlines))
            #################################
            total = rate = totalClasses = assetclasses = totalProdAssets = 0
        #################################
    for aline in assetlines:
        AssetProductID = aline[3]
        count = count + 1
        assetstatus = aline[17]
        assetcontact = aline[1]
    #################################
        machineid = aline[20]
        expiration = aline[21]
        exchanges = aline[27]
        assetrole = aline[41]
        license = aline[42]
        name = aline[12]
        product = aline[69]
        startdate = aline[135]
        enddate = aline[136]
        rate = assetclasses = 0
        if aline[134] != '':
            rate = float(aline[134])
        if aline[62]  != '':
            assetclasses = float(aline[62])
        for bline in productlines:
            ProductProductID = bline[0]
            if AssetProductID == ProductProductID:
                AssetProductName = bline[1]
        if assetstatus == 'Production':
            for contactline in contactlines:
                if contactline[0] == assetcontact:
                    contactname = contactline[7]
                    lastmodname = contactline[34]
                    print contactline[0], assetcontact, contactline[7], lastmodname
            totalprice = rate * 1
            total += totalprice
            totalClasses = float(assetclasses) + totalClasses
            totalProdAssets += 1
            totalClasses = 0
            numbermonths = 1
            format = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td><div align=\"center\">%6d </td><td><div align=\"right\">%8.2f </td><td><div align=\"right\">%8.2f</td></tr>\n"
            billingline = (format % (AssetProductName, contactname, date, ' xx', numbermonths, rate, totalprice))
            billinglines = billinglines + billingline
        print billinglines
            

    controlline = 'Controlline' + sagecode + 'totalbill=  ' + str(total) + ' '  + nameacct + ' ' + territory + ' |total assetlines ==' + totalines + ' |rundate = ' + filedate
    formathead = "<b><tr bgcolor=\"grey\"><td><b>%-20s </b></td><td><b>%-20s </b></td><td><b><div align=\"center\">%-8s </div></b></td><td><b>%-8s </b></td><td><b>%6s </b></td><td><b><div align=\"center\">%10s </b></td><td><b><div align=\"right\">%10s</b></td></tr></b>\n"
    LineItemHeader =  (formathead % ('Item/Descript.','Username','Billing','Period','Months','Rate', 'SubTotl'))
    #############
    #tformat = "%-20s %-20s %-8s %-8s %6d %-8s %8.2f\n"
    tformat = "<tr><td><b>%-20s </b></td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td>%6s </td><td>%10s </td><td><b><div align=\"right\">%8.2f<b></td></tr>\n"
    totallines = (tformat % ('Grand Total ', ' ', str(totalProdAssets), '', '', '', total))
    dateToCheck = '20120529'

##### html blocks n tags ##############
logofile = '<div align=\"right\"><img src=\"logoactant.JPG\" alt=\"some_text\"/></div align=\"right\">'
#s2 = '\n\n'
s1 = '<br />\n'
s2 = '<br /><br />\n\n'
#s1 = '\n'
starthtml = ' <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">\n <html lang=\"EN\" dir=\"ltr\">'
endhtml = ' </html>'
printa = '<p>'
printa_center= '<p align="center">'
printb = '</p>'
bolda = '<strong>'
boldb = '</strong>'
tablea = '<table width=\"730\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" frame=\"box\"> '
tablegraya = '<table width=\"730\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" frame=\"box\" bgcolor=\"#cccccc\"> '
tableacenter = '<table width=\"300\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" frame=\"box\" align=\"center\"> '
tableb = '</table>'
rowa = '<tr>'
rowb = '</tr>'
cola = '<td>'
colb = '</td>'
colab = colb + cola
tablenice = '<table border="void"  cellspacing="2" cellpadding="2" width="300"  align="center">'
centercella = '<tr><td><i><strong><font face="arial, helvetica, sans-serif"></font><font size="4"><div align="center">'
centersmallcella = '<tr><td><i><strong><font face="arial, helvetica, sans-serif"></font><font size="1"><div align="center">'
centercellb = '</div></font></i></strong></td></tr>'
###############
        

