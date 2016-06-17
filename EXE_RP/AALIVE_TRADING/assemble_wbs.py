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
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global  sym, symbol_list, symdict
########################################
date = today
dloads = 'C:/Users/bob/Downloads/blount/'
xlsdir = dloads +'dirxls/'
def convertxls():
    flist = glob.glob(dloads +'*.xlsx')
    for f in flist:
##        rpu_rp.convertXLSXtoCSV(f)   
        print f
#####################
def convertname():
    flist = glob.glob(xlsdir +'wb*.xlsx')
    print flist
    for f in flist:
        newname = f.replace('C:/Users/bob/Downloads/blount','newst')
        rpu.convertXLSX(f,'txt')
        print newname
#####################
convertname()
##def convertname():
##    flist = glob.glob(dloads +'blo*.txt')
##    for f in flist:
##        newname = f.replace('C:/Users/bob/Downloads/blount\\blount','wbn')
##        os.system('cp ' +f+ ' ' + dloads + newname)
####        rpu_rp.convertXLSXtoCSV(f)
##        print newname
##        print f
#######################
##convertname()
