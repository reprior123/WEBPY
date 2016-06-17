
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
path ='Z:/EXE/' 
test = path + 'test/'
print 'strting in ...'
print path
##############################
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
filedate = todaystring
month = '201202' 
#sfreal = path + 'DATA/SFDATA/'
sfreal = path + 'DATA/SFDATA/' + month + '/'
print sfreal
listing = os.listdir(sfreal)
print listing
outfilenew = open(path + 'countinfo.' + month + todaystring + '.out.txt','w')
datelist=[]
for file in listing:
    if '2012' in file and 'sf' in file:
        newname = file.replace('-','')
        daydir = newname[0:8]
        oldname = file 
        oldfile = os.path.join(sfreal, file)
        d = os.path.dirname(oldfile) + '/'+ daydir
        print d
        if not os.path.exists(d):
            os.makedirs(d)

        newfile = os.path.join(d, newname)
        print 'create daydir', daydir
        print oldfile
        print newfile
        shutil.move(oldfile, newfile)
