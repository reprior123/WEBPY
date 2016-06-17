import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, calendar, dateutil
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXE = rootpath + 'EXE/'   
EXEnoslash = rootpath + 'EXE'
sys.path[0:0] = [EXEnoslash] # sets sys directory for HVAR and rputile import
import HVARs
TMP = HVARs.TMP
invarea = TMP
targetarea = invarea + 'pdfouts/'

from os import walk
listoffiles = []
for (dirpath, dirnames, filenames) in walk(invarea):
    listoffiles.extend(filenames)
    break
#############################
for f in listoffiles:
    print f
    
fcount = 0
greptext = raw_input('enter text limiter for invoice to send here...: ')

for fileindivname in listoffiles:
    fcount += 1
    if fcount < 100:       
        if '.html' in fileindivname and greptext in fileindivname:        
            print fileindivname  ##   invbla = raw_input('send all invoices in '+ invarea + ' continue?')
            filetoattach = invarea + fileindivname   ### extract the sagecode from the filename ###
            targetfilename = targetarea + fileindivname + '.pdf'
            fullpathinfile = invarea + fileindivname
            print targetfilename
            pagesize = 'A4'
##            if cmode == 'US':
            pagesize = 'Letter'
##            pdferlocal = 'C:/Program Files(x86)/wkhtmltopdf/wkhtmltopdf.exe'
            pdferlocal = 'C:/wkhtmltopdf/wkhtmltopdf.exe'
            pdftmp = 'C:/wkhtmltopdf/tmp.pdf'
            pdfhtml ='C:/wkhtmltopdf/tmp.html'
            shutil.copy(fullpathinfile, pdfhtml)
            os.system(pdferlocal + ' -s ' + pagesize + ' ' + pdfhtml + ' ' + pdftmp  )
            shutil.copy(pdftmp, targetfilename )
            time.sleep(1)


