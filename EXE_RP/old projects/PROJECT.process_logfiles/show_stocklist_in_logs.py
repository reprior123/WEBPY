
######   This shell is pointed toa directory, then looks for all
######    csv files and reads the first 10 lines and attempts to
######    rename them in prep for reparsing later

import subprocess as S
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess
path = os.getcwd() + '/'
testoutput = path +  'test/'
EXE = 'C:/TS/EXE/'
projectarea = EXE + 'Bankfiles/'
downloads = 'C:/TS/downloadsTS/'
downloads = 'Z:/ACCOUNTING/'
downloads = projectarea 

savedfiles = projectarea + 'newlynamed/'
processedfiles  = projectarea + 'renamed_n_processed/'
#### need to see if they have semi colons or commas  !!!!!
##then need to determine bank name etc within one line [after the header...]
files = os.listdir(downloads)
tradesdb =[]
filecount = 0
stocks =[]
for filename in files:
    filecount += 1
##    import time
##    time.sleep(0.2)
    if 'renamedxxxxx' not in filename:
        if '.log' in filename  in filename:
            print filename
            from time import gmtime, strftime
            timenow = strftime("%d%H%M%S", gmtime())
            count = 0
            import rputiles
            stocks =[]

##            finallines = rputiles.TextfileToLines(filename, 'InstrQuotingParameters')
##            finallines = rputiles.TextfileToLines(filename, 'BasketList')
##            finallines = rputiles.TextfileToLines(filename, 'License')
            patterns = ['License Max classes', 'BasketList', 'Node:']
            for pattern in patterns:
                finallines = rputiles.TextfileToLines(filename, pattern)
                for row in finallines:
                    part1 = 'dd,d'
                    try:
                        part1 = (row.split())[9]
                    except:
                        pass
##                    part1 = 'dfdf,dfd'
                    stockname = (part1.split(','))[0]
                    if 'BasketList' not in row:
                        print row
                    if pattern == 'BasketList':                        
                        stocks.append(stockname)
    ##                print stockname
    shortlist = rputiles.uniq(stocks)
    numstocks = len(shortlist)
    print shortlist
    print numstocks
##    
##            banksfile = projectarea + 'banks_config.csv'
##            who_dict= rputiles.create_dict(banksfile,0,1)
##            bname_dict= rputiles.create_dict(banksfile,0,2)
##            curr_dict= rputiles.create_dict(banksfile,0,3)
##            
##            for line in csvr:
##                l = str(line)
##                newline =[]
##                count += 1
##                if count < 9:
##                    for pattern in who_dict.keys():
##                        if pattern in l:
##                            who = who_dict[pattern]
##                            bankname = bname_dict[pattern]
##                            currency = curr_dict[pattern]
##                            print 'found pattern', pattern
##                    if 'CHF'in str(line):
##                        currency = 'CHF'
##
##                line.append(bankname)
##                line.append('.bankname')
##                line.append(currency)
##                line.append(who)
##                tradesdb.append(line)
####            print tradesdb
##            accountfile.close()
##            newname = savedfiles  + 'trans.renamed.' + bankname + '.' + who + '.' + currency + "."+ timenow + str(filecount)+'.csv'
##            oldname = downloads + filename
##            processedname = processedfiles + filename
##            needs_investigate = projectarea +filename
##
##            if bankname == 'need' or who == 'need' or currency == 'need':
####                shutil.move(oldname, needs_investigate)
##                print 'move to needs'#, oldname, needs_investigate
##            else:
####                shutil.copy(oldname, newname)
##                print 'success now make copy'#, oldname, newname
####                shutil.move(oldname, processedname)
##                print 'success now make move' #, oldname, processedname
##            print bankname, who, currency, timenow, filecount
##
##            who =  bankname = currency = 'need'
####fileout = open('bla.csv', 'w')
####for linen in tradesdb:
####    fileout.writelines(linen)
####fileout.close()
##
##projectarea = EXE + 'Bankfiles/'
##downloads = 'C:/TS/downloadsTS/'
##savedfiles = projectarea + 'newlynamed'
##processedfiles  = projectarea + 'renamed_n_processed'            
##        
####                if '922973-40 Private account,  Nancy' in str(line):
##################################
####today = datetime.date.today()
####todayf = today.strftime('%Y%m%d')
####todaystring = str(todayf)
####print todaystring
####todaystring = '20120308'
####################################  hard coded text lines   ################
####filedate = todaystring
####sfdata = path + 'DATA/SFDATA/' + filedate + '/' + filedate + '.sf.'
####outfile = open(testoutput + '/outfile.csv', 'w')
####
####accountfile = open(downloads + 'ubs rp 20120505 ytd chf.csv', 'r')
#####print accountfile.readlines()
###################################################
####def csvlinesF():
####    csvr = csv.reader( accountfile, delimiter=',' )
####    targetdbf  = []
####    for line in csvr:
####        if 'Credit' in line:
####            if 'AMOUNT EUR' in str(line) or 'AMOUNT GBP' in str(line) or 'AMOUNT USD' in str(line):
####                targetdbf.append( line )
####    return targetdbf
#####foreignlines =  csvlinesF ()
######################################
####def csvlinesD():
####    csvr = csv.reader( accountfile, delimiter=',' )
####    blalines  = []
####    print 'csving'
####    for row in csvr:
####        #print row
####        if 'Credit' in str(row):
####            if 'AMOUNT EUR' not in str(row) and 'AMOUNT GBP' not in str(row) and 'AMOUNT USD' not in str(row):
####                blalines.append( row )
####    return blalines
##domesticlines =  csvlinesD()
##
##print len(domesticlines)
####################################
####################
##payeelist =[]
####################
##count = 0
##for line in domesticlines:
##    desc0 = line[0]
##    desc1 = line[1].split(";")
##    desc2 = line[2].split(";")
##    desc3 = line[3].split(";")
##    desc4 = line[4].split(";")
##    desc5 = line[5].split(";")
##    desc7 = line[7].split(";")
##    fn1 = len(desc1)
##    fn2 = len(desc2)
##    fn3 = len(desc3)
##    fn4 = len(desc4)
##    amount = balance = payee = 999 
##        ##############
##    if fn1 > 4:
##        date = desc1[3]
##        #print desc1
##        payee = desc1[4]
##        payeelist.append(payee)
##        if payee == 'MAESTRO PAYMENT':
##            count += 1
##            payee2 = desc1[6]
##            payeetype = 'maestro'
##             #foreign includes additional rate change fields
##             #domestic = simple desc4 info           
##            amount = 888
##            if fn4 > 4 :
##                amount =  desc4[4]
##                balance = desc4[6]
##        elif payee == 'ATM WITHDRAWAL':
##            payee2 = 'ATM__' + desc1[6]
##            payeetype = 'atm'
##            amount = desc7[0].replace(' COUNTERVALUE CHF ',"")  ### this needed for foreign?
##            amount = desc4[4]
##            balance = desc4[6]
##            count += 1
##        elif payee == 'MULTI E-BANKING ORDER':
##            payeetype = 'multi'
##            payee2 = payee
##            amount =  desc1[10]
##            balance = desc1[12]
##            count += 1
##        elif payee == 'E-BANKING ORDER':
##            if fn2 > 3:
##                payeetype = 'ebank'
##                payee2 = desc1[5]
##                amount =  desc2[4]
##                balance = desc2[6]
##            if fn2 < 3:
##                if 'NANCY ROSSELAND' in str(line):    
##                    amount =  desc1[10]
##                    balance = desc1[12]
##                else:
##                    amount =  desc4[4]
##                    balance = desc4[6]
##            count += 1
##        elif 'No debit because of UBS' in payee or payee == 'BAL.SERV.PRICES' :
##            payeetype = 'bankfee'
##            payee2 = 'UBS'
##            amount = desc1[9]
##            balance = 0
##            count += 1
##        else:
##            payeetype = 'other'
##            count += 1
##            if fn1 == 10:
##                payee2 = payee
##                amount = desc1[9]
##                balance = 888
##            elif fn1 == 7:
##                payee2 = desc1[5]
##            else:
##                payee = 'bla'
##    if  fn1 > 1 and payeetype == 'other' :
##        print date, ';', amount, ';', payeetype, ';', payee2, ';', balance, ';', count, ';', payee
##        print 'xxxxx'
##     
##def f4(seq): 
##   # order preserving
##   noDupes = []
##   [noDupes.append(i) for i in seq if not noDupes.count(i)]
##   return noDupes
##
##ulist = f4(payeelist)







    
#for item in ulist:
    #print item

#and 'MULTI' in str(line)
#######################
##count  = 0
##totdebit = float(0)
##for line in accountlines:
###    if 'AMOUNT CHF' in str(line) or 'DATED ' in line:
##    #if 'MAESTRO PAYMENT' not in str(line) and 'MULTI E-BANKING' in str(line):
##    #if 'MAESTRO PAYMENT' not in str(line) and 'MULTI E-BANKING' not in str(line) and 'ATM' not in str(line):
##    if 'MAESTRO PAYMENTxxxx'  in str(line):
##        reportdet = line[0]
##        desc1 = line[1]
##        desc2 = line[2]
##        desc4 = line[4]
##        if desc2 != '' :
##            date =  str(desc1).split(";")[3]
##            payee =  str(desc1).split(";")[6]
##            amt =  (str(desc4).split(";")[0]).replace("AMOUNT CHF ","")
##            print 'XXXXXXXX', date, payee, amt
##            #print desc4
##            linesemi = str(line).split(";")
##            #print line
##            ##################################
##    if 'MAESTRO PAYMENT'  not in str(line) and 'MULTI' not in str(line) and 'xxxx' in str(line):
##        reportdet = line[0]
##        desc1 = line[1]
##        desc2 = line[2]
##        desc3 = line[3]
##        if desc1 != '' :
##            date =  str(desc1).split(";")[3]
##            payee =  str(desc1).split(";")[6]
##            amtlines =  (str(desc1).split(";"))
##            fnums = len(amtlines)
##            if fnums == 10:
##                amt =  amtlines[9].replace("AMOUNT CHF ","")
##                payee = amtlines[4]
##                date = amtlines[3]
##                print fnums,amt, payee, date
##                #########################
##    if 'MAESTRO PAYMENT'  not in str(line) and 'MULTI' not in str(line):
##        reportdet = line[0]
##        desc1 = line[1]
##        desc2 = line[2]
##        desc3 = line[3]
##        if desc1 != '' :
##            amtlines =  (str(desc1).split(";"))
##            fnums = len(amtlines)
##            if fnums < 10 and fnums > 3:
##                #amt =  amtlines[9].replace("AMOUNT CHF ","")
##                payee = amtlines[4]
##                date = amtlines[3]
##                #print fnums,amt, payee, date
##                print 'newmones', 'xxxx', desc1
##                print amtlines


                
print 'done'
