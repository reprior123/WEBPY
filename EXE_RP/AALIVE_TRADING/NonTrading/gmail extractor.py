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
##############

myusername = 'reprior123@gmail.com'
mypassword =    'xxxxxxx'
import imaplib, time, os, sys
##from __future__ import division
##LOGGING IN TO THE INBOX
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(myusername, mypassword)
mail.list()

# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.
##GETTING ALL MAIL AND FETCHING THE LATEST
##Let’s start by searching our inbox for all mail with the search function.
##Use the built in keyword “ALL” to get all results (documented in RFC3501).
##We’re going to extract the data we need from the response, then fetch the mail via the ID we just received.

## working from basic full fetch
##########result, data = mail.search(None, "ALL")
##########ids = data[0] # data is a list.
##########print len(data),'is num of emails got'
##########id_list = ids.split() # ids is a space separated string
##########lenidlist = len(id_list)
##########print lenidlist
##########latest_email_id = id_list[lenidlist-1] # get the latest
##########result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

####Luckily we can ask the imap server to return a UID (unique id) instead.
## working from a searched uid list
searchterm = "Fwd: William Blount observations"
##result, data = mail.uid('search', None, "ALL") # search and return uids instead
result, searchresultuidliststring = mail.uid('search', None, '(HEADER Subject "Fwd: William Blount observations")')
searchresultuidlist = (searchresultuidliststring[0]).split()
lastinlist = searchresultuidlist[len(searchresultuidlist)-1]
print searchresultuidlist
for searchresultuid in searchresultuidlist:
    print searchresultuid

##    result, data = mail.fetch(searchresultuid, "(RFC822)") # fetch the email body (RFC822) for the given ID
    result, data = mail.uid('fetch', searchresultuid, '(RFC822)')
    ### or can use the uid to directly fetch without the fetch command

    # in both cases
    raw_email = data[0][1] # here's the body, which is raw text of the whole email including headers and alternate payloads
    ###################
    ####USING UIDS INSTEAD OF VOLATILE SEQUENTIAL IDS
    ####The imap search function returns a sequential id, meaning id 5 is the 5th email in your inbox.
    ####That means if a user deletes email 10, all emails above email 10 are now pointing to the wrong email.
    '''
    PARSING RAW EMAILS'''

    import email
    email_message = email.message_from_string(raw_email)
    toaddr =  email_message['To']
    print toaddr
    print email_message['From']
    print email_message['Subject']

##    b = email_message
##    if b.is_multipart():
##        for payload in b.get_payload():
##            # if payload.is_multipart(): ...
##            print payload.get_payload()
##        else:
##            print b.get_payload()
    
    bla = multibody(email_message)
    rpu_rp.WriteStringsToFile('bbb.txt',bla)
    print bla
##    for ll in bla:
##        print ll
##        print bla

##print email.utils.parseaddr(toaddr) 
####    for body in email_message.items():
####        print '####'
####        print body  # print all headers
# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)

############def get_first_text_block(self, email_message_instance):
############    maintype = email_message_instance.get_content_maintype()
############    if maintype == 'multipart':
############        for part in email_message_instance.get_payload():
############            if part.get_content_maintype() == 'text':
############                return part.get_payload()
############    elif maintype == 'text':
############        return email_message_instance.get_payload()
##################
############email_message_instance = raw_email
############get_first_text_block(get_first_text_block, email_message_instance)
############

'''
ADVANCED SEARCHES
We’ve only done the basic search for “ALL”.
Let’s try something else such as a combination of searches we want and don’t want.
All available search parameters are listed in the IMAP protocol documentation and
you will definitely want to check out the SEARCH Command reference.

Search any header

For searching any headers, such as the subject, Reply-To, Received, etc., the command is simply “(HEADER “”)”
mail.uid('search', None, '(HEADER Subject "My Search Term")')
mail.uid('search', None, '(HEADER Received "localhost")')
Search for emails since in the past day
Often times the inbox is too large and IMAP doesn’t specify a way of limiting results,
resulting in extremely slow searches. One way to limit is to use the SENTSINCE keyword.
The SENTSINCE date format is DD-Jun-YYYY. In python, that would be strftime(‘%d-%b-%Y’).

date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))

Limit by date, search for a subject, and exclude a sender
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date} HEADER Subject "My Subject" NOT FROM "yuji@grovemade.com")'.format(date=date))

FETCHES
Get Gmail thread ID
Fetches can include the entire email body, or any combination of results such as email flags
(seen/unseen) or gmail specific IDs such as thread ids.

result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')

Get a header key only
result, data = mail.uid('fetch', uid, '(BODY[HEADER.FIELDS (DATE SUBJECT)]])')

FETCH MULTIPLE
You can fetch multiple emails at once. I found through experimentation that it’s expecting comma delimited input.
result, data = mail.uid('fetch', '1938,2398,2487', '(X-GM-THRID X-GM-MSGID)')

USE A REGEX TO PARSE FETCH RESULTS
The returned result isn’t very easy to swallow. They are space separated key-value pairs.

Use a simple regex to get the data you need.
import re
result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')
re.search('X-GM-THRID (?P<X-GM-THRID>\d+) X-GM-MSGID (?P<X-GM-MSGID>\d+)', data[0]).groupdict()
# this becomes an organizational lifesaver once you have many results returned.
'''
###################
###############
'''
However I also use python (partly because that's what getmail is written in)
to do a number of other tasks. For example, I have some code that, each day,
looks for the oldest task in my inbox and adds it to a text file. Then
I have some more code that checks the inbox at noon to see if it's still there
- if the task is still there then it sends me a warning message...
The (fairly hacky, I'm not naturally a python programmer) code for this looks like
#Big problem with this is if tasks are in the list twice (two 'drink 1l water' f
or example) the current code checks *anywhere* in the inbox, not just at the bot
tom'''
########################
def findTask(filename):
    file = open(filename)
    line = file.readline()[33:]
    lastTask=""
    while line:
        lastTask=line
        line=file.readline()
#       print line
 #       print "and now" 
  #      print line
    return lastTask[33:]
########################
def processFile(filename,targettask):
    file = open(filename)
    line = file.readline()[33:]
    while line:
#       print line
            #print number
 #           print "line", line
 #           print "lastline",lastline
        if line.strip()==targettask.strip():
            print "WARNING!!!!!!"
            os.system('echo '+line.strip()+' > email.txt')
            os.system('/bin/mail -s "WARNING!!! OLDEST TASK ACTIVE:" "joe.reddington@gmail.com" < "email.txt"')
            os.system(' rm email.txt')
            sys.exit()
            line=file.readline()
########task=findTask("/home/pgrads/joseph/emailAnalysis/resultsOldest.txt")
########print task
########processFile("/home/pgrads/joseph/emailAnalysis/subjects.txt", task)
##########################
'''
But you can certainly see how I
can use the combination of gmail, getmail,
and python to search for emails of a particular
type and perform some extra action - for example
I have a bit of python that downloads all the sms
messages that arrive in my inbox (I use http://
ifoward.com/
to get them to my inbox) and puts them in a database file for archiving.'''
##################################################
import imaplib, email, base64
def fetch_messages(username, password):
    messages = []
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(username, password)
    conn.select()
    typ, data = conn.uid('search', None, 'ALL')

    for num in data[0].split():
        typ, msg_data = conn.uid('fetch', num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                messages.append(email.message_from_string(response_part[1]))
        typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
    return messages
##fetch_messages('rob.prior@royalblueit.ch','smile123')
#############################'''
