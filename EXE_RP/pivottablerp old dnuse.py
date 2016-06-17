# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#########################################
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RNR/'
localtag = '_RNR'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import rputiles, HVARs, rputilesPIV
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
sagefiles = rootpath #+ 'SAGE_EXPORTS/'
SageFlash = EXE + 'PROJECT.SageFlash'
#######################################################
array =[]
####### flush the outfile   ####
filename = TMP + 'tempflashmailstktrades.txt'
rputiles.WriteStringsToFile(filename,'\n')
##fname = 'stocktrades.csv'
##patternINheader = 'Account Number'
#### end flush   ################
def pivotloop(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader):
    print 'start loop'
    temparray = rputilesPIV.pivot_final_print(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader)
    catline =  'filter' + fpattern3 + 'x' +  fpattern2+ 'x' +fpattern1 + 'x' + sumcat1 + 'x'+ sumvalue
    rputiles.WriteStringsToFile(filename,catline)   
    pastefname = TMP + catline + '.txt'
    pastearray =[]
    for line in temparray:
        lf = len(line)
        laststr = line[lf-1]
        newline = laststr
        f = 0
        while f < lf:
            newline += ','
            newline += str(line[f])
            f+=1              
##            newline = laststr + ',' + str(line)
##            print newline
        pastearray.append(newline.split(','))
    rputiles.WriteArrayToCsvfile(pastefname, pastearray)
    print pastearray
##########   Run all DETAILS first at both BASE and CHF CURRENCY    ########
##fname = 'stocktrades.csv'
##sumcatH = patternINheader
##fheader1 = patternINheader
##fpattern1 = patternINheader
##fheader2 = fheader1
##fpattern2 = patternINheader
##sumcat1 = patternINheader    
##sumcat2 = patternINheader
##fheader3 = fheader2
##fpattern3 = patternINheader
##sumvalue =patternINheader
##        ##########################################
##pivotloop(sumcat1, sumcat2, sumcatH,sumvalue,fheader1,fpattern1,fheader2,fpattern2,fheader3,fpattern3,fname,patternINheader)
        ############################
##        rputiles.cat(filename)
########################################
recipient = 'reprior123@gmail.com'
subject = 'recent sage flash output'
body = 'see report pls'
attachment_fullpath = filename
sender = 'rob.prior@actant.com'
senderpwd = 'xxxxxxx'
ccnamelisttext = sender
##rputiles.gmail_attachment(recipient, subject, body, attachment_fullpath, sender, senderpwd, ccnamelisttext)
