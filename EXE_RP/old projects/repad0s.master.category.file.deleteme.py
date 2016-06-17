import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
from pprint import pprint
path = os.getcwd() + '/'
drivelet = path[0]
print drivelet

fnames = ['category.master.csv', 'category.master.newcats.csv']
for fname in fnames:
    
    pathSageF = path + 'SageFinancials/'
    os.system('cp '+ pathSageF + fname + ' ' + pathSageF +  fname + '.older')
    infile = open(pathSageF + fname, 'r')

    alllines=''
    for line in infile.readlines():
        nomcode = line.split(',')[0]
        cat = line.split(',')[1]
        cat1 = line.split(',')[2]
        cat2 = line.split(',')[3]
        cat3 = line.split(',')[4]
        firm = (line.split(',')[5]).strip()
        pad =''
        if len(nomcode) < 4:
            pad = '0'
        if len(nomcode) < 3:
            pad = '00'
        if len(nomcode) < 2:
            pad = '000'
        alllines += (pad+nomcode+','+cat+','+cat1+','+cat2+','+cat3+','+firm+',\n')
    infile.close()
    newfile = open(pathSageF + fname, 'w')
    newfile.write(alllines)
    newfile.close()
