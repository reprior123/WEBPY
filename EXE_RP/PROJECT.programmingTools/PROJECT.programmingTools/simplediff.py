
import os, sys, glob, csv, subprocess, datetime, shutil, difflib
#from difflib_data import *
path = os.getcwd() + '/'
test = path + 'test/'
print path
##############################
todaystring = str(datetime.date.today().strftime('%Y%m%d'))
################################  hard coded text lines   ################
sfreal = path + 'DATA/SFDATA/'
searchdate = '20120202'
ydate = '20120206'

        
bla = path + 'summarize_IBstates.new'
bla2 = path + 'size_finder.new'

file1 = open(bla,'r')
file2 = open(bla2,'r')

f1 = file1.read()
f2 = file2.read()

d = difflib.Differ(f1, f2)
d = difflib.SequenceMatcher(f1, f2)
d = difflib.ndiff(f1, f2)
#result = d.compare(f1, f2)
result = d
#print result
from pprint import pprint
pprint(result)
