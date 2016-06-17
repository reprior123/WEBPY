#########################
localtag = '_RP'
import ENVvars ,sys
nd = ENVvars.ENVvars(localtag)
path = nd['path']
##sys.path[0:0]=nd['EXEnoslash'] ### needed to work without tags
##resolve vardict back to normal variables
for var in nd.keys():
    
    locals()[var] = nd[var]
####################
rpfile = EXE + 'rpu_rp.py'
print EXE
r = open(rpfile, 'r')
for line in r.readlines():
    if 'def' in line:
        print line.strip()
        pass
r.close()
raw_input('clik to exit')


