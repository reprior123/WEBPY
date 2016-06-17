
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
drive = 'Y:/' 
test = path + 'test/'
#######
#for firm in ['2_AGZUG', '4_INC', '3_LTD']:
for firm in ['2_AGZUG']:
    #firm = '2_AGZUG'
    financeall = drive + 'FINANCE_ALL/'
    finance = financeall + firm + '/SCAN DOCS RECEIVED/INVOICES'

    print os.listdir(financeall)

    ##finance = drive + 'FINANCE_ALL'

    listing = os.listdir(finance)
    #print listing

    def listFiles(dir):
        basedir = dir
        #print "Files in ", os.path.abspath(dir), ": "
        print 'Files in  ', dir, ':' 
        subdirlist = []
        contents = os.listdir(dir)
        for item in sorted(contents) :
            if os.path.isfile(dir + '/' + item):
                if '2' in item:
                    print item
            else:
                subdirlist.append(os.path.join(basedir, item))
        for subdir in subdirlist:
            listFiles(subdir)
            bla = raw_input('ok')

    listFiles(finance)
    bla = raw_input('ok')

