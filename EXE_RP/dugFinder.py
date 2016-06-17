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
mainstem = 'C:/Users/bob/GDRIVE/MAIN DRIVE RP/'
maindir = mainstem +'memoirs'
outputtest =  maindir + '/outputtest/'
global stemdir
stemdir = 'C:/Users/bob/GDRIVE/MAIN DRIVE RP/'
print EXE

import os, sys
import hashlib

'''
Sometimes we need to find the duplicate files in our file system, or inside a specific folder.
In this tutorial we are going to code a Python script to do this. This script works in Python 3.x.
The program is going to receive a folder or a list of folders to scan,
then is going to traverse the directories given and find the duplicated files in the folders.
This program is going to compute a hash for every file,
allowing us to find duplicated files even though their names are different.
All of the files that we find are going to be stored in a dictionary, with the hash as the key,
and the path to the file as the value: { hash: [list of paths] }.
To start, import the os, sys and hashlib libraries:
Then we need a function to calculate the MD5 hash of a given file.

The function receives the path to the file and returns the HEX digest of that file:
'''
def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
'''Now we need a function to scan a directory for duplicated files:
'''
def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path.replace(stemdir,''))
            else:
                dups[file_hash] = [path.replace(stemdir,'')]
    return dups
##########
def findDupnrename(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            dirdetails = (((dirName.replace(stemdir,'')).replace('\\',' '))).upper().split()
            udetails = rpu_rp.uniqArray(dirdetails)
            lena = len(udetails)
            newfname = ''
            c=0
            while c < lena:                
                newfname += udetails[c]
                newfname += ' '
                c+=1
            newfname += filename
            print newfname
            wdirname = outputtest + newfname
##            shutil.copyfile(path,wdirname)# Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path.replace(stemdir,''))               
            else:
                dups[file_hash] = [path.replace(stemdir,'')]
    return dups
##########
def writecopies(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            dirdetails = (((dirName.replace(stemdir,'')).replace('\\',' '))).upper().split()
            udetails = rpu_rp.uniqArray(dirdetails)
            lena = len(udetails)
            newfname = ''
            c=0
            while c < lena:                
                newfname += udetails[c]
                newfname += ' '
                c+=1
            newfname += filename
            print newfname
            wdirname = outputtest + newfname
            shutil.copyfile(path,wdirname)
##            print dirdetails
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path.replace(stemdir,''))
            else:
                dups[file_hash] = [path.replace(stemdir,'')]
    return dups
'''The findDup function is using os.walk to traverse the given directory.
If you need a more comprehensive guide about it, take a look at the
How to Traverse a Directory Tree in Python article.
The os.walk function only returns the filename, so we use os.path.join to get the full path to the file.
Then we'll get the file's hash and store it into the dups dictionary.
When findDup finishes traversing the directory, it returns a dictionary with the duplicated files.
If we are going to traverse several directories, we need a method to merge two dictionaries:
'''

# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
'''joinDicts takes 2 dictionaries, iterates over the second dictionary and checks if the key exists in the first dictionary, if it does exist, the method appends the values in the second dictionary to the ones in the first dictionary. If the key does not exist, it stores it in the first dictionary. At the end of the method, the first dictionary contains all the information.
To be able to run this script from the command line,
we need to receive the folders as parameters, and then call findDup for every folder:
'''

def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            print len(result)
            words = []
            for subresult in result:
##                lengsubresult = len(subresult)
##                print lengsubresult
                file1 = subresult
                print file1
                file1words = ((file1.split('\\')[1]).split())
                upperwords=[]
                lenwrds = len(file1words)
                c=1
                for wrd in file1words:
                    if c < lenwrds:
                        upperwords.append(wrd.upper())
                        pass
                    else:
                        upperwords.append((wrd.split('.'))[0].upper())
##                    if '.' in wrd:
##                        print wrd.split('.')
##                        for w in wrd.split('.')
##                            upperwords.append(wrd.upper())
                        
##                    print wrd.upper()
##                    upperwords.append(wrd.upper())
##                print upperwords
                lastword = upperwords[len(file1words)-1].upper()
##                print lastword
                exten = lastword.split('.')[len(lastword.split('.'))-1]
                nonexten = lastword.split('.')[len(lastword.split('.'))-2]
                print exten, nonexten
##                upperwords
                fpath = os.path.join(mainstem, file1)
##                print fpath
                for word in subresult.split():
                    words.append(word)
##                print('\t\t%s' % subresult)
            print('___________________')
##            print words
 
    else:
        print('No duplicate files found.')
arg = [maindir+'/outputtest']

dups = {}
folders = arg
for i in folders:
    # Iterate the folders given
    if os.path.exists(i):
        # Find the duplicated files and append them to the dups
        joinDicts(dups, findDup(i))
##        writecopies(i)
    else:
        print('%s is not a valid path, please verify' % i)
        sys.exit()
printResults(dups)

'''The os.path.exists function verifies that the given folder exists in the filesystem. To run this script use python dupFinder.py /folder1 ./folder2. Finally we need a method to print the results:
'''

 

