#
##  need to create a loop on sagecodes, the create one
##record per sage code with bus address
#
# then need to csv out a few columns from sf tables and transpose
# headers to use for counts
import os, sys
#os.chdir('path')
path = os.getcwd()    ### grabs current directory ##
sstring =  sys.argv[1]
outfile1 = 'bla'
infile = sys.argv[2]

print 'grepping ' + sstring  + ' from ' + infile + ' into ' + outfile1
file = path + '/' + infile
outfile = open(path + '/' + outfile1, 'w')

data = 'Z:/data/SFDATA/AllObjectsExport/'
#data = 'Z:\data\SFDATA\sageraw\'
users = data + 'User.csv'
accts = open(data + 'Account.csv', 'r')
opps = data + 'Opportunities__c.csv'

###############  head command #######
head=[accts.next() for 1 in 1]
print head

#### Make a list of Sage codes with Account names #####
for line in accts:
             if '"Client"' in line:
              print line
              s = str(line)
              outfile.write(s)
## tie an account to an opp ##
sstring = 'Societe Generalxxxx'
for line in open(opps, 'r'):
             if sstring in line:
              print line
              s = str(line)
              outfile.write(s)
import glob
print data
list = glob.glob(data + 'User.csv')

print list

for f in list:
        print f
        for line in open(f, 'r'):
             if sstring in line:
              print line
              s = str(line)
              outfile.write(s)

#(glob handles *,?, and [] matching).
#files = data.listdir(".")
    #ignore files starting with '.' using list comprehension
    #files=[filename for filename in files if filename[0] != '.']
#print files

###########################################


raise SystemExit
