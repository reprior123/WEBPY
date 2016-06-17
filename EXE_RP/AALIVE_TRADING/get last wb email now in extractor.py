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
import  rpu_rp, glob, csv, subprocess, datetime, shutil, time
import imaplib, time, email
####################
import rpu_rp
######    ## see http://tools.ietf.org/html/rfc3501#section-6.4.5
######    messages = server.search(
######        ['FROM "brian.equities@gmail.com"', 'SINCE %s' % cutoff.strftime('%d-%b-%Y')])
######    response = server.fetch(messages, ['RFC822'])
######
######    for msgid, data in response.iteritems():
######        msg_string = data['RFC822']
######        msg = email.message_from_string(msg_string)
######        print 'ID %d: From: %s Date: %s' % (msgid, msg['From'], msg['date'])
########get_new_emails()
######    #####################
######
######    today = datetime.today()
######    cutoff = today - timedelta(days=1)
######    dt = cutoff.strftime('%d-%b-%Y')
########    typ, data = obj.search(None, '(SINCE %s) (FROM "mrtopstepgroup@gmail.com")'%(dt,))
######    typ, data = obj.search(None, '(SINCE %s)'%(dt,))
######    print data
####
####      msg = email.message_from_string(data[0][1])
####      print 'Message %s: %s' % (num, msg['Subject'])
####      print 'Raw Date:', msg['Date']
####      date_tuple = email.utils.parsedate_tz(msg['Date'])
####      if date_tuple:
####          local_date = datetime.datetime.fromtimestamp(
####              email.utils.mktime_tz(date_tuple))
####          print "Local Date:", \
####              local_date.strftime("%a, %d %b %Y %H:%M:%S")
#################################
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
myusername = 'reprior123@gmail.com'
mypassword =    'blaneed'
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(myusername, mypassword)
mail.list()
print mail.list()
mail.select("[Gmail]/All Mail") # connect to inbox.
searchterm = 'Fwd: William Blount observations'
f = '(HEADER Subject "' + searchterm + '")'
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
