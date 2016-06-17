import shutil, os, errno, csv, subprocess, filecmp
from datetime import datetime, timedelta
#yesterday = date.today() - timedelta(1)

path = os.getcwd() + '\\'
today = datetime.today()
yesterday = datetime.today() - timedelta(1)
todayf = today.strftime('%Y%m%d')
yesterdayf = yesterday.strftime('%Y%m%d')

print todayf, "bla", yesterdayf

#####   COPY TO Y:\ DRIVE   #####

filedate = todayf
monthtoday = todayf[0:6]
SfArea = path + 'DATA\\'
SourceToday = SfArea + 'SFDATA\\' + monthtoday + '\\' + todayf + '\\'
TodayFile = SourceToday + todayf + '.sf.Opportunities.csv'
SourceYesterday = SfArea + 'SFDATA\\' + monthtoday + '\\' + yesterdayf + '\\'
YesterdayFile = SourceYesterday + yesterdayf + '.sf.Opportunities.csv'
abct = SfArea + 'Comparison\\' + monthtoday + '\\' + todayf

try:
    os.makedirs(abct)
except OSError, e:
    if e.errno != errno.EEXIST:
        raise


shutil.copy(TodayFile, abct)
shutil.copy(YesterdayFile, abct)

########################################### GRABBING PROPER OPPORTUNITY FIELDS
OppfileToday = open(abct + '\\' + todayf + '.sf.Opportunities.csv', 'r')

def csvOppsToLines():
    csvr = csv.reader( OppfileToday )
    accountlines = []
    for row in csvr:
        accountlines.append( row )
    return accountlines
OpplinesToday =  csvOppsToLines ()
bla  = ' '
############################################### TODAY
for line in OpplinesToday:
    count = 0
    name = line[5]
    stage = line[7]
    type = line[13]
    closeDate = line[12]
    amount = line[8]
    nextSteps = line[42]
    blockers = line[54]
    #print name, stage, type, closeDate, amount, nextSteps, blockers
    LineItemHeader = 'Name' + ',' + 'Stage' + ',' 'Type' + ',' + 'Close Date' + ',' + 'Amount' + ','  + 'Next Steps' + ',' + 'Blockers'
    #Content = line[5] + ',' + line[7] + ',' + line[13] + ',' + line[12] + ',' + line[8] + ',' + line[42] + ',' + line[54]
    Content = name + ',' + stage + ',' + type + ',' + closeDate + ',' + amount + ',' #+ nextSteps + ',' + blockers
    format = "%9s, %9s, %9s, %9s, %s\n"
    bla = bla + Content + (format % (name, stage, type, closeDate, amount))
print bla

outfilename = path + 'DATA\Comparison\Opps.today.short.csv'
outfile = open(outfilename, 'w')
#outfile.write(LineItemHeader)
outfile.write(bla)
outfile.close()

############################################### YESTERDAY
OppfileYesterday = open(abct + '\\' + yesterdayf + '.sf.Opportunities.csv', 'r')

def csvOppsToLines():
    csvr = csv.reader( OppfileYesterday )
    accountlines = []
    for row in csvr:
        accountlines.append( row )
    return accountlines
OpplinesYesterday =  csvOppsToLines ()
bla  = ' '
#######################################
for line in OpplinesYesterday:
    count = 0
    name = line[5]
    stage = line[7]
    type = line[13]
    closeDate = line[12]
    amount = line[8]
    nextSteps = line[42]
    blockers = line[54]
    #print name, stage, type, closeDate, amount, nextSteps, blockers
    LineItemHeader = 'Name' + ',' + 'Stage' + ',' 'Type' + ',' + 'Close Date' + ',' + 'Amount' + ','  + 'Next Steps' + ',' + 'Blockers'
    #Content = line[5] + ',' + line[7] + ',' + line[13] + ',' + line[12] + ',' + line[8] + ',' + line[42] + ',' + line[54]
    Content = name + ',' + stage + ',' + type + ',' + closeDate + ',' + amount + ',' #+ nextSteps + ',' + blockers
    format = "%9s, %9s, %9s, %9s, %s\n"
    bla = bla + Content + (format % (name, stage, type, closeDate, amount))
print bla

outfilename2 = path + 'DATA\Comparison\Opps.yesterday.short.csv'
outfile = open(outfilename2, 'w')
#outfile.write(LineItemHeader)
outfile.write(bla)
outfile.close()



############## Determine the items that exist in both directories
os.chdir(path + "DATA\Comparison\\")
os.system("diff2files.bat")
print "batch file has been run"

logPrimary = path + "DATA\Comparison\\"
logFile = path + "DATA\Comparison\log.txt"
logDestination = logPrimary + "Differences" + "\\" + "differences from " + todayf + ".txt"
shutil.copy(logFile, logDestination)
OppsToRemoveT = path + "DATA\Comparison\Opps.today.short.csv"
OppsToRemoveY = path + "DATA\Comparison\Opps.yesterday.short.csv"
os.remove(logFile)
os.remove(OppsToRemoveT)
os.remove(OppsToRemoveY)