#

import os, sys, glob, csv, subprocess, datetime, shutil

today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
print todaystring

path = os.getcwd() + '/'    ### grabs current directory ##
print path
sfdata = path + 'DATA/SFDATA/201202/'
sfdata = path + 'DATA/SFDATA/'
filedate = '20120229'
sfdata = path + 'DATA/SFDATA/' + filedate + '/'
outfile = open(path + '/outfile.csv', 'w')

def csvToLines( csvfile ):
    csvr = csv.reader( csvfile )
    lines = []
    for row in csvr:
        lines.append( row )
    return lines

file = open(sfdata + filedate + '.sf.Assets.csv', 'r')

tempinputAcctfile = csv.writer(open(sfdata + '/temp.assetswdate.csv', 'wb'))
lines =  csvToLines (file)

for line in lines:
    status = line[17]
    lineplusdate = filedate + line
    if status != 'Expired':
        tempinputAcctfile.writerow(lineplusdate)
        print status
