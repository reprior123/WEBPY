import os, sys, csv

#os.chdir('path')
path = os.getcwd()    ### grabs current directory ##
infile =  sys.argv[1]
file = path + '/' + infile
f = csv.reader(open(file,'rb'), delimiter=',', quotechar='"')

#row1 = f.next()
work = 'C:/Work/Salesforce Data/'
fileout = open(work + 'last_activity.csv', 'w')


reader = csv.reader(f)
for row in reader:
    print row

for row in f:
    print row [0]
    fileout.write(test +'\n')

fileout.close()
