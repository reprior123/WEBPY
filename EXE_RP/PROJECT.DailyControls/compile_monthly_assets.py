import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, uniq_module
############################
path = os.getcwd() + '/'
drivelet = path[0]
datapath = drivelet + ':/'
TMP = datapath + 'TMP/'
sfarea = datapath + 'DATA/SFDATA/'
################################
lines = linesXXX = []
speedmode = 'fast'
#########
monthdir ='201306'
sfmonth = sfarea + monthdir + '/'
##sfdata = sfmonth + filedate + '/' + filedate + '.sf.'
if speedmode == 'fast':
    filedates = ['looponce']    
else:  
    filedates =  sorted(os.listdir(sfmonth))
for filedate in filedates:
    print filedate
    month = filedate[0:6]
    sfmonth = sfarea + month + '/'
    sfdata = sfmonth + filedate + '/' + filedate + '.sf.'
    ####################################################
    if speedmode == 'fast':
        justfilename = ['temp_fastmode']
        filein = open('temp_fastmode.csv', 'r')
    else:
        try:
            justfilename = sfdata + 'Assets.csv'
            filein = open(justfilename, 'r')
        except:
            justfilename = 'xxxxx.cc'
            try:
                filein = open(justfilename, 'r')
            except:
                bla = 'bla'                   
    ####################################
    sagecode = '00120000000B5qNAAS'    ####CUTLER
    ##################2##############
    try:
        for row in csv.reader(filein):
            row.append(filedate)
            assetstatus = row[17]
            assetrole = row[41]
            if sagecode  in str(row) and assetstatus == 'Production' and 'Vacant' in assetrole : 
                lines.append(row)
    except:
        pass
    try:
        filein.close()
    except:
        bla = 'bla'
##== 'Trading'        
##########
if speedmode == 'slow':     
    fileoutname = open('temp_fastmode.csv', 'w')                 
    for line in lines:
        (csv.writer(fileoutname)).writerow(line)
    fileoutname.close()
else:
    bla = 'bla'           
##########
lines2 = []
lines2 = uniq_module.uniq(lines)
lines = lines2
################################
prevleadsource = full_list = stat_list = ''
dateArray =[]
macidArray  = []
fulltagsArray =[]
sagecode  = ''
counter = 0
print len(lines)
for line in lines:
    row =[]
    macid = line[20]
    assetID = line[0]
    nameIDTAG = line[1]
    classes = line[62]
    assetstatus = line[17]
    assetrole = line[41]
    datef = line[129]
    row.append(macid)
    row.append(nameIDTAG)
    row.append(classes)
    row.append(datef)
    fulltagsArray.append(row)
##    print macid, classes, nameIDTAG
    macidArray.append(macid)
    dateArray.append(datef)
##        uniq that list
       ## then go and reextract one asset per mac id
######################
dateArrayUniqs = uniq_module.uniq(dateArray)
fulltagsArrayUniqs = uniq_module.uniq(fulltagsArray)
macidUniqs  = (uniq_module.uniq(macidArray))
for macid in macidUniqs:
    print 'that was macid'
    for lineb in fulltagsArrayUniqs:
        if macid == lineb[0]:
            print lineb[0], '\t', lineb[1], '\t',lineb[2], '\t',lineb[3], '\n',   
print '########' 
print len(macidArray)
##print macidUniqs
print len(macidUniqs)
#######################
##  see if you can account for all replaced assets to accomodate machine moving around, then same for users moving around

##############
##fname = TMP  + filenameout
##print fname
##outfile = open(fname, 'w')
##outfile.write(stat_list)
##outfile.close()
##outfile = open(fname, 'r')
##print outfile.read()
##outfile.close()
####bla = raw_input('click to finish')
##
##

############################################
## remember to crete recent sagecodes file !
####################
##def create_dict(fdname):
##    binfile = open(fdname, 'r')
##    reader = csv.reader(binfile)
####    reader = binfile.readlines()
##    dictbla = {}
##    try:
##        for line in reader:
##            bla2= (line[0]).strip()
##            bla1= (line[95]).strip()
##            if bla1 not in dictbla:
##                dictbla[bla2] = list()
##                dictbla[bla2].append(bla1)
##    except:
##        print 'need help'
##    return dictbla
##    binfile.close()
##    #######
