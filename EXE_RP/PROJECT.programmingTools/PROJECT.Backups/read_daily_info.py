def showlines(fileroot,fieldcheck):
    import os, sys, glob, csv, subprocess, datetime, shutil, rputiles
#########################################
    path = os.getcwd() + '/'
    drivelet = path[0] + ':/'
    EXE = drivelet + 'EXE/'
    DATA = drivelet + 'DATA/'
    TMP = drivelet + 'TMP/'
    mydirectory = 'C:/Documents and Settings/rob.prior/My Documents/'
    mydirectory  = DATA + 'invoice_runs_raw/bank statements chantal/'
    projectarea = EXE + 'PROJECT.SageFlash/'
    config = projectarea + 'config_sage/'
    inputfiles_area =  projectarea + 'inputfiles/' 
    #######################################
    output = []
    filename = 'output.daily.csv'
    headerline = 'dfdf,dfdf,dddd,dddd,\n'
    for firmcodesmall in ['inc', 'agz', 'ltd']:
        output.append(firmcodesmall)
        print firmcodesmall
        firmcodeupper = firmcodesmall.upper()
        src = mydirectory + firmcodesmall + fileroot
##        recent_manual_file_upper = config  + firmcodeupper + '.manual.entries.csv'
        dst = inputfiles_area + firmcodeupper + fileroot
        
        os.system('cp "' + src + '" '  + dst)
        lines = rputiles.csvToLines(dst)
        for line in lines:
            if line[fieldcheck] != '0.00' > 0:
##                print line
                output.append(line)
    rputiles.write_file_to_csvfileWheader(filename,output,headerline)

fileroot = '.ar.csv'
fieldcheck = 3
##showlines(fileroot,fieldcheck)
#######
fileroot = '.ap.csv'
fieldcheck = 3
##showlines(fileroot,fieldcheck)


##        fileboth = inputfiles_area  + firmcodeupper + '.both.csv '
####        filemanual = mydirectory + firmcode + '.BF.csv '
##        blob = open(dest_recent_sage_file_upper).read()
##        blob2 = open(recent_manual_file_upper).read()
##        newfile = open(fileboth, 'w')
##        blob3 = blob + blob2
##        newfile.write(blob3)
##        newfile.close()

##rerun()   ### testerline
