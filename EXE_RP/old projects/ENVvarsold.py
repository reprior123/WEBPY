#######################################
def ENVvars(localtag):
##    print 'loading envars from AALIVE DIR'
    import os, sys
    #######################################
    path = os.getcwd() + '/'
    rootpath = ((path.replace('EXE','|')).split('|'))[0]
    localtagSLASH = localtag + '/'
    EXEnoslash = rootpath + 'EXE' + localtag
    sys.path[0:0] = [EXEnoslash]
    
    EXE = EXEnoslash + '/'
    DATA = rootpath + 'DATA' + localtagSLASH
    TMP = rootpath + 'TMP' + localtagSLASH
    projectarea = parea = EXE + 'AALIVE_TRADING/'
    Cpath = 'C:/'
    TS = Cpath + 'TS/'
    AS = Cpath + 'as/'
    ################################
    date_format  = "%d-%m-%Y"
    unix_format  = "%Y%m%d"
    unixmin_format  = "%H%M"
    time_format = '%H:%M:%S'
    spaceYtime_format = ' %Y-%m-%d %H:%M:%S'
    spaceY_format = ' %Y-%m-%d '
    #####################################
    nosync = TS   #rootpath + 'NOSYNC/'
    DataDownNoSlash =  AS + 'IBDATA'
    DataDown = DataDownNoSlash + '/'  
    WeeklySave = DataDown+'WeeklySave/'
    sigarea = DataDown + 'Signals/'
    statearea = DataDown + 'Signals/states/'
    soundarea = projectarea + 'sounds/'
    #####################
    cpfname = EXE + 'signalcontroller.txt'
    libticks = EXE + 'library.snapshotfields.csv'
    libbars = EXE + 'library.bars.csv'
    libsyms = EXE + 'library.syms.csv'
######################################
    varlist = ['cpfname', 'spaceYtime_format', 'time_format', 'Cpath','unixmin_format','unix_format', 'date_format', 'path', 'rootpath',\
               'EXE', 'DATA', 'TMP','EXEnoslash','projectarea', 'time_format', 'spaceYtime_format','AS', \
               'DataDownNoSlash','spaceY_format','DataDown','sigarea','statearea','soundarea', 'libbars', 'libsyms','WeeklySave']
    vardict ={}
##    print fielddict
    for var in varlist:        
        vardict[var] = locals()[var]
    return vardict   
##ENVvars('_RP')
