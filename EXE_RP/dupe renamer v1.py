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

##EXE =  EXEnoslash + '/AALIVE_TRADING'
##outputtest =  maindir + '/outputtest/'
global mainstem, maindir, lenwrds
maindir = 'C:/Users/bob/Google Drive/PhotosLoose/photosm/Photos/2011/2011f'
maindir = 'C:/Users/bob/Google Drive/PhotosLoose/photosm/RPHOMEMOVSnew'
##maindir = 'C:/Users/bob/Videos/copied from data'
desktop = 'C:/Users/bob/Desktop/movsrenamed/'
mainstem = maindir + '/'
stemtoremove = 'C:/Users/bob/Google Drive/PhotosLoose/photosm/Photos/'
stemtoremove = maindir
mainstemxx = mainstem+'xx'
outputcopiesdir = desktop #maindir + '/outputrenamedcopies/'
import os, sys
import hashlib
###########
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
                dups[file_hash].append(path.replace(mainstemxx,''))
            else:
                dups[file_hash] = [path.replace(mainstemxx,'')]
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
##################
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
####################
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        resultnum =0
        for result in results:
##            print result
##            resultnum +=1
##            if resultnum == len(results):
##                print 'this is the last result of the pair', len(result)
            words = []
            upperwords=[]
            subresultnum = 0
            for subresult in result:
                subresultnum+=1
                lengsubresult = len(result)

##                print lengsubresult
                file1 = subresult
                filenostem = file1.replace(maindir,'')

##                print filenostem
                fileline  =  filenostem.replace('\\',' ').replace('_',' ').replace('-',' ')
                justfilename = filenostem.split('\\')[len(filenostem.split('\\'))-1]
                partfolder = filenostem.replace(justfilename,'')
                print partfolder, justfilename
                file1words = fileline.split()
####                print file1words
                lenwords = len(file1words)
##                print lenwords
                c=0
                for wrd in file1words:
                    c+=1
##                    print c,wrd
                    if c==lenwords:
                        lastwrdsplit = wrd.upper().split('.')
##                        print lastwrdsplit
                        if len(lastwrdsplit) == 2:
                            lastwrd = lastwrdsplit[0]
                        else:
                            lastwrd = wrd.uppper()
                        exten = lastwrdsplit[len(lastwrdsplit)-1]
                        wrd = lastwrd
                        pass
                    else:
                        wrd = wrd.upper()
                    upperwords.append(wrd.upper())
##                print exten, lastwrd, 'extension'
                if lengsubresult == subresultnum:
                    print 'lastdupe of pair'
                    newfname =''
                    upperwordsu = rpu_rp.uniq(upperwords)
                    for wordup in upperwordsu:
                        newfname = newfname +' '+ wordup
##                        newfnameNext = outputcopiesdir +partfolder+ newfname+'dupexx'+'.'+exten
                        newfnameNext = outputcopiesdir + newfname+'dupexx'+'.'+exten
                    print newfnameNext
##                    print maindir,'maindir'
##                    fpath = os.path.join(maindir, newfnameNext)
##                    print newfnameNext
                    shutil.copyfile(subresult,newfnameNext)
##                    print 'copy',subresult,'to',newfnameNext
            print('___________________')
    else:
        print('No duplicate files found.')
##################
arg = [maindir]
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
