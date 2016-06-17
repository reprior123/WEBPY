
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
ypath ='Y:/'
print path
##############################

##########################
todayf = str(datetime.date.today().strftime('%Y%m%d'))
print todayf
todayf = '20120413'
filedate = todayf
monthtoday = todayf[0:6]

sfmonth = ypath + 'DATA/SFDATA/' + monthtoday + '/'
todaydir = sfmonth + todayf
todaylist = os.listdir(todaydir)
print todaylist
print sfmonth
listing = os.listdir(sfmonth)
print listing
listsorted = (sorted(listing))

#listsorted = ['20120410']  #### this line ws in for testing...take it out to work on latest file

lastnum =  len(listsorted)
def listFiles(dir):
    basedir = dir
    print 'Files in  ', dir, ':'
    subdirlist = []
    contents = os.listdir(dir)
    for item in sorted(contents) :
        if os.path.isfile(dir + '/' + item):
            print item
        else:
            subdirlist.append(os.path.join(basedir, item))
    for subdir in subdirlist:
        listFiles(subdir)
dcount = 0
for newdir in listsorted:
    dcount +=1
    if dcount == lastnum:
        print newdir
        fulldir = sfmonth + newdir
        listoffiles = listFiles(fulldir)
        if listoffiles < 2:
            print "warning!!! and send email here...."
            #######!/usr/bin/python
            import smtplib
            pword = 'actant123'
            server = 'smtp.gmail.com'
            port = 587
            recipient  = 'rob.prior@actant.com'
            sender = 'reports@actant.com.test-google-a.com'
            sender = 'sffiles.alert@gmail.com'
            subject = 'Warning...Warning....SF routine did not run properly'
            body = 'warning...sf files not here yet today...'
            "Sends an e-mail to the specified recipient."
            body = "" + body + ""
            headers = ["From: " + sender,
            "Subject: " + subject,
            "To: " + recipient,
            "MIME-Version: 1.0",
            "Content-Type: text/html"]
            headers = "\r\n".join(headers)
            session = smtplib.SMTP(server, port)
            session.ehlo()
            session.starttls()
            session.ehlo
            #session.login(sender, 'pword')
            session.login(sender, 'actant123')
            session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
            session.quit()
            print 'done'

