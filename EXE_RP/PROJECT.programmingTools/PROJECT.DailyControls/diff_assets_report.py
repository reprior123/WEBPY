
import os, sys, glob, csv, subprocess, datetime, shutil, difflib
#from difflib_data import *
path = os.getcwd() + '/'
test = path + 'test/'
print path
##############################
todaystring = str(datetime.date.today().strftime('%Y%m%d'))
################################  hard coded text lines   ################
sfreal = path + 'DATA/SFDATA/'
searchdate = '201203'
month = searchdate[0:6]
sfmonth = sfreal + '/' + month + '/'
ysfmonth = sfreal + '/' + ymonth + '/'
listing = os.listdir(sfmonth)
#print listing

ftypes = ['assets', 'accounts', 'products', 'contacts']
for ftype in ftypes:
    datelist=[]
    dcount = 0
    for date in listing:
        dcount += 1
        if '2012' in date and dcount < 2:
            ydate = date
        if '2012' in date and dcount < 6:
            ymonth = month = date[0:6]
            print date, ydate
            sfdatefile1 = sfmonth + '/' + date + '/' + date + '.sf.' + ftype + '.csv' 
            sfdatefiley = ysfmonth + '/' + ydate + '/' + ydate + '.sf.' + ftype + '.csv'
            outputfile = path + 'diffs.' + date + '.' + ydate + '.' + ftype + '.txt'
            program = path + "diffviabat.bat"
            subprocess.call([program, sfdatefile1, sfdatefiley, outputfile])
            outfile = open(outputfile, 'r')
            print len(outfile.readlines())
            outfile.close()
            ydate = date
            ymonth = ydate[0:6]
            ysfmonth = sfreal + '/' + ymonth + '/'
