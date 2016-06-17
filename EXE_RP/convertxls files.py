import os, sys
localtag = '_RP'
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
##EXEnoslash = rootpath + 'EXE' + '_RP'
sys.path[0:0] = [rootpath + 'EXE' + '_RP']
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
    locals()[var] = nd[var]
####################
import glob, csv, subprocess, datetime, shutil, time
import  rpu_rp

desktop = 'C:/Users/bob/Desktop/'
infile = desktop + 'junk/inc.xlsx'
outfile = desktop + 'junk/inc.csv'
'''
filelist = glob.glob(desktop + 'junk/*ag*.xlsx')
for f in filelist:
    print f
    infile = f
    outfile = f.replace('xlsx','csv')
    
##    rpu_rp.convertXLSXtoCSV(infile)
    print 'done', f
    for l in rpu_rp.CsvToLines(outfile):
        if l[1] == 'Type':
            header = l
            c=0
            for h in header:
                print h,c
                c+=1
for ltd get rid of col7 20 and 21
for agz also get rid of 10 and 11
'''
def convert_xlsx_newsage_csv(filename,style):
##    rpu_rp.convertXLSXtoCSV(infile)
    outfile = infile.replace('xlsx','csv')
    outfilenew = infile.replace('xlsx','new.csv')
    lines = rpu_rp.CsvToLines(outfile)
    newfile =[]
    cl=0
    for l in lines:
        numflds = len(l)
        c=0
        newline =[]
        if style == 'incstyle':
            for col in l:
                if c == 7 or c == 21 or c == 22:
                    pass
                else:
                    newline.append(col)
                c+=1
            newfile.append(newline)
            cl +=1
        else: 
            for col in l:
                if c == 7 or c == 21 or c == 22 or c==10 or c== 11:
                    pass
                else:
                    newline.append(col)
                c+=1
##                print newline
            newfile.append(newline)
            cl +=1
            
    print 'wrting new file'
    rpu_rp.WriteArrayToCsvfile(outfilenew, newfile)
        ##############
filelist = glob.glob(desktop + 'junk/*ag*.xlsx')
for f in filelist:
    print f
    convert_xlsx_newsage_csv(f,'incstyle')
        
