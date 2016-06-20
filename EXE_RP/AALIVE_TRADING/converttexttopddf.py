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
moduleNames = open(EXE +'importmodlist.txt').readlines()


import re # import regular expressions module

project = "./" # specify the project folder
in_file = "{}example.txt".format(project) # path to the txt-file relative to the project folder

with open(in_file) as f:    # loads the file
    content = f.read()
    keys = re.findall(r"%(.+):", content)   # find the keys using RegEx
    values = re. findall(r":\s*([\w\W]+?)\s*(?:%|$)", content) # find the values using RegEx

options = zip(keys, values) # combining keys and values in one nested list

print options
tex_code = ""
for key, value in options:
    tex_code = tex_code + "\\newcommand{{\\{}}}{{{}}}\n".format(key, value)



template = "test"
tex_code = tex_code + """

\\documentclass{{{}}} % din a4, 11 pt, one-sided,

\\begin{{document}}

\\end{{document}}
""".format(template)

import os

build_d = "{}.build/".format(project)
out_file = "{}templatemain".format(build_d)

if not os.path.exists(build_d):  # create the build directory if not existing
    os.makedirs(build_d)

with open(out_file+".tex", "w") as f:  # saves tex_code to output file
    f.write(tex_code)    


os.system("pdflatex -output-directory {} {}".format(os.path.realpath(build_d), os.path.realpath(out_file)))

##sleep(6)
shutil.copy2(out_file+".pdf", os.path.dirname(os.path.realpath(in_file)))
