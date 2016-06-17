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
import  rpu_rp, Mod_rpInd
#TicksUtile, RP_Snapshot,
import glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
################
date = yesterday
import imaplib, time, email
####################
import rpu_rp
def multibody(email):
    b= email
##    b = email.message_from_string(a)
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = b.get_payload(decode=True)
    return body
####################################
def extract_wbmails(myusername,mypassword):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(myusername, mypassword)
    mail.list()
    print mail.list()
    mail.select("[Gmail]/All Mail") # connect to inbox.
    searchterm = 'Fwd: William Blount observations'
    frommts = '(HEADER From "info@mrtopstep.com")'
    frommts = '(HEADER Subject "Fwd: William Blount observations")'
##    f = '(HEADER Subject "' + searchterm + '")'
    f= frommts
    result, searchresultuids  = mail.uid('search', None, f)
    uidlist = (searchresultuids[0]).split()
    lastsinlist = uidlist[len(uidlist)-1]
    print lastsinlist
    for uid in [lastsinlist]:
        print uid
        result, data = mail.uid('fetch', uid, '(RFC822)')
        raw_email = data[0][1] # here's the body, which is raw text of the whole email including headers and alternate payloads
        ###################
        email_message = email.message_from_string(raw_email)
        toaddr =  email_message['To']
    ##    print toaddr
        print 'Raw Date:', email_message['Date']
        print email_message['From'],email_message['Subject'] 
        bla = multibody(email_message)
        rpu_rp.WriteStringsToFile('BlountNewEmail.txt',bla)


########################
username = 'reprior123@gmail.com'
mypassword = 'bla'
mypassword = raw_input('pw here: ')
extract_wbmails(username,mypassword)

##raw_input('remember to add weekly pivot...')
wbfile = 'BlountNewEmail.txt'
osCommandString = 'notepad.exe ' + wbfile 
##osCommandString = 'cat ' + wbfile 
##os.system(osCommandString)

######################
def convert_emailtolines():
    wbfile = downloads +'BlountNewEmail.txt'
    wbfile = 'BlountNewEmail.txt'

    lines = rpu_rp.TxtToLines(wbfile)
    full=[]
    readflag ='n'
    label = 'WBs_'
    prevline = []
    prevlabel = ''
    fullarray =[]
    for l in lines:
        rowarray =[]
        sline = ' '.join(l.split()).replace('MAX ','MAX').replace('TWO DAY','TWODAY')
        linelength = len(sline.split())
        b = sline
        c = sline.split()
        if 'Range Projections' in str(l):
            label = 'Range_'
        elif 'TVS' in str(l):
            label = 'TVS'
        elif 'TWODAY' in str(sline):
            label = 'TWODAY_'
        elif 'OPG' in str(l):
            label = 'prev_'
        else:
            pass   
        if 'JUNE 2016 contract' in str(l):
            readflag = 'y'
        if '*email*: info@mrtopstep.com' in str(l):
            readflag = 'n'
        if readflag == 'y' and linelength > 0:
            if len(c) == 1 and len(prevline) > 1 :
                if prevlabel == 'WBs_' or prevlabel == 'prev_':
                    dval = prevline[1]
                    wval = c[0]
                    maintag = prevlabel+prevline[0]
                    for dwtag in ['_DAY','_WEEK']:                     
                        tag = maintag+dwtag
                        if dwtag == '_DAY':                        
                            val = dval
                            pass
                        else:
                            val = wval
                        if val != 'DAILY':
                            rowarray=[val,tag]
                            fullarray.append(rowarray)     
                        #########
                if prevlabel == 'Range_':
                    rangedesc = prevline[1]
                    for rangetag in ['Low_','Hi__']:
                        for dwtag in ['_DAY','_WEEK']:
                            if  rangetag == 'Low_' and dwtag == '_DAY':
                                val = prevline[0].split('-')[0]                            
                            if  rangetag == 'Hi__' and dwtag == '_DAY'   :                 
                                val = prevline[0].split('-')[1]                                     
                            if rangetag == 'Low_' and dwtag == '_WEEK':
                                val = c[0].split('-')[0]
                            if rangetag == 'Hi__' and dwtag == '_WEEK':
                                val = c[0].split('-')[1]
##                            if 'alternate' not in rangedesc:
                            rowarray=[val,prevlabel+rangetag+rangedesc +dwtag]
                            fullarray.append(rowarray)                      
                    ##############################           
            if len(c) > 1 and len(prevline) > 1 and prevlabel == 'TWODAY_':
                dvallow = prevline[0].split('-')[0]
                dvalhii = prevline[0].split('-')[1]
                rangedesc = prevline[1]
                
                wval = c[0]
                tag = prevlabel+'Low_'+rangedesc +'_2DAY\n'
                val = dvallow
                rowarray=[val,tag]
                fullarray.append(rowarray)
                
                tag = prevlabel+'Hi__'+rangedesc +'_2DAY\n'
                val = dvalhii
                rowarray=[val,tag]
                fullarray.append(rowarray)
                
            prevline = c
            prevlabel = label

    fname = libarea + 'SpotsWBDaily.ES.txt'
    rpu_rp.WriteArrayToCsvfile(fname,fullarray)
#############################
print ' need to get the email first....!!!!'
convert_emailtolines()
############################
def create_dailypivots(sym):
    pivot = round(float(Mod_rpInd.gatherline(sym,'pivot')[1]),1)
    R1 = round(float(Mod_rpInd.gatherline(sym,'R1')[1]),1)
    S1 = round(float(Mod_rpInd.gatherline(sym,'S1')[1]),1)
    S2 = round(float(Mod_rpInd.gatherline(sym,'S2')[1]),1)
    R2 = round(float(Mod_rpInd.gatherline(sym,'R2')[1]),1)
##    print S1,R1,pivot
    ##do the same for weekly by adding dur to variables and create a weekly  from dailys..
##    find pivots, find fibbo retraces on recnt moves[rangebars,hi,lo]
##    calculate 10 handles off high of day,lowday,openday,yestclose,prevhourhilow
    outfile = libarea +'SpotsAutopivot.' + sym +'.txt'
    itemlist = [pivot,R1,S1,S2,R2]
    itemlisttags = ['pivotRP','R1rp','S1rp','S2rp','R2rp']
    lines=[]
    c=0
    for item in itemlist:
        tag = itemlisttags[c]
        c+=1
        line=[]
        line.append(item)
        line.append(tag)
        lines.append(line)      
    for line in lines:
        print line
    rpu_rp.WriteArrayToCsvfile(outfile,lines)
##############
create_dailypivots('ES')
create_dailypivots('FDAX')
###########################
def create_roundie(centerprice,increment,loopnum,sym):
    outfile = libarea +'SpotsRoundies.' + sym +'.txt'
##    print outfile
    i=0
    lines=[]
    while i < 10:
        i+=1
        line=[]
        up = centerprice + (i*increment)
        down = centerprice - (i*increment)
    ##    print centerprice,up,down
        line.append(up)
        line.append('roundie')
        lines.append(line)
        line=[]
        line.append(down)
        line.append('roundie')
        lines.append(line)
    for line in lines:
        print line
    rpu_rp.WriteArrayToCsvfile(outfile,lines)
##############
centerprice = 1900
increment = 10
loopnum = 10
sym = 'ES'
create_roundie(centerprice,increment,loopnum,sym)
###############
centerprice = 9750
increment = 50
loopnum = 10
sym = 'FDAX'
create_roundie(centerprice,increment,loopnum,sym)
############
start = '01:00:05'
end   = '20:58:05'

sym ='ES'
##raw_input('remember to add weekly pivot...')
wbfile = libarea +'SpotsWBDaily.' + sym +'.txt'
##osCommandString = 'notepad.exe ' + wbfile 
##os.system(osCommandString)

###
##raw_input('remember to addnew spots...')
wbfile = libarea +'SpotsFull.' + sym +'.txt'
##osCommandString = 'notepad.exe ' + wbfile 
##os.system(osCommandString)


osCommandString = 'notepad.exe ' + wbfile 
##osCommandString = 'cat ' + wbfile 
os.system(osCommandString)
