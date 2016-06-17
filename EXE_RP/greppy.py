import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
###########################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles, rpu_rp
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
ActantData = 'C:/Program Files/Actant/Log/'
ActantDataNoSlash = 'C:/Program Files/Actant/Log'
maindirectorynoSlash = EXE + 'IbPy-master/IbPy-master'
    ########### take two header names and creates the dictionar
def grep_txtfile_to_array(infilename,greppattern):
    arrayout  =[]
    try:
        lines =[]
        with open(infilename, 'r') as afile:
            lines = afile.readlines()
            for line in lines:
                if greppattern in str(line):
                    arrayout.append(line)
    except:
        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
        pass
    print 'just grepped in rputiles...', greppattern, infilename
    return arrayout

def grep_to_txtfile(infilename,greppattern,outfilename):
    try:
        outfile = open(outfilename, 'w')
        lines =[]
        with open(infilename, 'r') as afile:
            lines = afile.readlines()
            for line in lines:
                if greppattern in str(line):
                    outfile.write(str(line))
                    print line
                    print infilename
            outfile.write('\n')
            outfile.close()
    except:
        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
        pass
    return lines

def ShowDirList(maindirectorynoSlash):
    print maindirectorynoSlash
    path  = maindirectorynoSlash
    import os
    rootDir = path
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
##            print dirName + '/' +fname
            greppattern = 'reqMktData'
            grep_to_txtfile(dirName + '/' +fname,greppattern,'dukwout.txt')
            
ShowDirList(maindirectorynoSlash)    
