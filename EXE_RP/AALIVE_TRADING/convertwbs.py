################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open('importmodlist.txt').readlines()
for module in moduleNames:
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
import Mod_TicksUtile, Mod_ibutiles
######################
#############################
global  sym, symbol_list, symdict
########################################
date = today

def convert_emailtolines():
    wbfile = downloads +'BlountNewEmail.txt'
    wbfile = 'BlountNewEmail.txt'

    lines = rpu_rp.TxtToLines(wbfile)
    full=[]
    readflag ='n'
    label = 'WBs_'
    prevline = []
    prevlabel = ''
    fullarray =[]
    for l in lines:
        rowarray =[]
        sline = ' '.join(l.split()).replace('MAX ','MAX').replace('TWO DAY','TWODAY')
        linelength = len(sline.split())
        b = sline
        c = sline.split()
        if 'Range Projections' in str(l):
            label = 'Range_'
        elif 'TVS' in str(l):
            label = 'TVS'
        elif 'TWODAY' in str(sline):
            label = 'TWODAY_'
        elif 'OPG' in str(l):
            label = 'prev_'
        else:
            pass   
        if 'JUNE 2016 contract' in str(l):
            readflag = 'y'
        if '*email*: info@mrtopstep.com' in str(l):
            readflag = 'n'
        if readflag == 'y' and linelength > 0:
            if len(c) == 1 and len(prevline) > 1:
                if prevlabel == 'WBs_' or prevlabel == 'prev_':
                    dval = prevline[1]
                    wval = c[0]
                    
                    tag = prevlabel+prevline[0]+'_DAY'
                    val = dval
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
                    print rowarray
                    
                    tag = prevlabel+prevline[0]+'_WEEK'
                    val = wval
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
                    print rowarray
             
                if prevlabel == 'Range_':
                    dvallow = prevline[0].split('-')[0]
                    dvalhii = prevline[0].split('-')[1]
                    rangedesc = prevline[1]

                    tag = prevlabel+'Low_'+rangedesc +'_DAY'
                    val = dvallow
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
                    
                    tag = prevlabel+'Hi__'+rangedesc +'_DAY'
                    val = dvalhii
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
                    ##########
                    dvallowwk = c[0].split('-')[0]
                    dvalhiiwk = c[0].split('-')[1]
                    
                    tag = prevlabel+'Low_'+rangedesc +'_WEEK'
                    val = dvallowwk
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
         
                    tag = prevlabel+'Hi__'+rangedesc +'_WEEK'
                    val = dvalhiiwk
                    rowarray=[val,tag]
                    fullarray.append(rowarray)
                ##############################           
            if len(c) > 1 and len(prevline) > 1 and prevlabel == 'TWODAY_':
                dvallow = prevline[0].split('-')[0]
                dvalhii = prevline[0].split('-')[1]
                rangedesc = prevline[1]
                
                wval = c[0]
                tag = prevlabel+'Low_'+rangedesc +'_2DAY'
                val = dvallow
                rowarray=[val,tag]
                fullarray.append(rowarray)
                
                tag = prevlabel+'Hi__'+rangedesc +'_2DAY'
                val = dvalhii
                rowarray=[val,tag]
                fullarray.append(rowarray)
                
            prevline = c
            prevlabel = label

    fname = libarea + 'SpotsWBDaily.ES.txt'
    rpu_rp.WriteArrayToCsvfile(fname,fullarray)
