import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, rputiles
############################
path = os.getcwd() + '/'
test = path + 'test/'
SageOut = path + 'SageOut/'
drivelet = path[0]
datapath = drivelet + ':/'
TMP = datapath + 'TMP/'
##########
datapath = 'Y:/'
DATA = datapath + 'DATA/'
dataarea = DATA + 'SFDATA/'
#########

print rputiles.path

##################2##############
##def csvToLines(justfilename):
############################################    
##def create_dict(file_inname, field1, field2):
#################################
##bla = create_dict('Y:/DATA/SFDATA/201302/20130228/20130228.sf.Accounts.csv', 0, 92)
##for sage in bla.values():
##    print sage
############################################    
##def create_dictHEADER(file_inname,search1, search2):
##############################
##def write_file_array(filename,arrayname):
###takes 3 arguments...the dates array to loop thru, the filetype, and the dirname
##### returns a filename array from sfarea 
##def filedate_looper(filedates, filetype, sfarea):
################################### take two header names and creates the dictionary
dates=['20130227', '20130203']
header1 = 'SAGECODE__C'
header2 = 'ID'
alllines = []
fnames = rputiles.filedate_looper(dates, 'Assets', dataarea)
for fname in fnames:
    print fname
    bla =  rputiles.csvToLines(fname)
    for line in bla:
        if '00' in line and 'Production' in line:
            alllines.append(line)

print alllines
rputiles.write_file_array('bla.csv',alllines)           
##
##            print line
##            assid = line[0]
##            user = line[1]
##            prod = line[3]
##            accttid = line[2]
##            name = line[12]
##            status = line[17]
##            exc = line[27]
##            classes = line[62]
##            role = line[41]
##            rate = line[113]
##            billend  = line[115]
##            if status = 'Production'
##            newline.append(assid)
##            newline.append(user)
##            newline.append(exch)
##            newline.append(assid)
##            newline.append(assid)
##            newline.append(assid)
            
##    val1 = ( rputiles.create_dictHEADER(fname, header1, header2))[0]
##    val2 = ( rputiles.create_dictHEADER(fname, header1, header2))[1]
##    newdictionary = rputiles.create_dict(fname, val1, val2)
##    namelist = ''
##    for item in newdictionary.keys():
##        namelist += item + '\n'
##    print namelist
####    for item in newdictionary.values():
####        print item
##    rputiles.write_file_array('bla.csv', namelist)   
##
##### still need the uniqer here and the file writer utile
##
