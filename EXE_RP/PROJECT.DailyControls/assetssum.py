
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time

###################
path = os.getcwd() + '/'
test = path + 'test/'
print path
#########
footerfile = open(bconfig +  'footer.'  + countrytag + '.' +  currency + '.txt', 'r')
sfarea = path + 'DATA/SFDATA/'
outfile = open(test + '.assetsINV.' + periodstart + '.' + countrytag + '.html', 'w')
LineItemFooter = ''
billinglines = adetaillines = ' '
AssetProductName = 'bla'

date_format = "%d-%m-%Y"
today = datetime.date.today()
todayf = today.strftime(date_format)
old_date_format = "%Y%m%d"
todayoldf = today.strftime(old_date_format)
todaystring = str(todayf)
todaystringold = str(todayoldf)
todaystringold = '20120503'
filedate = '20120503'
dateToCheck = todaystringold
prevdate = todaystring
month = dateToCheck[0:6]
sfmonth = sfarea + month + '/'
######  dates set here   #############################
from datetime import timedelta
from datetime import datetime

##########################
##invoiceharddate = todaystring
##invoice_sequence = '.' + periodstart + '.01'
##specialperiodend = '01-08-2012'
##
##paybyDAYS = 20
#### set quarterly monthly etc here with ndays ##
##ndays = numbermonths * 365/12
##
##pstart = datetime.strptime(periodstart, date_format)
##pendpartial = datetime.strptime(specialperiodend, date_format)
##
##cycleend = (pstart + timedelta(days=ndays)).strftime(date_format)
###payby_date = periodstart + 20
##payby_date = (pstart + timedelta(days=paybyDAYS)).strftime(date_format)
##delta = pendpartial - pstart
##partialmth = ('%3.1f' %((delta.days / 30)))
##print periodstart, numbermonths, ndays, cycleend, partialmth, payby_date
##periodend = cycleend
import datetime
#################################
filedate = dateToCheck
sfdata = path + 'DATA/SFDATA/' + month + '/' + filedate + '/' + filedate + '.sf.'
accountfile = open(sfdata + 'Accounts.csv', 'r')
assetfile = open(sfdata + 'assets.csv', 'r')
productfile = open(sfdata + 'products.csv', 'r')
contactsfile = open(sfdata + 'contacts.csv', 'r')
###############################################
def csvASSETSToLines():
    csvr = csv.reader( assetfile )
    assetlines = []
    for row in csvr:
        assetlines.append( row )
    assetfile.close()
    return assetlines

assetlines = csvASSETSToLines ()
totalines = str(len(assetlines))
#############################
##actcount = 0
##pui_tuples = []
##for line in accountlines:
##    actcount += 1
##    if actcount < 100:
##        count = 0
##        status = line[35]
##        territory = line[34]
##        sagecode = line[95]
##        currency = line[23]
##        nameacct = line[3]
##        acctid = line[0]
##        billrule = line[115]
##        status = line[35]
##        billingcycle = line[103]
##        payabledate = line[124]
##        currencyBillable = line[23]
##        outstandings = line[117]
##        slabillrule = line[123]
##        ItemRate = 1
##        ##########################
##        assetlines = []
##        for row in assetlinesCC:
##            if row[2] == acctid :
##                assetlines.append( row )
##        totalines = str(len(assetlines))
##        #################################
##        total = rate = totalClasses = assetclasses = totalProdAssets = 0
##        puilevels ={}
##        totalClasses = 0
    #################################
for aline in assetlines:
    AssetProductID = aline[3]
    count = count + 1
    assetstatus = aline[17]
    assetcontact = aline[1]
    assetName = aline[12]
#################################
    machineid = aline[20]
    expiration = aline[21]
    exchanges = aline[27]
    assetrole = aline[41]
    license = aline[42]
    name = aline[12]
    
    proddesc = aline[19]
    #product = aline[69] + proddesc
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
            #print contactline[0], assetcontact, contactline[7]
            if contactline[0] == assetcontact:
                contactname = contactline[7]
                lastmodname = contactline[34]
                #print contactline[0], assetcontact, contactline[7], lastmodname
        totalprice = rate * numbermonths
        total += totalprice
        totalClasses = float(assetclasses) + totalClasses
        totalProdAssets += 1
        #totalClasses = 0
        empty = ' '
        if 'Classic_PUI' in  slabillrule:
            puirate = rate
            puibreak = aline[138]
            bla = 'bla'
            AssetProductName = ' PUI Scale'
            if puirate > 1:
                #puilevels += [str(puirate) + ' ' + str(puibreak)]
                puilevels[puirate] = puibreak
                #pui_tuples.append(puirate, puibreak)
                format = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td><div align=\"center\">%6d </td></tr>\n"
                adetailline = (format % (contactname, assetName, periodend, assetclasses))
            else:
                bla = bla
        else:
            format = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td><div align=\"center\">%6d </td><td><div align=\"right\">%8.2f </td><td><div align=\"right\">%8.2f</td></tr>\n"
            billingline = (format % (AssetProductName, contactname, periodstart, periodend, numbermonths, rate, totalprice))
            format = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td><div align=\"center\">%6d </td></tr>\n"
            adetailline = (format % (contactname, assetName, periodend, assetclasses))
            format = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td><div align=\"center\">%6s </td><td><div align=\"right\">%8s </td><td><div align=\"right\">%8s</td></tr>\n"
            billingline2 = (format % (proddesc, empty, empty, empty, empty, empty, empty))
            ### pui billinglines ####
            #billingline = (format % (AssetProductName, contactname, startdate, enddate, assetclasses, rate, totalprice))
            billinglines = billinglines + billingline +billingline2
            adetaillines = adetaillines + adetailline

        print adetaillines        
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
tablenice = '<table="void"  cellspacing="2" cellpadding="2" width="300"  align="center">'
centercella = '<tr><td><i><strong><font face="arial, helvetica, sans-serif"></font><font size="4"><div align="center">'
centersmallcella = '<tr><td><i><strong><font face="arial, helvetica, sans-serif"></font><font size="1"><div align="center">'
centercellb = '</div></font></i></strong></td></tr>'
###############
######## create header in a table form   ######
#tablenice = '<table border="2"  cellspacing="2" cellpadding="2" width="300" bgcolor="#cc9999" align="center">'
headerEU = tablenice
for litem in [hname, hstreet, hzip, hcountry]:
    headerEU = headerEU + centercella
    headerEU = headerEU + litem
    headerEU = headerEU + centercellb
headerEU = headerEU + centersmallcella + hvat
headerEU = headerEU + centercellb 
headerEU = headerEU + tableb
#################################
custaddrblock = s1 + line[3] + s1 + line[7] + s1 + line[8] + s1+ line[9] + line[10] + ' ' + line[11] + s2
contactblock = 'CONTACT: ' + line[105] + s1 + 'email: ' + line[106]  + s1
invoiceperiod =  'Invoice Period:  ' + periodstart + ' to ' + periodend + s1
invoiceDateBlock = 'Invoice Number:  ' + invoice_sequence + s1 + 'Invoice Date:  ' + invoiceharddate 
payableBlock = 'Invoice Due Date:  ' + payby_date  
customerBlock = 'Customer code:  ' + line[95] + s1
customerBlock =  s1

controlline = 'Controlline' + sagecode + 'totalbill=  ' + str(total) + ' '  + nameacct + ' ' + territory + ' |total assetlines ==' + totalines + ' |rundate = ' + filedate
payus_string = 'We kindly ask you to pay the oustanding balance in ' + bolda + currencyBillable +boldb + ' in full by:'
#############
#formathead = "%-20s %-20s %-8s %-8s %6s %8s %8s\n<br />%s\n<br />%s \n"
#formathead = "<tr><td>%-20s </td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td>%6s </td><td>%10s </td><td>%10s</td></tr>\n"
formathead = "<b><tr bgcolor=\"grey\"><td><b>%-20s </b></td><td><b>%-20s </b></td><td><b><div align=\"center\">%-8s </div></b></td><td><b>%-8s </b></td><td><b>%6s </b></td><td><b><div align=\"center\">%10s </b></td><td><b><div align=\"right\">%10s</b></td></tr></b>\n"
LineItemHeader =  (formathead % ('Item/Descript.','Username','Billing','Period','Months','Rate', 'SubTotl'))
#############
#tformat = "%-20s %-20s %-8s %-8s %6d %-8s %8.2f\n"
tformat = "<tr><td><b>%-20s </b></td><td>%-20s </td><td>%-8s </td><td>%-8s </td><td>%6s </td><td>%10s </td><td><b><div align=\"right\">%8.2f<b></td></tr>\n"
from operator import itemgetter, attrgetter

#print sorted(pui_tuples, key=itemgetter(1),reverse=True)
print sorted(puilevels, reverse=True)
print puilevels.values()
for puir in puilevels:
    print puilevels[puir]
    print totalClasses
    stocks = totalClasses - float(puilevels[puir])
    print stocks
    print puir
    
print totalClasses
totallines = (tformat % ('Sub Total ', ' ', str(totalProdAssets), '', '', '', total))
totallines0VAT = (tformat % ('VAT ', ' ', ' ', '', '', '', 0.00))
totallinesVAT = (tformat % ('Total incl. vat ', ' ', ' ', '', '', '', total))
########################  start letter HTML   ######
infolines = s1
allletters = s1
letter = s1 + starthtml  ### take out the letter here to create indiv letters
###################
letter = letter +  headerEU +s1 + logofile
letter = letter + s2  + custaddrblock + contactblock + invoiceperiod + invoiceDateBlock  + customerBlock + payableBlock + s2
#letter = letter + tablegraya + LineItemHeader + tableb + tablea +  billinglines + s1 + tableb
letter = letter + tablea + LineItemHeader + billinglines + s1 + totallines + s1 +  totallines0VAT + s1 + totallinesVAT + tableb
letter = letter + s1
letter = letter + s1 + payus_string + s1 + payby_date + s1
letter = letter + printa + bolda + str(footerfile.read()) + boldb + printb + s1
letter = letter + s1 +  endhtml
#print letter
#### open file to write to #####
outfile.write('\n' + letter)
footerfile.close()
outfile.close()
infolist.close()   ### need to remove these closers when createing indiv letters...
dateToCheck = '20120529'
benchmark = datetime.datetime.strptime(dateToCheck,"%Y%m%d")
print benchmark.date()
print datetime.date.today()
#if benchmark.date() > datetime.date.today() :
    #print "later"



            

