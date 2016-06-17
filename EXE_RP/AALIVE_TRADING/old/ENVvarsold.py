#######################################
print 'importing envars from aalive trading'
#########################
def ENVvars(localtag):
    import os, sys
    #######################################
    path = os.getcwd() + '/'
    rootpath = ((path.replace('EXE','|')).split('|'))[0]
    localtagSLASH = localtag + '/'
    EXEnoslash = rootpath + 'EXE' + localtag
    sys.path[0:0] = [EXEnoslash]   
    EXE = EXEnoslash + '/'
######################################
    varlist = ['path', 'rootpath','EXE']
    vardict ={}
##    print fielddict
    for var in varlist:        
        vardict[var] = locals()[var]       
    return vardict   
