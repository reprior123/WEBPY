
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
#####     #######
######  get all license logs from dll on zugiis01

###################
path = os.getcwd() + '/'
test = path + 'test/'
logpath = 'U:'

listing = os.listdir(logpath)
print listing


for file in listing:
    ffile = open(logpath + '/' + file, 'r')
    ffile.readlines()
    
