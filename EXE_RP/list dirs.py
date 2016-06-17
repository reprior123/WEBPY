import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp

EXE =  EXEnoslash + '/AALIVE_TRADING'
mainstem = 'C:/Users/bob/Google Drive/MAIN DRIVE RP/'
maindir = mainstem +'memoirs'
outputtest = EXE # maindir # + '/outputtest/'
global stemdir
stemdir = EXE #'C:/Users/bob/GDRIVE/MAIN DRIVE RP/'
print EXE
import os, sys

import rpu_rp

def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = []    
    c=0
    for dirName, subdirs, fileList in os.walk(parentFolder): 
##        print('Scanning %s...' % dirName)
        for filename in fileList:
            dupline =[]
            c+=1
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
##            file_hash = hashfile(path)
##            dupline.append(str(c))
            dupline.append(path)
            dups.append(dupline)
    rpu_rp.WriteArrayToCsvfileAppend('bla.csv',dups)
    return dups
##########
list1 = ['4444']
list2 = ['dddd']
def compare2lists(list1,list2):
    for fname in list1:
        status = 'notfound'
        for fname2 in list2:
            if fname == fname2:
                status = 'found'
        if status == 'notfound':
            print 'did not find..',fname
compare2lists(list1,list2)
arg = [EXEnoslash]
dups = {}
folders = arg
rpu_rp.WriteArrayToCsvfile('bla.csv',[])
for i in folders:
    # Iterate the folders given
    if os.path.exists(i):
        # Find the duplicated files and append them to the dups
        findDup(i)
##        writecopies(i)
    else:
        print('%s is not a valid path, please verify' % i)
        sys.exit()

'''The os.path.exists function verifies that the given folder exists in the filesystem. To run this script use python dupFinder.py /folder1 ./folder2. Finally we need a method to print the results:
'''

 

