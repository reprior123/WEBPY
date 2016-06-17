#! /usr/bin/env python
import urllib 
url = urllib.URLopener()
##resp = url.open('http://agenthost.com/myip.php')
ipserver = 'http://www.myipaddress.com/show-my-ip-address/'
##resp = url.open(ipserver)
##html = resp.readline()
html = '82.136.96.205'

######################
import os, sys
################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_RNR'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
print EXEnoslash
import HVARs, rputiles
#################

fromaddr = 'rob.prior@actant.com'
toaddrs  = ['addy1@gmail.com', 'someotheraddy@gmail.com']
msg = 'My IP is' + html + ' Right NOW!'

sender = 'rob.prior@actant.com'
recipient = 'reprior123@gmail.com'
senderpwd = 'xxxxxx'
subject ='IPaddre'
body = html
signaturefile = 'signaturefile.txt'

rputiles.gmail_NO_attachment(recipient, subject, body, sender, senderpwd, signaturefile)
  
