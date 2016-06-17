# -*- coding: utf-8 -*-
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, zipfile
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtag = '_' + (((path.replace('EXE_','|')).split('|'))[1]).replace('/','')
print localtag
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] 
import HVARs, rputiles
################################
EXE = EXEnoslash + '/'
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
###########################################
outputarea = TMP
worddir = 'K:\Actant University'
####################
from os import chdir, getcwd, listdir, path
from time import strftime
##from win32com import client
import win32com
##import win32

def count_files(filetype):
    ''' (str) -> int
    Returns the number of files given a specified file type.
    >>> count_files(".docx")
    11
    '''
    count_files = 0
    for files in listdir(folder):
        if files.endswith(filetype):
            count_files += 1
    return count_files
######################################
# Function "check_path" is used to check whether the path the user provided does
# actually exist. The user is prompted for a path until the existence of the
# provided path has been verified.
def check_path(prompt):
    ''' (str) -> str
    Verifies if the provided absolute path does exist.
    '''
    abs_path = raw_input(prompt)
    while path.exists(abs_path) != True:
        print "\nThe specified path does not exist.\n"
        abs_path = raw_input(prompt)
    return abs_path    
####################################################    
print "\n"
folder = check_path(worddir)
chdir(folder)

# Count the number of docx and doc files in the specified folder.

num_docx = count_files(".docx")
num_doc = count_files(".doc")

# Check if the number of docx or doc files is equal to 0 (= there are no files
# to convert) and if so stop executing the script. 

if num_docx + num_doc == 0:
    print "\nThe specified folder does not contain docx or docs files.\n"
    print strftime("%H:%M:%S"), "There are no files to convert. BYE, BYE!."
    exit()
else:
    print "\nNumber of doc and docx files: ", num_docx + num_doc, "\n"
    print strftime("%H:%M:%S"), "Starting to convert files ...\n"

# Try to open win32com instance. If unsuccessful return an error message.
try:
    word = client.DispatchEx("Word.Application")
    for files in listdir(getcwd()):
        if files.endswith(".docx"):
            new_name = files.replace(".docx", r".pdf")
            in_file = path.abspath(folder + "\\" + files)
            new_file = path.abspath(folder + "\\" + new_name)
            doc = word.Documents.Open(in_file)
            print strftime("%H:%M:%S"), " docx -> pdf ", path.relpath(new_file)
            doc.SaveAs(new_file, FileFormat = 17)
            doc.Close()
        if files.endswith(".doc"):
            new_name = files.replace(".doc", r".pdf")
            in_file = path.abspath(folder + "\\" + files)
            new_file = path.abspath(folder + "\\" + new_name)
            doc = word.Documents.Open(in_file)
            print strftime("%H:%M:%S"), " doc  -> pdf ", path.relpath(new_file)
            doc.SaveAs(new_file, FileFormat = 17)
            doc.Close()
except Exception, e:
    print e
finally:
    word.Quit()

print "\n", strftime("%H:%M:%S"), "Finished converting files."    

# Count the number of pdf files.
num_pdf = count_files(".pdf")   
print "\nNumber of pdf files: ", num_pdf

# Check if the number of docx and doc file is equal to the number of files.
if num_docx + num_doc == num_pdf:
    print "\nNumber of doc and docx files is equal to number of pdf files."
else:
    print "\nNumber of doc and docx files is not equal to number of pdf files."


###################
##rpfile = EXE + 'rputiles.py'
##r = open(rpfile, 'r')
##
##for line in r.readlines():
##    if 'def' in line:
##        print line.strip()
##
##r.close()
##raw_input('clik to exit')
