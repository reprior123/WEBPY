
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, calendar, dateutil
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
##################################
todaydir = EXE + 'Invoice_output/Created_Invoices/' + todaystringunix
eudir = todaydir + '\US'
usdir = todaydir + '\EU'
htmldir = todaydir + '\html_olds'
print todaydir
if not os.path.exists(todaydir):
    os.makedirs(todaydir)
    os.makedirs(eudir)
    os.makedirs(usdir)
    os.makedirs(htmldir)
    #################################
prforce_area = 'Q:\P4Backup'

filetobackup = 'perforcefile'

    files to backup
    perforce_backups.ckp.????.gz
    perforce_backups.ckp.????.gz.md5
    perforce_backups.jnl.????.gz
    perforce_backup.txt
    log
    log-weekly


    builds to backup...
    


