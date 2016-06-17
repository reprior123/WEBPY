import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp

EXE =  EXEnoslash + '/AALIVE_TRADING'
mainstem = 'C:/Users/bob/GDRIVE/MAIN DRIVE RP/'
maindir = mainstem +'memoirs'
outputtest =  maindir + '/outputtest/'
worddocs = outputtest +'samplefiles'
global stemdir
stemdir = 'C:/Users/bob/GDRIVE/MAIN DRIVE RP/'
##print EXE

import os, sys
import hashlib


import fnmatch, os, pythoncom, sys, win32com.client

wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")

print 'here'
def convertwords(maindir):
    try:
        for path, dirs, files in os.walk(maindir):
            for doc in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, '*.doc')]:
                print "processing %s" % doc
                wordapp.Documents.Open(doc)
                docastxt = doc.rstrip('doc') + 'txt'
                wordapp.ActiveDocument.SaveAs(docastxt, FileFormat=win32com.client.constants.wdFormatTextLineBreaks)
                wordapp.ActiveWindow.Close()
##                sleep(2)
    finally:
        pass
        wordapp.Quit()

convertwords(worddocs)
