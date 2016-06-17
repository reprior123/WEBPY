
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
program = path + "diffviabat.bat"
input1 = bla2
input2 = bla
outputfile = path + 'outputfile.txt'
subprocess.call([program, input1, input2, outputfile])


