import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, calendar, dateutil
############################
path = os.getcwd() + '/'
test = path + 'test/'
SageOut = path + 'SageOut/'
print path
drivelet = path[0]
datapath = drivelet + ':/'
print drivelet , path, datapath
sfarea = datapath + 'DATA/SFDATA/'
filedate = '20130120'
searchstring = 'SLA'
searchstring = raw_input('give search string  here: ')
#filedate = raw_input('give fdate here')
####################
path = os.getcwd() + '/'
drivelet = path[0] + ':/'
EXE = drivelet + 'EXE/'
DATA = drivelet + 'DATA/'
TMP = drivelet + 'TMP/'
print drivelet, path, EXE
pathSage = EXE + 'SageOut/'
pathSageF = EXE + 'SageFinancials/'
pathSageRaw = drivelet + 'FINANCE_ALL/8_INVOICING/SageRawDump/'
test = path + 'test/'
drivelet = path[0]
datapath = drivelet + ':/'
bconfig = path + 'billing_config_files/'
date_format = "%d-%m-%Y"
unix_format = "%Y%m%d"
#####################
today = datetime.date.today()
todayf = today.strftime(date_format)
todayfunix = today.strftime(unix_format)
todaystring = str(todayf)
todaystringunix = str(todayfunix)
todaystringunix = str(todayfunix)
#################################

##head in python
##with open("datafile") as myfile:
##    head=[myfile.next() for x in xrange(N)]
##print head
##Here's another way
##
##from itertools import islice
##with open("datafile") as myfile:
##    head=list(islice(myfile,N))
##print head


filetypes = ['Accounts', 'Opportunities', 'Assets', 'Contacts', 'Tasks', 'Emails']
alllines = 'bla'
blines = oneline = []
for filet in filetypes:
    inputfile =  sfarea + filedate[0:6] + '/' + filedate + '/' + filedate + '.sf.' + filet + '.csv'
    tempfile = TMP + filet
    os.system('head -1 ' + inputfile + ' > ' + tempfile)

    acctID = 'bla'
    printlines = 'bla'

    def csvToLines(justfilename):
        lines = []
        try:
            with open(justfilename, 'r') as afile:
                csvr = csv.reader( afile )
                for row in csvr:
                    if 'ID' in row:
                        lines.append( row )
        except StandardError:
            pass
        return lines

    lines = csvToLines(tempfile)
    acctID = sagecode = 'need'
    count =  count2 = 0
    for line in lines:
        count += 1
        if count == 1:
            numberfields = len(line)
            print  ' number of fields =',numberfields, filet
            for item in line:
                #print item, count2, filet
                alllines = alllines +  item +  '  ' + str(count2) + ' | '+ filet + '\n'
                count2 += 1
print '######'
#################
fname = SageOut   + 'acctidddnfo.csv'
outfile = open(fname, 'w')
outfile.write(alllines)
outfile.close()

outfile = open(fname, 'r')
#print outfile.readlines()
for line in outfile.readlines():
        if searchstring.upper() in str(line):
            print line
outfile.close()
filedate = raw_input('hit return to finish')

###################

