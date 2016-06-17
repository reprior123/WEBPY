# -*- coding: utf-8 -*-
import os, sys
##from datetime import datetime
#########################################
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#######################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    if 'indl' in var:
        print var
##    print nd[var]
    locals()[var] = nd[var]
####################
from time import sleep
import glob, csv, subprocess, datetime, shutil, subprocess, time, os.path
import  rpu_rp, rpInd, TicksUtile, ctypes 
##############################
#StochK,1min,valtest,poscrxx,1,0,21,BUY,stochkLT20
indlist = indlist_oscils #['RVIsignal','StochK','Stoch_CROSS','RSI','AO','ROC']
##indlist_oscils
##indlist_partofcrosses
##indlist_crossers
##indlist_lines
##indlist_All
##indlist_other
durlist = ['1min','5mins','15mins','1hour','1day']
for ind in indlist:
    for dur in durlist:
        percentvalue = 0.80
        stdfactor = 1      
        if dur == '5mins':
            stdfactor = 2
            percentvalue = 0.80
        test = 'value' # 'stringtest'
        text = 'normal' # 'neg'
        crxtext = 'crxx'
        position ='1'  ## 4 is slope,,1 is ind val,
        namestd =   'bla' #str(stdfactor)
        namepvalue = 'bla' #str(percentvalue)
        
        ilist = [ind,dur,test,crxtext,position,percentvalue,text,text,stdfactor]
        outfile =  RulesArea +ind+'.'+dur+'.'+ namestd +'.'+  namepvalue +'.rules.csv'

        lines = []
        ruleline = []
        for i in ilist:
            ruleline.append(i)
        lines.append(ruleline)
        print ruleline
        ##ROC,15mins,value,crxx,1,0.60,normal,normal
        rpu_rp.WriteArrayToCsvfile(outfile,lines)
        ##rpu_rp.WriteArrayToCsvfileAppend(outfile,lines)
        ##########
