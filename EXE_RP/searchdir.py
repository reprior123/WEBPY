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
desktopnoslash = 'C:/Users/bob/Desktop'
emptys = desktopnoslash + '/emptys'
##os.mkdir(emptys)
maindir = 'C:/Users/bob/Google Drive/PhotosLoose'
maindir = 'C:/Users/bob'
maindir = 'C:/Program Files'
##maindir = desktopnoslash + '/goo sage reports'
##maindir = 'C:/Users/bob/Google Drive/PhotosLoose/photosm/RPHOMEMOVSnew'
mainstem = maindir + '/'
stemtoremove = 'C:/Users/bob/Google Drive/PhotosLoose/photosm/Photos/'
stemtoremove = maindir
import os, sys
import time
###########
a = ['f','g']
b = ['h','u']
c = a +b
print c
def findsubdirs(parentFolder,search):
    mainarray = os.walk(parentFolder)
    for x in mainarray:
        if search in str(x[0]):
            print x[0],x[1]
#######################
##########
def findFile(parentFolder,search):
##    search ='WAP_SEPT07_SCAN10043'
    print search, parentFolder
    for dirName, subdirs, fileList in os.walk(parentFolder):
##        print('Scanning %s...' % dirName)
        for filename in fileList:
            path = os.path.join(dirName, filename)
            # Add or append the file path
            if search.upper() in filename.upper():
                print filename
                print path
##########
def RenameFiles(parentFolder,search):
##    search ='WAP_SEPT07_SCAN10043'
    print search, parentFolder
    for dirName, subdirs, fileList in os.walk(parentFolder):
        for filename in fileList:
            path = os.path.join(dirName, filename)
            # Add or append the file path
            if search in filename:
                numwords = len(filename.split(' '))
                if numwords > 3:
                    print filename
                    newfilename = filename.replace(search,' ')
                    newpath = os.path.join(dirName, newfilename)

                    print newfilename
##                    shutil.move(path,newpath)
##########
def emptydirs(parentFolder):
    import time
    mainarray = os.walk(parentFolder,topdown=False)
    fullarr=[]
    for d in mainarray:
##        print d[0],d[1],d[2]
        if len(d[2]) == 1 and 'point' in str(d[0]) and len(d[1]) == 0:
            print d[0],len(d[2]),d[2],
##            os.system('rmdir ' + d[0])
##            shutil.move(d[0],emptys+'temp')
##                os.remove(d[0]+'/'+'desktop.ini')
##                os.remove(d[0]+'/'+'Thumbs.db')
##                os.rmdir(d[0])
##                shutil.rmtree(d[0])
##                os.system('rmdir ' + d[0])
print 'starting....'
search = raw_input('searchhere: ')
findFile(maindir,search)
##findsubdirs(maindir,search)
##RenameFiles(maindir,search)
##emptydirs(maindir)

