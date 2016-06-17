import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
############################
path = os.getcwd() + '/'
test = path + 'test/'
SageOut = path + 'SageOut/'
drivelet = path[0]
datapath = drivelet + ':/'
print drivelet , path, datapath
TMP = datapath + 'TMP/'
#########
sfarea = datapath + 'DATA/SFDATA/'
##############################
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
filedate = todaystring
 
maininvoices = datapath + 'FINANCE_ALL/4_INC/Scanned Document - Incoming/INVOICES/'
needapprove =  maininvoices +'03.Checked_by_Orderer_Ready_to_be_Approved/'
approved = maininvoices + '05.Approved_Awaiting_Payment/'


listing = os.listdir(needapprove)
print needapprove
for item in listing :
    print item
print "-------"
listing = os.listdir(approved)
print approved
for item in listing :
    print item

##outfilenew = open(path + 'countinfo.' + month + todaystring + '.out.txt','w')
##datelist=[]
##for file in listing:
##    if '2012' in file and 'sf' in file:
##        newname = file.replace('-','')
##        daydir = newname[0:8]
##        oldname = file 
##        oldfile = os.path.join(sfreal, file)
##        d = os.path.dirname(oldfile) + '/'+ daydir
##        print d
##        if not os.path.exists(d):
##            os.makedirs(d)
##
##        newfile = os.path.join(d, newname)
##        print 'create daydir', daydir
##        print oldfile
##        print newfile
##        shutil.move(oldfile, newfile)
