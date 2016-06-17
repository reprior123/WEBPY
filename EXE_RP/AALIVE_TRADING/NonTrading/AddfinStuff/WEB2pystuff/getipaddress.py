import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp,  glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
import ctypes
################
date = today
###
from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()
print my_ip

import rpu2
recipient = 'reprior123@gmail.com'
sender = recipient
subject = 'ipaddre'
body = my_ip
senderpwd = 'bla'
signaturefile = EXE + 'exe.bat'
rpu2.gmail_NO_attachment(recipient, subject, body, sender, senderpwd, signaturefile)
