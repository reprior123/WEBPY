localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
##############################################################################
def ENVdicts(localtag):
##    print 'loading envars from AALIVE DIR'
    import os, sys
    import rpu_rp   

    libticks = EXE + 'library.snapshotfields.csv'
    fielddict = rpu_rp.create_dict(libticks,0,2)
    libbars = EXE + 'library.bars.csv'
    libbarsweekly = EXE + 'library.bars.spaced.weekly.csv'
    libsyms = EXE + 'library.syms.csv'
    cpfname = EXE + 'signalcontroller.txt'
    libticks = EXE + 'library.snapshotfields.csv'
    libsymlines = EXE + 'library.symlines.csv'
    libsymNEWS = EXE + 'library.symNEWSTIMES.csv'
    ESlines = EXE + 'library.symlines.ES.csv'
    fielddict = rpu_rp.create_dict(libticks,0,2)
    
    bardict = rpu_rp.create_dict(libbars,0,1)
    bardictweekly = rpu_rp.create_dict(libbarsweekly,0,1)
    secdict = rpu_rp.create_dict(libbars,0,4)
    modedict = rpu_rp.create_dict(libbars,0,5)
    
    symdict = rpu_rp.create_dict(libsyms,0,1)
    tickvaluedict = rpu_rp.create_dict(libsyms,0,8)
    tsizedict = rpu_rp.create_dict(libsyms,0,7)
    showdecimaldict = rpu_rp.create_dict(libsyms,0,9)
    entrywiderdict = rpu_rp.create_dict(libsyms,0,10)
    ticktypedict = rpu_rp.create_dict(libsyms,0,11)

    symlinedict = rpu_rp.create_dict(libsymlines,0,1)
    symNEWSdict = rpu_rp.create_dict(libsymlines,0,2)
######################################
    varlist = ['ESlines','bardict','fielddict','secdict','modedict','symdict','tickvaluedict',\
    'tsizedict','showdecimaldict','entrywiderdict', 'ticktypedict','bardictweekly']
    vardict ={}
    for var in varlist:    
        vardict[var] = locals()[var]
    return vardict   
##ENVdicts('_RP')
