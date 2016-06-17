import ENVvars, os
nd ={}
nd = ENVvars.ENVvars('_RP')
for var in nd.keys():
    locals()[var] = nd[var]
####################################
env1 = EXE + 'ENVvars.py'
env2 = projectarea + 'ENVvars.py'
print EXE, projectarea
import rpu_rp

rpu_rp.diff(env1,env2)
##########
print 'now diffs in envdicts...'
env1 = EXE + 'ENVdicts.py'
env2 = projectarea + 'ENVdicts.py'
import rpu_rp

rpu_rp.diff(env1,env2)
'''
f2 = 'bla'
os.system('diff ' + env1 + ' ' + env2 + ' > '+f2)
import rpu_rp
bla = rpu_rp.cattxt(f2)
print bla
##cc= raw_input('c')
########text1_lines = rpu_rp.cattxt(env1)
########text2_lines = rpu_rp.cattxt(env2)
########import difflib
########from difflib_data import *
########
########d = difflib.Differ()
########diff = d.compare(text1_lines, text2_lines)
########print '\n'.join(diff)
'''
