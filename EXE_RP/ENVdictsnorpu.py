import sys,os
localtag = '_RP'
print 'importing envdicts from exe..'
global path,rootpath,EXE
path = os.getcwd() + '/' ##supress
rootpath = ((path.replace('EXE','|')).split('|'))[0]##supress
localtagSLASH = localtag + '/'##supress
EXEnoslash = rootpath + 'EXE' + localtag##supress
sys.path[0:0] = [EXEnoslash]   ##supress
EXE = EXEnoslash + '/' ##supress
######################################
##########import rpu_rp
#################
def ENVdicts(localtag):
    import os
    import glob, csv, datetime, shutil, subprocess, time,zipfile,openpyxl 
    from datetime import date, timedelta
    import datetime
##    from rpu_rp import CsvToLines
#####################################################################################
    def CsvToLines(justfilename):
        lines = []  ##supress
        try:
            with open(justfilename, 'r') as afile:
                csvr = csv.reader( afile )    ##supress
                for row in csvr:    ##supress
                    lines.append( row )  
        except:
            print 'could not read ' + str(justfilename) + ' for CsvToLines in rputiles'
        return lines
###########################################
    def grep_txtfile_to_array(infilename,greppattern):
        arrayout  =[]  ##supress
        try:
            lines =[]  ##supress
            with open(infilename, 'r') as afile:
                lines = afile.readlines()   ##supress
                for line in lines:
                    if greppattern in str(line):
                        arrayout.append(line)
        except:
            print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
        return arrayout
    #####################
    def create_dict(file_inname, field1, field2):
        linesb =[]  ##supress
        linesb = CsvToLines(file_inname)   ##supress
        dict_out = {}   ##supress
        for aline in linesb:
            dict_out[str(aline[field1])]  = str(aline[field2])   ##supress  ### this uses a string
        return dict_out
    ################################################
    def create_dictGREP(file_inname, field1, field2,grepp):
        linesb =[]  ##supress
        linesb = CsvToLines(file_inname)   ##supress
        dict_out = {}   ##supress
        for aline in linesb:
            if grepp in str(aline):
                dict_out[str(aline[field1])]  = str(aline[field2])   ##supress  ### this uses a string
        return dict_out
    ################################################
    def create_dictByKey(file_inname, field1, field2,fieldkey,valuekey):
        linesb =[]  ##supress
        linesb = CsvToLines(file_inname)   ##supress
        dict_out = {}   ##supress
        for aline in linesb:
            if aline[fieldkey] == valuekey :
                dict_out[str(aline[field1])]  = str(aline[field2])   ##supress  ### this uses a string
        return dict_out
    ################################################
    def create_dict1n2(file_inname, field1, field2):
        linesb =[]   ##supress
        linesb = CsvToLines(file_inname)   ##supress
        dict_out = {}   ##supress
        fieldextra = int(field1) + 1   ##supress    
        for aline in linesb:
            if len(aline) > 1:
                combo = str(aline[field1]) + str(aline[fieldextra])   ##supress
                dict_out[combo]  = str(aline[field2])   ### this uses a string   ##supress
        return dict_out
################################################
    def create_dict1n2n6(file_inname, field1, field2):
        linesb =[]   ##supress
        linesb = CsvToLines(file_inname)   ##supress
        dict_out = {}   ##supress
        fieldextra = int(field1) + 1   ##supress
        fieldextra6 = int(field1) + 6   ##supress 
        for aline in linesb:
            if len(aline) > 1:
                combo = str(aline[field1]) + str(aline[fieldextra]) + str(aline[fieldextra6])   ##supress
                dict_out[combo]  = str(aline[field2])   ### this uses a string   ##supress
        return dict_out
################################################    
    localtagSLASH = localtag + '/'
    EXEnoslash = rootpath + 'EXE' + localtag
    sys.path[0:0] = [EXEnoslash]    ##supress
    EXE = EXEnoslash + '/'
    DATA = rootpath + 'DATA' + localtagSLASH
    TMP = rootpath + 'TMP' + localtagSLASH
    projectarea = parea = EXE + 'AALIVE_TRADING/'
    Cpath = 'C:/'
    TS = Cpath + 'TS/'
    AS = Cpath + 'as/'
    ################################
    musername = 'bob'    ### <<<<<<<<<<<<<<<<<<<<<<<<
    date_format  = "%d-%m-%Y"
    unix_format  = "%Y%m%d"
    unixmin_format  = "%H%M"
    time_format = '%H:%M:%S'
    spaceYtime_format = ' %Y-%m-%d %H:%M:%S'
    spaceY_format = ' %Y-%m-%d '
    #####################################
##    todaydash = datetime.date.today() supress
    todayoffset = 2
    todaydash = datetime.date.today() - datetime.timedelta(todayoffset)
    
    todayfunix = todaydash.strftime(unix_format)
    todaysdateunix = todayfunix 
    todaydashes = todaydash.strftime(date_format)
    today = todayfunix
    print todayfunix,' is using this date'
    
    yesterdayoffset = 1
    yesterdayraw = datetime.date.today() - datetime.timedelta(yesterdayoffset)
    
    yesterday = yesterdayraw.strftime(unix_format)
    timenow = time.strftime(unixmin_format)
    ######################
    nosync = TS   #rootpath + 'NOSYNC/'
    DataDownNoSlash =  AS + 'IBDATA'
    DataDown = DataDownNoSlash + '/'  
    WeeklySave = DataDown+'WeeklySave/'
    sigarea = AS + 'SIGNALS/'
    statearea = AS + 'STATES/'
    soundarea = projectarea + 'sounds/'
    libarea = projectarea + 'lib/'
    RulesArea = AS + 'RULES/'
    baseuser  = Cpath +'users/' + musername +'/'
    documents = baseuser +'/documents/'
    desktop = baseuser +'/desktop/'
    #####################        
    libticks = libarea + 'library.snapshotfields.csv'
    libinds = libarea + 'indlevels.csv'
    
    libbars = libarea + 'library.bars.csv'
    libbarsweekly = libarea + 'library.bars.spaced.weekly.csv'
    
    libAllSyms = libarea + 'library.ALL.syms.csv'
    libTickerSyms = libarea + 'library.ticker.syms.csv'
    libsyms = libAllSyms
  
    cpfname = libarea + 'signalcontroller.txt'
    libticks = libarea + 'library.snapshotfields.csv'
    libsymlines = libarea + 'library.symlines.csv'
    ESlines = libarea + 'library.symlines.ES.csv'
    libsymNEWS = libarea + 'library.symNEWSTIMES.csv'

    libtags = libarea + 'getbartags.csv'
    tagsdict = create_dict1n2(libtags,0,1)
    tagsstartdict = create_dict1n2(libtags,0,2)
    tagsenddict = create_dict1n2(libtags,0,3)
    
    fielddict = create_dict(libticks,0,2)
    
    indsMIDdict = create_dict1n2n6(libinds,0,2)
    indsMAXdict = create_dict1n2n6(libinds,0,3)
    indsVALNORMALdict = create_dict1n2n6(libinds,0,4)
    indsSTRINGNORMALdict = create_dict1n2n6(libinds,0,5)
    indsStdValuedict = create_dict1n2n6(libinds,0,7) 

    bardict = create_dict(libbars,0,1)
    secdict = create_dict(libbars,0,4)
    modedict = create_dict(libbars,0,5)
    bardictspaced = create_dict(libbars,0,6)
    
    bardictweekly = create_dict(libbarsweekly,0,1)
    
##    symdict = create_dictGREP(libsyms,0,1,',active,') supress
    symdictAll = create_dict(libAllSyms,0,1)
    symdict = symdictAll
    symdictTicker = create_dict(libTickerSyms,0,1)
    symdictDload = create_dict(libAllSyms,0,1)
    
    exchdict = create_dict(libsyms,0,2)
    currdict = create_dict(libsyms,0,3)
    expiredict = create_dict(libsyms,0,4)  
    typedict = create_dict(libsyms,0,5)
    dboostdict = create_dict(libsyms,0,6)
    tsizedict = create_dict(libsyms,0,7)
    tickvaluedict = create_dict(libsyms,0,8)
    showdecimaldict = create_dict(libsyms,0,9)
    entrywiderdict = create_dict(libsyms,0,10)
    ticktypedict = create_dict(libsyms,0,11)  
    roundfactordict =  create_dict(libsyms,0,12)
    optrightdict = create_dict(libsyms,0,13)
    optstrikedict = create_dict(libsyms,0,14)

    symlinedict = create_dict(libsymlines,0,1)
    symNEWSdict = create_dict(libsymlines,0,2) 
######################################
    barlist_1day = ['1day']
    barlist_78 = ['78mins']
    barlist_5sec = ['5secs']
    barlist_1min = ['1min']
    barlist_Recent = ['1min', '3mins', '5mins', '15mins','1hour']
    barlist_Recent78 = barlist_Recent + barlist_78
    barlist_All = barlist_Recent + barlist_1day
    barlist_Allw5sec = barlist_All + barlist_5sec
    indlist_oscils = ['ROC','AO','AOAcc','RSI']
    indfile = projectarea +'indfile.csv'
    indlistDict_oscils = create_dictByKey(indfile,0,1,1,'osc') #(file_inname, field1, field2,fieldkey,valuekey)
    indlist_oscils = indlistDict_oscils.keys()
    indlist_crossers = ['mcross','Stoch_CROSS','mcd','RVI_CROSS']
    indlist_partofcrosses = ['StochD','StochK','RVIsignal','RVIline']
    indlist_other  = ['ATR','diffvES']
    indlist_lines = ['kupper', 'klower','kmid','bbandupper','bbandlower','stddev',\
                     'pivot','R1', 'S1', 'S2', 'R2','sma200','sma100','sma50','ema']
    indlist_All = indlist_oscils + indlist_crossers + indlist_partofcrosses + indlist_other + indlist_lines

##    symbol_listall = symdictAll.keys() ##supress
    symlistTicker = symdictTicker.keys()
    symlistDload = symdictDload.keys()
    symlistAll = symdictDload.keys()
    
######    symbol_list2 = []##supress
######    symbol_list_opts = []##supress
######    for b in symbol_listall:
######        if typedict[b] == 'OPT' or typedict[b] == 'STK' or typedict[b] == 'INDxx':   ##supress
######            symbol_list_opts.append(b)
######        else:
######            symbol_list2.append(b)
######
######
    #################################################################
    newvars = grep_txtfile_to_array(EXE+'ENVdicts.py',' = ')   ##supress
    varlistfull = []
    for n in newvars:
        if 'supress' not in str(n):
            varb = (n.split('=')[0]).replace(' ','')   ##supress
            varlistfull.append(varb)
    vardict ={}
    for var in varlistfull:    
        vardict[var] = locals()[var]  ##supress
    return vardict   
##########################################
