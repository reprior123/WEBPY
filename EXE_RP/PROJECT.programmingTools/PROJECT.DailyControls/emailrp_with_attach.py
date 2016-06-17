import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
test = path + 'test/'
pathSage = path + 'SageOut/'
#filetoattach = raw_input('Which file?: ')
#print 'you entered', filetoattach
tab = '\t'

filetoattach = sys.argv[1]

## emailer as attach happens here  ####
#!/usr/bin/python
import smtplib
server = 'smtp.gmail.com'
port = 587
recipient  = 'rob.prior@actant.com'
#recipient  = 'helen.Vollmann@actant.com'
sender = 'sffiles.alert@gmail.com'
password = 'actant123'
subject = 'Sending email through Gmail with Python'
body = 'blah blah blah'
"Sends an e-mail to the specified recipient."
body = "" + body + ""
headers = ["From: " + sender,
"Subject: " + subject,
"To: " + recipient,
"MIME-Version: 1.0",
"Content-Type: text/html"]

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = sender
gmail_pwd = password

def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   print os.path.basename
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

mail(recipient,
   "Hello from python RP!",
   "This is a auto email sent with python and contains file " + str(filetoattach),
    filetoattach)

