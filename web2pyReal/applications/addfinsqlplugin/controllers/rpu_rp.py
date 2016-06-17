################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
############
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
##import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot,BarUtiles,RulesEngine
import glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime, date, timedelta
import ctypes, winsound
##import xlrd, openpyxl,zipfile ### these have been moved... numpy,codecs, cStringIO
## time functions ##
timenow = time.strftime(unixmin_format)
#####################################
def todaysdateunix():
    return todayfunix
#####################################
def todaysdatehypens(todayin):
    year = todayin[0:4]
    mo = todayin[4:6]
    day = todayin[6:8]
    return ' '+year+'-'+mo+'-'+day+' '
#####################################
def todaysminuteunix():
    return timenow
#####################################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
############################
#########################
def convertXLSX(infile,style):
    replacer='.' +style 
    outfile = (infile.replace('.xlsx', replacer)).replace(' ','')           
    fname = outfile.replace('C:/Users/bob/','')
    wb = openpyxl.load_workbook(infile)
    ws = wb.active
    barray =[]
    for r in ws.rows:       
        rowline = []
        rowline.append(fname)
        for cell in r:
            if cell.value == None:
                clean = ' '
            else:
                clean = cell.value #unicode(cell.value , errors='ignore')
            rowline.append(clean)
        barray.append(rowline)
    if style == 'csv':
        ArrayToCsvfileWriter(barray,outfile)
    else:            
        WriteArrayToTxtfile(outfile,barray)  
#########################
## for xlsx files... 
def convertXLSXtoCSV(infile):
##    outfile = (infile.replace('.xlsx', '.txt')).replace(' ','')
    outfile = (infile.replace('.xlsx', '.csv')).replace(' ','')
    wb = openpyxl.load_workbook(infile)
    sh = wb.get_active_sheet()
    barray =[]
    for r in sh.rows:
        textu =  [cell.value for cell in r]
        barray.append((textu))
    WriteArrayToCsvfile(outfile,barray)  #WriteArrayToTxtfile(fileoutname, arrayname)
#########################
def convertXLSXtoCSVwbs(infile):
    outfile = (infile.replace('.xlsx', '.xxx.csv')).replace(' ','')
    fname = outfile.replace('C:/Users/bob/Downloads/blount/dirxls\\','')    
    wb = openpyxl.load_workbook(infile)
    sh = wb.get_active_sheet()
    barray =[]
    for r in sh.rows:
        rowline = []
        for cell in r:
            if cell.value != None:
                 clean = cell.value.replace('\/','')
                 rowline.append(clean)
        rowline.append(fname)
##        print rowline
        barray.append(rowline)
    WriteArrayToCsvfile(outfile,barray)  #WriteArrayToTxtfile(fileoutname, arrayname)
#########################
def convertXLSXtoCSVold(infile):
    #-*- coding: utf-8 -*-
    outfile = infile.replace('.xlsx', '.csv')
    wb = openpyxl.load_workbook(infile)
    sh = wb.get_active_sheet()
    with open(outfile, 'wb') as f:
        c = csv.writer(f)
        for r in sh.rows:
            print r
##            c.writerow([cell.value for cell in r])
#########################
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
##############################

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)
#### outdirname with no slash on end
def openZipDir(OutdirName,zipfname):
     os.mkdir(OutdirName)
     fh = open(zipfname,'rb')
     z = zipfile.ZipFile(fh)
     for name in z.namelist():
         outfile = open(OutdirName+'/'+name, 'wb')
         outfile.write()
         outfile.close()
     fh.close()
#############################################
def convertXLStoCSV(fname):
    outfile = (fname.replace('.xls', '.csv')).replace(' ','')
    with xlrd.open_workbook(fname) as wb:
        sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
    with open(outfile, 'wb') as f:
        c = csv.writer(f)
        for r in range(sh.nrows):
            c.writerow(sh.row_values(r).value.decode('utf-8'))
##########################################
mode = 'justdiffs' ## or adds or subtracts or fullrepeat
def diff2files(file1, file2, mode):
    output = []
    try:
        with open(file1, 'r') as a:
            text1 = a.readlines()
        with open(file2, 'r') as b:
            text2 = b.readlines()
    except:
        print 'file[s] could not load'
    txt2len = len(text2)
    txt1len = len(text1)
    import difflib
    d = difflib.Differ()
    result = (d.compare(text1, text2))
    for line in result:
        if mode == 'adds' and line[0] == '+':
            output.append(line)
        if mode == 'subtracts' and '-' == line[0]:
            output.append(line)
        if mode == 'changes' and '-' ==line[0] or '+' == line[0]:
            output.append(line)
        else:
            pass   
    return output
#####################################
def diff(f1,f2):
    f3 = 'bla'
    os.system('diff ' + f1 + ' ' + f2 + ' > '+f3)
    bla = cattxt(f3)
    print bla
#########
def CsvToLines(justfilename):
    lines = []
    try:
        with open(justfilename, 'r') as afile:
            csvr = csv.reader( afile )
            for row in csvr:
                lines.append( row )  
    except:
        print 'could not read ' + str(justfilename) + ' for CsvToLines in rpus'
    return lines
###########################################
def TABToLines(justfilename):
    tabines = TxtToLines(justfilename)
    for row in tabines:
        bla = (row.strip()).split('\t')
        tablines.append(bla)
    return tablines    
###########################################
def TxtToLines(justfilename):
    lines = []
    try:
        with open(justfilename, 'r') as afile:
            lines = afile.readlines()
    except:
        print 'could not read ' + str(justfilename) + ' for TxtToLines in rpus'
    return lines
###########################################
def create_dict(file_inname, field1, field2):
    linesb =[]
    linesb = CsvToLines(file_inname)
    dict_out = {}
    for aline in linesb:
        dict_out[str(aline[field1])]  = str(aline[field2])   ### this uses a string
    return dict_out
################################################
def create_dict1n2(file_inname, field1, field2):
    linesb =[]
    linesb = CsvToLines(file_inname)
    dict_out = {}
    fieldextra = int(field1) + 1    
    for aline in linesb:
        if len(aline) > 1:
            combo = str(aline[field1]) + str(aline[fieldextra])
            dict_out[combo]  = str(aline[field2])   ### this uses a string
    return dict_out
####################
def create_dictTAB(file_inname, field1, field2):
    linesb =[]
    linesb = TABToLines(file_inname)   
    dict_out = {}
    for aline in linesb:
        if len(aline) > max(field1, field2):
            dict_out[str(aline[field1])]  = str(aline[field2])   ### this uses a string ### was changed may be broken and need the str taken away
    return dict_out
################################  creates dict in full string as item element 
def create_dictFullline(file_inname, field1, field2):
    linesb =[]
    linesb = CsvToLines (file_inname)   
    dict_out = {}
    for aline in linesb:
        dict_out[str(aline[field1])]  = str(aline)    ### this gives the full line as a string needs splitting
    return dict_out
############################################
def create_dictFulllineNonstring(file_inname, field1, field2):
    linesb =[]
    linesb = CsvToLines (file_inname)   
    dict_out = {}
    for aline in linesb:
        dict_out[str(aline[field1])]  = aline
    return dict_out
###############################
def create_dictHEADER(file_inname,search1, search2):
    linesb = csvToLines (file_inname)   
    dict_temp = {}
    count =  counthead = 0
    for aline in linesb:
        if count  == 0:
            for header in aline:
                dict_temp[header]  = counthead
                counthead += 1
            count += 1
    value1 = dict_temp[search1]
    value2 = dict_temp[search2]
    return value1, value2
##############################
def WriteStringsToFile(filename,stringname):
    outfile = open(filename, 'w')
    outfile.write(stringname)
    outfile.write('\n')
    outfile.close()
##########################################
def WriteStringsToFileAppend(filename,stringname):
    outfile = open(filename, 'a')
    outfile.write(stringname)
    outfile.write('\n')
    outfile.close()   
##########################################
##########################################
def WriteArrayToTxtfile(fileoutname, arrayname):
    outfile = open(fileoutname, 'w')
##    filecsvwriter = csv.writer(targetcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for string in arrayname:
##        print string[0]
##        fullline = string[0] + '|' + string[1] + '|' + string[2]
        outfile.write(str(string))
        outfile.write('\n')
    outfile.close()
####################
def WriteArrayToCsvfile(fileoutname, arrayname):
    targetcsvfile = open(fileoutname,'wb')
    filecsvwriter = csv.writer(targetcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for row in arrayname:
        filecsvwriter.writerow(row)
    targetcsvfile.close()
####################
    ####################
def WriteArrayToCsvfileNEW(fileoutname, arrayname):
##    targetcsvfile = open(fileoutname,'wb')
##    filecsvwriter = csv.writer(targetcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
##    with open(fileoutname,'wb') as f:
##        f.write(arrayname)
##        for row in arrayname:
##            filecsvwriter.writerow(row)
##    targetcsvfile.close()

    a = numpy.asarray(arrayname)
    numpy.savetxt(fileoutname, a, fmt = '%18S',delimiter=",")
####################
class UTF8Recoder:
    """Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")
class UnicodeReader:
    """ A CSVreader  will iterate over lines in the CSVfile "f", encoded in the given encoding."""
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self
class UnicodeWriter:
    codec = 'utf-8' #'Latin-1'  'utf-8'
##    CSV writer which will write rows to CSV file "f",which is encoded in the given encoding
    def __init__(self, f, dialect=csv.excel, encoding= codec, **kwds):
        codec = 'utf-8' #'Latin-1'  'utf-8'
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n', **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        codec = 'utf-8' #'Latin-1'  'utf-8'
        self.writer.writerow([s.encode(codec) for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode(codec)
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
##################
def ArrayToCsvfileWriter(rowsarray,fname):
    tfile = open(fname,'wb')
    writer = UnicodeWriter(tfile)
    writer.writerows(rowsarray)
    tfile.close()
#############
def WriteArrayToCsvfileAppend(fileoutname, arrayname):
    targetcsvfile = open(fileoutname,'ab')
    filecsvwriter = csv.writer(targetcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in arrayname:
        filecsvwriter.writerow(row)
    targetcsvfile.close()
###########
def WriteArrayToCsvfileWheader(fname, arrayname, headerline):
    outfile = open(fname, 'w')
    outfile.write(headerline)
    outfile.close()
    outfile = open(fname,'a')
    filecsvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for row in arrayname:
        filecsvwriter.writerow(row)
    outfile.close()
####################################################
def  uniqArray(arrayin):
    previtem ='xxxxxxx'
    uniqarray = []
    for item in sorted(arrayin):
        if previtem != item :
            uniqarray.append(item)       
        previtem = item
    return uniqarray
############################################
def  uniqElementsOfArray(arrayin):
    prevcombinedtag =  prevuniqfield0 = prevfirm ='ggg'
    previtem ='xxxxxxx'
    uniqarray = []
    for item in sorted(arrayin):
        uniqfield0 = item[0] + ' | '
        uniqfield1 = item[1] + ' | '
        uniqfield2 = item[2]+ ' | '
        uniqfield3 = item[3]
        firm = item[4]
        sharedwith = 'sharedwith >'
        combinedtag = uniqfield0 + uniqfield1 +uniqfield2 + uniqfield3
        if uniqfield0 == prevuniqfield0 and prevcombinedtag != combinedtag:
            print item, prevfirm
            item.append(sharedwith)
            item.append(prevfirm)
            print item
            uniqarray.append(item)
        previtem = item
        prevfirm =firm
        prevuniqfield0 = uniqfield0
        prevuniqfield1 = uniqfield1
        prevuniqfield2 = uniqfield2
        prevuniqfield3 = uniqfield3
        prevcombinedtag = prevuniqfield0 + prevuniqfield1 +prevuniqfield2 + prevuniqfield3
    return uniqarray
################################
def pdfer(infilename):
    pdffilefname = infilename.replace('html', 'pdf')
    if 'bob' in rootpath:
        pdferlocal = 'C:/wkhtmltopdf/wkhtmltopdf.exe'
        pdftmp = 'C:/TSTMP/tmpw.pdf'
        pdfhtml ='C:/TSTMP/tmpw.html'
    else:
        pdferlocal = 'C:/wkhtmltopdf/bin/wkhtmltopdf.exe'
        pdftmp = 'C:/tmpw.pdf'
        pdfhtml ='C:/tmpw.html'     
    pagesize = 'Letter'
    shutil.copy(infilename, pdfhtml)
    os.system(pdferlocal + ' -s ' + pagesize + ' ' + pdfhtml + ' ' + pdftmp  )
    shutil.copy(pdftmp, pdffilefname )
    print 'just ran pdfer in rputiles...might require a local install of wkhtmltopdf'
    time.sleep(1)
#######################################################################################
def grep_txtfile_to_array(infilename,greppattern):
    arrayout  =[]
    try:
        lines =[]
        with open(infilename, 'r') as afile:
            lines = afile.readlines()
            for line in lines:
                if greppattern in str(line):
                    arrayout.append(line)
    except:
        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
    return arrayout
#######################################################################################
#######################################################################################
def grep_array_to_txtfile(arrayin,outfilename,greppattern):
    arrayout  =[]
    lines = arrayin
    for line in lines:
        if greppattern in str(line):
            arrayout.append(line)
    WriteArrayToCsvfile(outfilename,arrayout)
##############################################################################
def grep_Csvfile_to_array(infilename,greppattern):
    arrayout  =[]
    try:
        lines = CsvToLines(infilename)
        for line in lines:
            if greppattern in str(line):
                arrayout.append(line)
    except:
        print 'could not read ' + infilename + ' in grep_Csvfile_to_array in rpu'
    return arrayout
#######################################################################################
def grep_array_to_array(arrayin,greppattern):
    arrayout  =[]
    try:
        lines = arrayin
        for line in lines:
            if greppattern in str(line):
                arrayout.append(line)
    except:
        print 'failed'
    return arrayout
####################################
def grep_to_txtfile(infilename,greppattern,outfilename,fieldnum):
    WriteStringsToFile(outfilename,'')
    try:
        lines = TxtToLines(infilename)
    except:
        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
    if fieldnum == 99:        
        for line in lines:
            if greppattern in line:
                WriteStringsToFileAppend(outfilename,str(line))
##            outfile.write('\n')
    else:
        for line in lines:
            if greppattern in line[fieldnum]:
                WriteStringsToFileAppend(outfilename,str(line))     
    print 'outfile is in ...', outfilename
#####################################
def bank_statements():
    bankarea = DATA 
    from os import listdir
    files  = os.listdir(bankarea)
    lines =[]
    for f in files:
        fname =bankarea + f
        if 'UBS' and 'csv' in f:
            lines += rputiles.csvToLines(fname)
            allines = lines.sorted()
#########################
def catcsv(justfilename):
    lines = []
    try:
        lines = CsvToLines(justfilename)  
    except:
        print 'could not read ' + str(justfilename) + ' for csvToLines in rputiles'
    for line in lines:
        print line
#################
def cattxt(justfilename):
    lines= TxtToLines(justfilename)
    for line in lines:
        print line
##########################
def catstring(justfilename):
    string =''
    lines= TxtToLines(justfilename)
    for line in lines:
        string += line
    return string
##########################
def  uniq(arrayin):
    previtem ='xxxxxxx'
    uniqarray = []
    for item in sorted(arrayin):
        if previtem != item :
            uniqarray.append(item)       
        previtem = item
    return uniqarray
############################################
def  uniqnosort(arrayin):
    previtem ='xxxxxxx'
    uniqarray = []
    for item in arrayin:
        if previtem != item :
            uniqarray.append(item)       
        previtem = item
    return uniqarray
############################################
def head_to_txtfile(infilename,headvalue,outfilename):
    lines= TxtToLines(infilename)   
    outfile = open(outfilename, 'w')
    count = 0
    for line in lines:
        if count < headvalue:
            outfile.write(str(line))
            count +=1
    outfile.close()
############################################
def tail_to_txtfile(infilename,tailvalue,outfilename):
    lines= TxtToLines(infilename)
    outfile = open(outfilename, 'w')
    totlen = len(lines)
    cutoff = totlen - tailvalue
    count = 1
    for line in lines:
        if count > cutoff:
            outfile.write(str(line))
        count +=1
    outfile.close()  
############################################
def tail_array_to_array(arrayin,tailvalue):
    arrayout = []
    cutoff = len(arrayin) - tailvalue
    count = 1
    for line in arrayin:
        if count > cutoff:
            arrayout.append(line)
        count +=1
    return arrayout 
############################################
def head_array_to_array(arrayin,hvalue):
    arrayout = []
    count = 1
    for line in arrayin:
        if count < hvalue:
            arrayout.append(line)
        count +=1
    return arrayout 
############################################
def ShowDirList(maindirectorynoSlash):
    print maindirectorynoSlash
    path  = maindirectorynoSlash
    rootDir = path
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('%s' % dirName,'\t%s'  %fname)
######################################################
##    for maindirectorynoSlash, dirs, files in os.walk("."):
##        for name in files:
##            print(os.path.join(maindirectorynoSlash, name))
##        for name in dirs:
##            print(os.path.join(maindirectorynoSlash, name))

        
##    from os.path import join, getsize, isfile, isdir, splitext
##    def GetFolderSize(maindirectorynoSlash):
##        TotalSize = 0
##        for item in os.walk(path):
##            for file in item[2]:
##                try:
##                    TotalSize = TotalSize + getsize(join(item[0], file))
##                except:
##                    print("error with file:  " + join(item[0], file))
##        return TotalSize
##    print(float(GetFolderSize("C:\\")) /1024 /1024 /1024)
