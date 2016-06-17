import os, sys
#os.chdir('path')
path = os.getcwd()    ### grabs current directory ##

search_string = sys.argv[1]

rawfile = sys.argv[2]
file = path + '/' + rawfile

outfile = path + '/bla.csv'
outfile1 = open(outfile, 'w')
for line in open(file):
 if search_string in line:
    print line
    s = str(line)
    outfile1.write(s)


## need to use the split command to give out field #1 and field 96 from  the file  adn write into another file


outfile2 = open(outfile, 'r')
for line in open(file):
 if search_string in line:    
    print line[1:19]
    s = str(line)
    outfile2.write(s)


