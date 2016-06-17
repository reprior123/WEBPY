# grab the lines from logfile = complete or fired and pairt them together
# create a file with all trades = handleOLT
# count hits and partial fills and misses between the two
# lookup in time and sales what traded compared with misses, partials etc.
# lookup in enhanced time and sales and see the prices which triggered to determine how good they were

import os, sys, glob,zipfile
path = os.getcwd() + '/'    ### grabs current directory ##
#data = 'V:/Salesforce Cases/2012/Kyte Group - Atlantic Trading Indexes/00020532/'
datanino = 'C:/TS/NINO_FHQ/'
data = 'C:/TS/NINO_FHQ/integralcases/00020689/'

os.listdir(data)
#logfile = 'AQTOR_20120216_1_120216141127.log'
logfilezip = 'AQTOR_20120220_1_120220153604.log'
logfilezip = 'AQTOR3.71.3991.21_GregKIR_120301122604.zip'
newfile = open(path + 'genlogfile', 'w')

file = zipfile.ZipFile(data + logfilezip, "r")
for name in file.namelist():
    data = file.read(name)
    if 'AQTOR' in name:
        if 'log' in name:
            realfile = data
            print name
            newfile.write(realfile)
            break
print '--'*20

# list file information
#for info in file.infolist():
#    print info.filename, info.date_time, info.file_size

#To read data from an archive, simply use the read method.
#It takes a filename as an argument, and returns the data as a string.
#Example: Using the zipfile module to read data from a ZIP file
# File: zipfile-example-2.py

