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
##import  rpu_rp, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
##import RulesEngine
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

from matplotlib import pyplot as plt

data = [range(n) for n in range(4,9)]
bla = range(4,9)
print bla
print data

for i, x in enumerate(data):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.pie(x, labels=x)

    fig.savefig("pie{0}.png".format(i))

    
def get_name_count(Names):
    if "Bob" in Names:
        NameList[0] +=1
    elif "Ann" in Names:
        NameList[1] +=1
    elif "Ron" in Names:
        NameList[2] +=1
    elif "Zee" in Names:
        NameList[3] +=1

def plot_dist(Values, Labels, Title):
    plt.title(Title)
    plt.pie(Values, labels = Labels, autopct='%0.0f%%', colors = ('g', 'r', 'y',  'c'))

NameList = [0]*4

##for Line in 'namesfile.txt':
##    for Names in Line:
##        get_name_count(Names)

####pp=PdfPages("myPDF.pdf")
####MyPlot = plt.figure(1, figsize=(5,5))
####Labels = ('Bob', 'Ann', 'Exon', 'Ron', 'Zee')
####Values = NameList
####
####plot_dist(Values, Labels, "Name Distribution")
####pp.savefig()
####plt.close()
####pp.close()

