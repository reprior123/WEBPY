
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time
############################
path = os.getcwd() + '/'
test = path + 'test/'
SageOut = path + 'SageOut/'
drivelet = path[0]
datapath = drivelet + ':/'
print drivelet , path, datapath
#########
sfarea = datapath + 'DATA/SFDATA/'
#################################
def csvToLines(justfilename, searchtext):
    lines = []
    try:
        with open(justfilename, 'r') as afile:
            csvr = csv.reader( afile )
            for row in csvr:
                if searchtext in str(row):
                    lines.append( row )  
    except Error, e:
        pass
    return lines
############################################    
newline =  full_list = ''
filedate = '20121125'
#################   end account area  #######
##create dictionary
####################################
month = filedate[0:6]
sfmonth = sfarea + month + '/'
sfdata = sfmonth + filedate + '/' + filedate + '.sf.'
#print filedate
justfilename = sfdata + 'contacts.csv'
activityfilename = sfdata + 'Tasks.csv'
print justfilename
lines = csvToLines (justfilename,'optiver')
print lines
lines2 = lines
##tasklines = csvToLines (activityfilename,'0')
prevleadsource =''
leadlist = []
f1name = 'file1'
f2name = 'file2'
data =''
for aline in lines:
    email = aline[24]
    first = aline[5]
    last = aline[4]
    if email != '' and first != '' and last != '': #and 'trx' in aline:
        acctIDa = aline[2]
        contactID = aline[0]
        verifyemail = aline[81]      
        ContactProductID = aline[3]   
        email = aline[24]
        optout = aline[31]
        bouncedemaildate = aline[41]
        phone = aline[19]
        accountID = aline[3]
        bouncedreason = aline[40]
        leadsource = aline[75]
        otheremails = aline[74]
        leadlist.append(leadsource)
        prevleadsource = leadsource
        count = 0
        f1 = open(f1name,'w')
        f2 = open(f2name,'w')
        for line2 in lines2:
            email2 = line2[24]
            phone2 = line2[19]
            first2 = line2[5]
            last2 = line2[4]
            acctIDa2 = line2[2]
            contactID2 = line2[0]
            ##### same email and name
            ##### same email and account name
##            if email in line2 and last in line2 and first in line2:
##            if email == email2 and last == last2 and first == first2: # and acctIDa == acctIDa2:
            if email == email2:
                count+= 1
                if count > 4:
                    line1str = str(aline)
                    line2str = str(line2)
                    print last, last2, email, email2, first, first2, contactID2
                    data += contactID2 + '\n'
                    os.system('echo "' + email2 + ' email2" >> allgreps.txt')
                    os.system('grep ' + contactID2 + '  ' + sfdata + '*.csv  | cut -c1-70 >> allgreps.txt')
fname = SageOut + 'dupes.csv'
outfile = open(fname, 'w')
outfile.write(data)
outfile.close()
print 'done'  
#################
outfile = open(fname, 'r')
print outfile.read()
outfile.close()
##########







                    
##                    for taskline in tasklines:
##                        if contactID in str(taskline):
##                            print taskline[2], taskline[0]
##                    f1.write(line1str)
##                    f2.write(line2str)
##                    os.system('diff ' + f1name + ' ' + f2name + '  >> bla.txt')
####            if email != '' : #and verifyemail != '':
##    if  'ice' in leadsource :
##        print email, '|', first, '|', last, '|', accountID, '|' ,leadsource, '\n'
####            print email
##    full_list += email + '\n'
###################
##previtem =''
##for item in sorted(leadlist):
##    if previtem != item:
##        print item
##    previtem = item

##fname = SageOut  + filedate + '.emailcount.all.tsv'

