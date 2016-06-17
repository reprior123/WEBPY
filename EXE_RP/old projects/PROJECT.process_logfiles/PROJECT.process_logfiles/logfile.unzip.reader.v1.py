import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, zipfile
from pprint import pprint
path = os.getcwd() + '/'
drivelet = path[0]
print drivelet

searchstr = raw_input('give searchstri for target zip file here...: ')
searchstr = 'teveJIR_120907120916'
##SteveJIR_120917141246
##SteveJIR_120917131120
##SteveJIR_120907085751new

## list other arguments here like logfile repos, agelimit etic.

logfile_repos = 'C:/TS/'

for filen in (os.listdir(logfile_repos)):
    if '.zip' in filen and searchstr in filen:
            newfile = filen
print newfile
outfile = open(logfile_repos + 'target.log.txt', 'w')

file = zipfile.ZipFile(logfile_repos + newfile, "r")
# list filenames
for name in file.namelist():
    if '.log' in name:
        data = file.read(name)
        print name, len(data), repr(data[:10])
        outfile.write(data)
  
# list file information
for info in file.infolist():
    if '.log' in info.filename:
        print info.filename, info.date_time, info.file_size
