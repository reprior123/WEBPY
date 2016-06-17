import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, difflib
import emaildifflines
############################
path = os.getcwd() + '/'
print path
#############################
from pprint import pprint
#########################################
path = os.getcwd() + '/'
drivelet = path[0] + ':/'
EXE = drivelet + 'EXE/'
DATA = drivelet + 'DATA/'
TMP = drivelet + 'TMP/'
print drivelet, path, EXE
projectarea = EXE + 'PROJECT.Backups/'
config = projectarea + 'config_sage/'
backuparea = DATA + 'backups/Backup_diff_check_reports/'
#######################################
bigstring = ''
debuglines = ''
forecasts = actuals = []
rootdir  = drivelet
maintag = 'FINANCE_ALL'
livedir = drivelet + maintag
##cs.nrp.newstyle.alltrans
##filein = open('cs.nrp.newstyle.alltrans.csv', 'r')
### 1. first do a nightly backup
### 2. run a dir listing on backup and live in the morning
### 3. email the report looking for large changes
### 4. run a noon and 15:00 dir report as well to keep track of work done [can be removed when smoothly running]
##can be run on any directory root...on backups, need to rename the root for the diff to work
##livedir = 'C:\BACKUP_AREA\FINANCE_ALL_20130514'
##livedir = 'C:/Documents and Settings/rob.prior/My Documents/Google Drive'

## toggle today and yesterday here  ##
from time import gmtime, strftime
timef = strftime("%H%M%S",gmtime())
import time
todayf = '20130517'
from datetime import datetime, timedelta
today = datetime.today()
todayf = today.strftime('%Y%m%d')
yesterdayf = '20130516'
yesterday = datetime.today() - timedelta(1)
yesterdayf = yesterday.strftime('%Y%m%d')

#### alternate yesterday for intraday check ####
##dirlisting = sorted((os.listdir(livedir)))
dirlisting = sorted((os.listdir(backuparea)))
for fname in dirlisting:
    if '.fnames.txt' in fname:
        yesterdayf = fname.split('.')[1]
############
todayfiles = backuparea + maintag + '.' + todayf + timef +'.fnames.txt'
todaydirs = backuparea +  maintag + '.' + todayf + timef +'.dirnames.txt'
yesterdayfiles =  backuparea + maintag + '.' + yesterdayf +'.fnames.txt'
yesterdaydirs = backuparea + maintag + '.' + yesterdayf + '.dirnames.txt'
##print 'today', todaydirs
##print 'yesterday', yesterdaydirs
##################### 
os.system('ls -R "' + livedir + '" > fdirs.txt') ## this is the fully recursive method ...takes longer
##os.system('ls  "' + livedir + '" > fdirs.txt')
filesarray = []
dirsarray = []
dirname = ''
fullname = ''
cleanline =''
fdirs = 'fdirs.txt'
fdirs_opened = open(fdirs, 'r')
#####################
for line in fdirs_opened.readlines():
    cleanline = line.strip()
##    print cleanline
    if '=:' in cleanline:      
        dirsarray.append(cleanline)
        dirname = cleanline
        fullname = dirname
    if '=:' not in cleanline:
        fullname = dirname + cleanline
    filesarray.append(fullname)
    ###############################
outfile_dirs = open(todaydirs, 'w')
for line in dirsarray: 
    outfile_dirs.writelines(line)
    outfile_dirs.writelines('\n')
outfile_dirs.close()
#########################
outfile_files = open(todayfiles, 'w')
for line in filesarray: 
    outfile_files.writelines(line)
    outfile_files.writelines('\n')
outfile_files.close()
#######
fdirs_opened.close()
###########   diff starts here  #######
oldsnapshot = yesterdayfiles
newsnapshot = todayfiles
#######
oldsnapshot = yesterdayfiles
newsnapshot = todayfiles
#diff oldsnapshot newsnapshot > reportfile
os.system('diff ' + oldsnapshot + ' ' + newsnapshot + ' > ' + backuparea + 'reportfile.' + todayf + timef + '.txt')
print 'diff ' + oldsnapshot + ' ' + newsnapshot + ' > ' + backuparea + 'reportfile.' + todayf + timef + '.txt'
#####
oldsnapshot = yesterdaydirs
newsnapshot = todaydirs
os.system('echo "directorys here ####################"  >> ' + backuparea + 'reportfile.' + todayf + timef + '.txt')
os.system('diff ' + oldsnapshot + ' ' + newsnapshot + ' >> ' + backuparea + 'reportfile.' + todayf + timef + '.txt')
##email reportfile
##then diff now to prev and send email
### maybe use this part later if redo the unix in python
### can also be adjusted to copy over files
##if os.path.isdir(today):
##    print 'do nothing'
##else:
####    shutil.copytree(livedir, today)
##    print ' would have copied here....'
####################################################
gmail_sender = 'sffiles.alert@gmail.com'
gmail_pwd = 'actant123'
att = backuparea + 'reportfile.' + todayf + timef + '.txt'
emaillist = ['bb;rob.prior@actant.com;' + att]
tab = '\t'
body = 'this is  a list of file changes in FINANCEALL last night'
subject = 'warning check diffs'

for line in emaillist:
   time.sleep(3)
   linesplit = line.split(';')
   sagecode = linesplit[0]
   filetoattach = linesplit[2]
   recipient = linesplit[1]
   print sagecode,recipient,filetoattach

   emaildifflines.mail(gmail_sender,gmail_pwd, recipient, subject, body, filetoattach)
###########################################################

import rputiles, read_daily_info
fileroot = '.ar.csv'
fieldcheck = 3
liners = read_daily_info.showlines(fileroot,fieldcheck)
#####################################
gmail_sender = 'sffiles.alert@gmail.com'
gmail_pwd = 'actant123'
att = projectarea + 'output.daily.csv'
emaillist = ['bb;rob.prior@actant.com;' + att]
tab = '\t'
body = 'this is  a list of AR  generated by project.backups/BackupGdocsDrive.py daily'
subject = 'AR list'

for line in emaillist:
   time.sleep(3)
   linesplit = line.split(';')
   sagecode = linesplit[0]
   filetoattach = linesplit[2]
   recipient = linesplit[1]
   print sagecode,recipient,filetoattach

   emaildifflines.mail(gmail_sender,gmail_pwd, recipient, subject, body, filetoattach)
###########################################################
fileroot = '.ap.csv'
fieldcheck = 3
liners = read_daily_info.showlines(fileroot,fieldcheck)
#####################################
gmail_sender = 'sffiles.alert@gmail.com'
gmail_pwd = 'actant123'
att = projectarea + 'output.daily.csv'
emaillist = ['bb;rob.prior@actant.com;' + att, 'bb;helen.vollmann@actant.com;' + att]
tab = '\t'
body = 'this is  a list of APs generated by project.backups/BackupGdocsDrive.py daily'
subject = 'AR list'

for line in emaillist:
   time.sleep(3)
   linesplit = line.split(';')
   sagecode = linesplit[0]
   filetoattach = linesplit[2]
   recipient = linesplit[1]
   print sagecode,recipient,filetoattach

   emaildifflines.mail(gmail_sender,gmail_pwd, recipient, subject, body, filetoattach)
###########################################################
## this is to test if can ls the directory with os.walk, remember output of walk is 3 items, root,dir, and fnames

##alldirs = os.walk(livedir)
##for root in alldirs:
##    print root[0]
#### this is to do a diff using python instead of unix...works...
##file1 = open('FINANCE_ALL.20130516.fnames.txt', 'r')
##file2 = open('FINANCE_ALL.20130515.fnames.txt', 'r')
####file1 = open('bla1.txt', 'r')
####file2 = open('bla2.txt', 'r')
##text1 = file1.readlines()
##text2 = file2.readlines()
####differbla = difflib.SequenceMatcher(None, file1.read(), file2.read())
####diffs = difflib.make_file(file1.read(), file2.read())
####print difflib.Differ(file1.read(), file2.read())
##d = difflib.Differ()
##result = list(d.compare(text1, text2))
##
##for line in result:
##    if '- Y:' in str(line) or '+ Y:' in str(line):
##        print line
##from pprint import pprint
##pprint(result)
##print result
##file1.close()
##file2.close()
##### endd of python differ code  ####
