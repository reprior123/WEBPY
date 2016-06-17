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

##
newarr =[]
for module in moduleNames:   
    modulestripped = module.strip()
    print modulestripped
    newarr.append(modulestripped)
##modules = map(__import__,newarr)
##modules    
##    if modulestripped != titleself:
    print modulestripped, 'self'
####        print '...',modulestripped,'xxx',titleself
##    my_module =
    bla = 'Mod_TicksUtile'
    import Mod_TicksUtile, Mod_ibutiles

    importlib.import_module(bla,package=None)
##    import modulestripped
##    else:
##        print 'is self'
######################
import Mod_TicksUtile, Mod_ibutiles
##        Mod_TicksUtile
#############################
sym = 'ES'
onerow = ['3434','34343','34334','34343','343434','3434','34343','34334','34343','343434','3434','34344']
cleanonerow = Mod_TicksUtile.clean_RTTick5secBars(onerow,sym)
