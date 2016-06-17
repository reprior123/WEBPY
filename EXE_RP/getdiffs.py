
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#loop_filedate_names
############################

##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
EXE = rootpath + 'EXE/'   
EXEnoslash = rootpath + 'EXE'
sys.path[0:0] = [EXEnoslash] # sets sys directory for HVAR and rputile import
import HVARs,rputiles
datapath = rootpath
DATA = datapath + 'DATA/'
TMP = datapath + 'TMP/'
invoice_proj_area =  EXE + 'PROJECT.INVOICING/'
invoice_output_area_noslash = DATA + 'invoice_runs_raw'
logoarea = invoice_proj_area + 'logoFiles/'
invoice_output_area = invoice_output_area_noslash + '/'
bconfig = invoice_proj_area + 'billing_config_files/'
sagearea = EXE + 'PROJECT.SageFlash/'
sageconfig = sagearea   + 'config_sage_new/'
sfarea = DATA + 'SFDATA/'
SFDATA = sfarea
SAGE_EXPORTS = rootpath + 'SAGE_EXPORTS/'

##date1 ='20140329' 
##file1=sfarea + '201403/'+ date1 + '/' + date1 + '.sf.Accounts.csv'
##date2 ='20140301' 
##file2=sfarea + '201403/'+ date2 + '/' + date2 + '.sf.Accounts.csv'
##mode = 'changes'
##rputiles.diff2files(file1,file2,mode)

date1 ='20140301' 
file1=sfarea + '201403/'+ date1 + '/' + date1 + '.sf.Assets.csv'
print file1
date2 ='20140301' 
file2=sfarea + '201403/'+ date2 + '/' + date2 + '.sf.Accounts.csv'
print file2
mode = 'changes'
bla = rputiles.diff2files(file1,file2,mode)
print bla
