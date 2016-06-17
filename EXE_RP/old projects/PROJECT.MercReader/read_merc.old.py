import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
localtag = '_RP'
import ENVvars
nd={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
#############
downloads = 'C:/Users/bob/Downloads/'
import rpu_rp, filecmp #, os.path
import urllib, urllib2
##########################################
def grapmercpages(startnum,endnum):
    pagesfile = 'mercenary_pages.' + startnum + '.to.'+ endnum + '.txt'    
    webbase = 'http://www.mercenarytrader.net/page/'
    def Connect2Web(webpage):
      aResp = urllib2.urlopen(webpage);
      web_pg = aResp.read();
      return web_pg
    #############################
    fname = pagesfile
    i= startnum
    while i < endnum :
      webpage = webbase + str(i) +'/'
      print i
      newpage = Connect2Web(webpage)
      rpu_rp.WriteStringsToFileAppend(fname,newpage)
      i+=1
#####################
##grabmercpages(0,100)
#######################################
def parse_merc_input(filein):
    f = open(filein, 'r')
    f.close()
    f = open(filein, 'r')
    count = fcount = 0
    flagon = 'n'
    trades =[]
    date ='nodatefound'
    doublespace = 'n'
    linegaps = '0'

    datedline = newdate ='need this need | | | '
    day = month = time = ''
    for line in f.readlines():
        liner = line.split()       
        count += 1
        if count < 3000000:
##            <div class="post-byline">9:02 am - January 13, 2014 <meta http-equi
            if '<div class="post-byline">' in line:
                newdate=line.replace('<','>').split('>')[2]
##                print newdate
            if '2014' in line and len(line.split()) > 3:
                month = line.split()[3]
                day = line.split()[4]
                date = month+day
                time = line.split()[0]
            if 'triggered' in line or 'covered' in line or 'executed' in line or 'hit our risk point'  in line:
                datedline = line.strip() + '...' + newdate
                trades.append(datedline)
    stocklist =[]
    for l in trades:
        stock = l.split()[2]
        stock2 = l.split()[1]
        stocklist.append(stock)
        stocklist.append(stock2)
    ustklist = rpu_rp.uniqArray(stocklist)
    price = 'xx'
    linenum = 0
    tradelist =[]   
    for s in ustklist:
        tradeside = 'long'
        lengths = len(s)       
        searchp = ' ' +s.upper() + ' '
        searchp = ' ' + s.upper()
        searchp2 = '<li>'
        searchp2 = ' '
        if 'AMTD' not in  s  and lengths >2 and   lengths <5:
            print ' ====== ' + searchp +  ' ======'
            for line2 in trades:
                tradeside = 'long'
                if searchp in line2 and searchp2 in line2 :
                    newline = (line2.replace('<li>','|')).split('|')
                    newlinedate = (line2.replace('...','|')).split('|')
##                    print newlinedate[1]
                    newlineprice = (line2.replace('</li>','@')).split('@')
                    if 'short' in str(line2) or 'sell' in str(line2) or 'sold' in str(line2):
                        tradeside  = 'sell'
                    if '5-min rule' in str(line2):
                        tradeside  = 'notrade'
                    if 'covered' in str(line2)  :
                        tradeside  = 'coverfull'
                    if 'covered half' in str(line2) :
                        tradeside  = 'coverhalf' 
                    if '@' in str(line2):
                        price  = newlineprice[1]
                    try:
                        trdmssg = newline[1]
                    except:
                        trdmssg = 'badline'
##                    print trdmssg, 'mssg', price, searchp, linenum, tradeside, newlinedate[1]
##                    print linenum, searchp, price, tradeside
                    fulltrade = []
                    fulltrade.append(linenum)
                    fulltrade.append(searchp)
                    fulltrade.append(price)
                    fulltrade.append(tradeside)
                    fulltrade.append(newlinedate[1])
                    tradelist.append(fulltrade)
                    fulltrade =[]
                    linenum += 1
                    pass
    prevstocksym = 'bla'
    for t in sorted(tradelist, key=lambda bla: bla[0], reverse=True):
        stocksym = t[1]
        if prevstocksym != stocksym:
            status = 'flat'
            value2 = 0
            netpos = 0
            total = 0
        if status == 'flat' and t[3] == 'sell':
            value2 = 2
            status = 'short'
        if status == 'flat' and t[3] == 'long':        
            value2 = -2
            status = 'long'
        if t[3] == 'coverhalf' and status == 'short':
            value2 = -1
        if t[3] == 'coverhalf' and status == 'long':
            value2 = 1
        if t[3] == 'coverfull' and status == 'short':
            value2 = netpos * -1
        if t[3] == 'coverfull' and status == 'long':
            value2 = netpos * -1
        netpos = value2     
        total += float(t[2]) * netpos
        print t, total
        prevstocksym = stocksym
    f.close()
#####################
#######################
filein = 'mercwebscrapepages.0.100.txt'
##filein = path + 'mercwebscrapepages.txt'
dothis = parse_merc_input(filein)
##########################


tradewords =['Tightening risk point','New pending shorts','triggered','Reinstating','pyramid','executed','AUDIBLE:','Covering','Covered']
for word in tradewords:
  for line in rpu_rp.TxtToLines(filein):
    if word in str(line):
##      print line
      pass

##        if '2013' in line:
##            print line
##            date = str(liner[0:5])
##        liner.append(date)
##        if 'Trade Log' in line or 'Trade Alert'  in line  or 'Trade Note' in line:
##            flagon ='y'
##            if line == '\n':
##                print line
##        if line == '' and doublespace != 'y':
##            linegaps = '1'
##            print line
##        if line == '' and linegaps == '1':
##            doublespace = 'y'
##        if doublespace == 'y':
##            flagon = 'n'
##            print doublespace, flagon, linegaps
##        if flagon == 'y':
##            trades.append(liner)
##for l in trades:
####    print l
##    pass
##count += 1
##    if count < 100:
##        print line
##        headerarray = (line.strip()).split('\t')
##        print headerarray
##        numberfields = len(headerarray)
##        print numberfields
##        fcount = 0
##        dictbla = {}
####        for x in range(numberfields)
##        for headname in headerarray:
##            print headname, fcount
##            fcount += 1
##
##            try:
##                if headname not in dictbla:
##                    dictbla[fcount] = list()
##                    dictbla[fcount].append(headname)
##            except:
##                print 'need help'
##        print dictbla
##        print dictbla.keys()
##        print dictbla.values()
