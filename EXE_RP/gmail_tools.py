import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
###########################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################################
#############
yesterdayoffset = 1
from datetime import date, timedelta
today = datetime.date.today()
yesterday = datetime.date.today() - timedelta(yesterdayoffset)
todayf = today.strftime(date_format)
todayfunix = today.strftime(unix_format)

yesterdayf = yesterday.strftime(date_format)
yesterdayfunix = yesterday.strftime(unix_format)
todaydir = DATA + todayfunix
import datetime

## time functions ##
timenow = time.strftime(unixmin_format)
###################################################################################
def gmail_attachment(recipient, subject, body, attachment_fullpath, sender, senderpwd, ccnamelisttext):
    import smtplib
    server = 'smtp.gmail.com'
    port = 587
    headers = ["From: " + sender, subject, recipient,"MIME-Version: 1.0", "Content-Type: text/html"]
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
    sigfile=open(signaturefile, 'r')
    signature_text = sigfile.readlines()
    print signature_text
    sigfile.close()
    ###### now add these lines to body ####
    for line in signature_text:
        body = body + line
    body = body + ' '
    ########################
    server = 'smtp.gmail.com'
    port = 587
    headers = ["From: " + sender, subject, recipient, "MIME-Version: 1.0", "Content-Type: text/html"]
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
    msg['CC'] = 'finance@actant.com'
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
##gmail_NO_attachment('rob.prior@actant.com', 'testnew', 'testnewbody', 'rob.prior@actant.com', 'cxxxxxx', path +'rpsignaturefile.txt')
##########################################
