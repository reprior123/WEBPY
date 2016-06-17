
##def grep_to_txtfile(infilename,greppattern,outfilename):
##    try:
##        outfile = open(outfilename, 'w')
##        lines =[]
##        with open(infilename, 'r') as afile:
##            lines = afile.readlines()
##            for line in lines:
##                if greppattern in line:
##                    print 'MATCH'
##                    outfile.write(str(line))
##            outfile.write('\n')
##            outfile.close()
##    except:
##        print 'could not read ' + infilename + ' in grep_to_txtfile in rputiles'
##        pass
##    print 'outfile is in ...', outfilename
####greppattern = 'output'
####grep_to_txtfile('Script1.py',greppattern,'dukwout.txt')
outfilename = 'bb.html'
infilename = 'new.csv'
outfile = open(outfilename, 'w')
lines =[]
newline = 'http://finance.yahoo.com/d/quotes.csv?s='
with open(infilename, 'r') as afile:
    lines = afile.readlines()
    for line in lines:
            sym = line.strip()
            newline = newline + sym + '+'
##            XOM+EK+JNJ+MSFT&f=snd1t1l1ohgvwdyr
##            outfile.write(str(line))
end = '&f=snd1t1l1ohgvwdyr'
print newline + end
outfile.write(newline + end)
outfile.close()
