################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
############
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
##import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot,BarUtiles,RulesEngine
import glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime, date, timedelta
import ctypes
import zipfile,openpyxl 
import datetime
## time functions ##
timenow = time.strftime(unixmin_format)

import rpu_rp
###########################################
def create_header_importsage_file(filename):
    clarrayline = []
    Type = 'Type'
    NominalAcRef = 'Nominal'
    DepartCode = 'Depart Code'
    Sagecode = 'Account'
    Reference = 'Reference'
    ExtraReference = 'Extra Reference' 
    TaxCode = 'Tax Code'
    NetAmount = 'Net Amount'
    TaxAmount = 'Tax Amount'
    TotalInvoicedAmount = 'TotalInvoicedAmount'
    Details = 'Details'
    Date = 'Date'
    CURR = 'CURR'
    UserName = 'UserName'
    blankf = 'blank'
    ExchangeRate = 'Exchange Rate' 
    itemlist = [Type, NominalAcRef, DepartCode, Sagecode, Reference, ExtraReference,\
    TaxCode, NetAmount, TaxAmount, TotalInvoicedAmount, Details,\
    Date, CURR, UserName, blankf, ExchangeRate]
    for item in itemlist:
        clarrayline.append(item)
    cfilenew = open(filename, 'wb')
    spamwriter = csv.writer(cfilenew)
    spamwriter.writerow(clarrayline)
    cfilenew.close()
##############   end of header  ########
def gmail_attachment(recipient, subject, body, attachment_fullpath, sender, senderpwd, ccnamelisttext):
    import smtplib
    server = 'smtp.gmail.com'
    port = 587
    headers = ["From: " + sender, subject, recipient,
    "MIME-Version: 1.0",
    "Content-Type: text/html"]
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    import os
    gmail_user = sender
    gmail_pwd = senderpwd
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Cc'] = ccnamelisttext
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_fullpath, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attachment_fullpath))
    if attachment_fullpath == 'noattach':
        print "no attachment, now sending...."
    else:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment_fullpath, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attachment_fullpath))
        msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    ##    mailServer.sendmail(gmail_user, recipient, msg.as_string())
    mailServer.sendmail(gmail_user, msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
###########################
##This bit explains how to add cc style email lists. to be used by autoemailer  !!!!  
##The problem seems to be that the email.Message module expects something different than the smtplib.sendmail() function.
##In short, to send to multiple recipients you should set the header to be a string of comma delimited email addresses.
##The sendmail() parameter to_addrs however should be a list of email addresses.
##msg["To"] = "malcom@example.com,reynolds@example.com,firefly@example.com"
##msg["Cc"] = "serenity@example.com,inara@example.com"
###########################
def gmail_NO_attachment(recipient, subject, body, sender, senderpwd, signaturefile):
    import smtplib
    #####
########    sigfile=open(signaturefile, 'r')
########    signature_text = ['xx']#sigfile.readlines()
########    sigfile.close()
########    ###### now add these lines to body ####
########    for line in signature_text:
########        body = body + line
    body = body + ' '
    ########################
    server = 'smtp.gmail.com'
    port = 587
    headers = ["From: " + sender, subject, recipient,\
               "MIME-Version: 1.0", "Content-Type: text/html"]
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email import Encoders
    import os
    gmail_user = sender
    gmail_pwd = senderpwd
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['CC'] = 'reprior123@gmail.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
##    part = MIMEBase('application', 'octet-stream')
##    part.set_payload(open(attachment_fullpath, 'rb').read())
##    Encoders.encode_base64(part)
##    part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attachment_fullpath))
    print os.path.basename
##    msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, recipient, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
##########################################
def bank_statements():
    bankarea = DATA 
    from os import listdir
    files  = os.listdir(bankarea)
    lines =[]
    for f in files:
        fname =bankarea + f
        if 'UBS' and 'csv' in f:
            lines += rputiles.csvToLines(fname)
            allines = lines.sorted()
#########################
            #################
def catcsv(justfilename):
    lines = []
    try:
        lines = CsvToLines(justfilename)  
    except:
        print 'could not read ' + str(justfilename) + ' for csvToLines in rputiles'
    for line in lines:
        print line
#################
def cattxt(justfilename):
    lines = []
    with open(justfilename, 'r') as afile:
        try:
    ##        with open(justfilename, 'r') as afile:
            lines = afile.readlines()
        except:
            print 'could not read ' + str(justfilename) + ' for csvToLines in rputiles'
        for line in lines:
            print line
######
##############################################
def ShowDirList(maindirectorynoSlash):
    print maindirectorynoSlash
    path  = maindirectorynoSlash
    import os
    rootDir = path
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('%s' % dirName,'\t%s'  %fname)

##    for maindirectorynoSlash, dirs, files in os.walk("."):
##        for name in files:
##            print(os.path.join(maindirectorynoSlash, name))
##        for name in dirs:
##            print(os.path.join(maindirectorynoSlash, name))   
##    from os.path import join, getsize, isfile, isdir, splitext
##    def GetFolderSize(maindirectorynoSlash):
##        TotalSize = 0
##        for item in os.walk(path):
##            for file in item[2]:
##                try:
##                    TotalSize = TotalSize + getsize(join(item[0], file))
##                except:
##                    print("error with file:  " + join(item[0], file))
##        return TotalSize
##    print(float(GetFolderSize("C:\\")) /1024 /1024 /1024)  
