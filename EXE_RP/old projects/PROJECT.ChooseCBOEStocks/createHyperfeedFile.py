# -*- coding: utf-8 -*-
import os, sys
############################
blasym = ' €'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_RNR'
localtagSLASH =  localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
print EXEnoslash
import HVARs, rputiles
import glob, csv, subprocess, datetime, shutil, subprocess, time, urllib2, urllib, requests
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
projectarea = EXE + 'PROJECT.SageFlash/'
config = projectarea + 'config_sage/'
nasarea =  rootpath 
SAGE_EXPORTS = TMP
outputarea = TMP
#######################################
invoice_proj_area =  EXE + 'PROJECT.INVOICING/'
invoice_output_area_noslash = DATA + 'invoice_runs_raw'
logoarea = invoice_proj_area + 'logoFiles/'
invoice_output_area = invoice_output_area_noslash + '/'
bconfig = invoice_proj_area + 'billing_config_files/'
sagearea = EXE + 'PROJECT.SageFlash/'
sageconfig = sagearea   + 'config_sage/'
sfarea = DATA + 'SFDATA/'
SFDATA = sfarea
SAGE_EXPORTS = rootpath + 'SAGE_EXPORTS/'
######################################################
print rootpath
downloads = 'C:/Users/bob/Downloads/'
fname = '130medpricevolstocks'
f = EXE + fname

lines = rputiles.csvToLines(f)

for line in lines:
##    print 'S ' + line[0] + ' M USD XUSA XCBO'
    print 'S ' + line[0] + ' M USD XUSA'
##    S IBM M USD XUSA XCBO
## create hyperfeed

