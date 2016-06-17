import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
ypath ='Y:/'
print path
drivelet = path[0]
datapath = drivelet + ':/'
##############################
import re
rawf = 'rpblanoremove.txt'
FILE = path +rawf
f = open(FILE, 'w')

todayf = str(datetime.date.today().strftime('%Y%m%d'))
print todayf
filedate = todayf
monthtoday = todayf[0:6]
sfmonth = datapath + 'DATA/SFDATA/' + monthtoday + '/'
todaydir = sfmonth + todayf
todaylist = os.listdir(todaydir)

number_files = len(todaylist)

warnflag = 'safe'

if number_files < 16:
    print 'alert'
    f.write(str(todaylist))
    f.write(' WARNING not all files there..')
    warnflag = 'warn'

listsorted = (sorted(todaylist))

for filebla in listsorted:
    fsize = os.path.getsize(todaydir + '/' + filebla)
    if fsize < 10:
        f.write(' WARNING empty files detected')
        f.write(filebla)
        warnflag = 'warn'

f.close()

if warnflag == 'warn':
    os.system('emailrp_with_attach.py ' + rawf )
    os.system('email_fraser_with_attach.py ' + rawf )
    os.system('email_glen_with_attach.py ' + rawf )




