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
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
'''	 	
Have you tried conn.search(None, 'ALL') to get all the messages? – theodox Feb 25 '13 at 21:00
yes, i updated the code snippet to make it clear that 'status' was set to 'ALL' – vgoklani Feb 25 '13 at 21:03
You might try using conn.search() instead of conn.uid(). You'll get indices rather than uids,
but you can get the uid when you fetch the message.'''
####################
##The IMAP protocol document is absoutely key to understanding the commands available, but let me skip attempting to
##explain and just lead by example where I can point out the common gotchas I ran into.
import rpu_rp


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})
file1.SetContentString('Hello')
file1.Upload() # Files.insert()

file1['title'] = 'HelloWorld.txt'  # Change title of the file
file1.Upload() # Files.patch()

content = file1.GetContentString()  # 'Hello'
file1.SetContentString(content+' World!')  # 'Hello World!'
file1.Upload() # Files.update()

file2 = drive.CreateFile()
file2.SetContentFile('hello.png')
file2.Upload()
print 'Created file %s with mimeType %s' % (file2['title'], file2['mimeType'])
# Created file hello.png with mimeType image/png

file3 = drive.CreateFile({'id': file2['id']})
print 'Downloading file %s from Google Drive' % file3['title'] # 'hello.png'
file3.GetContentFile('world.png')  # Save Drive file as a local file

# or download Google Docs files in an export format provided.
# downloading a docs document as an html file:
docsfile.GetContentFile('test.html', mimetype='text/html')
