
def mail(gmail_sender, gmail_pwd, recipient, subject, text, attach):
   import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
   path = os.getcwd() + '/'
   test = path + 'test/'
   pathSage = path + 'SageOut/'

   from email.MIMEMultipart import MIMEMultipart
   from email.MIMEBase import MIMEBase
   from email.MIMEText import MIMEText
   from email import Encoders
   import os
   import smtplib
   #####################################
   msg = MIMEMultipart()
   msg['From'] = gmail_sender
   msg['To'] = recipient
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
   mailServer.login(gmail_sender, gmail_pwd)
   mailServer.sendmail(gmail_sender, recipient, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()
################################################################    
##gmail_sender = 'sffiles.alert@gmail.com'
##gmail_pwd = 'actant123'
##att = 'reportfile.20130516.txt'
##emaillist = ['bb rob.prior@actant.com ' + att,'bb reprior123@gmail.com ' + att]
##tab = '\t'
##invarea = 'Y:/EXE/'
##body = 'this is  a list of file changes in FINANCEALL last night'
##subject = 'warning check diffs'
##
##for line in emaillist:
##   print line
##   time.sleep(3)
##   linesplit = line.split()
##   sagecode = linesplit[0]
##   filetoattach = invarea + linesplit[2]
##   recipient = linesplit[1]
##   print sagecode,recipient,filetoattach
##
##   mail(gmail_sender,gmail_pwd, recipient, subject, body, filetoattach)






