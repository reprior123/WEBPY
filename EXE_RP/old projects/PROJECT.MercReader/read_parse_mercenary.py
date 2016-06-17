# -*- coding: cp1252 -*-
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
def grabmercpages(startnum,endnum):
    pagesfile = 'mercenary_pages.' + str(startnum) + '.to.'+ str(endnum) + '.txt'    
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
############grabmercpages(101,120)
#######################################
def parse_merc_input(filein):
    #### build the month dictionary from text to unix values   ###
    monthdict = {}
    mlist = ['January', 'February','March', 'April', 'May','June','July','August','September','October','November','December']
    count =1
    for mth in mlist:
        if count < 10:
            monthdict[mth.upper()] = '0' + str(count)
        else:
            monthdict[mth.upper()] = '' + str(count)
        count +=1
#####################  create the trades database based on keywords for trades  ####
    linesin = rpu_rp.TxtToLines(filein)
    count  = 0
    trades =[]
    datedline = newdate ='need this need | | | '  
    for line in linesin:
        count += 1
        if count < 300000:
##            <div class="post-byline">9:02 am - January 13, 2014 <meta http-equi
            if '<div class="post-byline">' in line:
                newdate=line.replace('<','>').split('>')[2]
##                print newdate
            triggerwordlist = ['TRIGGERED','COVERED','EXECUTED','HIT OUR RISK POINT','BOUGHT','SOLD']
            for word in triggerwordlist:
                if word in str(line).upper():
                    datedline = line.upper().strip() + '...' + newdate.upper()
                    trades.append(datedline)
                ####################
    #####################  create stock list
    stocklist =[]
    for l in trades:
##        print l
        splitline = l.replace('–','|')
        spl2 = splitline.replace('&#8211;','|')
        sp3 = spl2.split('|')
        if len(sp3) == 3 and "," in sp3[0]:
            print len(sp3), sp3
        if ';' in l and '@' in l:
            if '&#8211;;;;;' in l:
                print l
##            <p>LPX, YUM triggered &#8211; short LPX @ 13.67 &#8211; short YUM @ 67.61</p>...12:52 pm - September 25, 2012
        stock = l.split()[2]
        stock2 = l.split()[1]
        stocklist.append(stock)
        stocklist.append(stock2)
        ################
        ###############
    ustklist = rpu_rp.uniqArray(stocklist)
    price = 'xx'
    linenum = 0
    tradelist =[]
    datelines = []
    ### end of building stocklist ##
    for s in ustklist:
        tradeside = 'long'
        lengths = len(s)       
        symbolfromlist = '' + s.upper()
        print s, symbolfromlist               
        if 'AMTD' not in  s  and lengths >2 and   lengths <5:
            searchp = 'x'
##            print ' ====== ' + searchp +  ' ======'
            for lineraw in trades:
                line2 = lineraw.upper()
##                print line2
                symbolline = line2.replace('�','').replace('&#8211;','')
                symbol = symbolline.split()[1]
                
                tradeside = 'long'
                if symbolfromlist ==  symbol  :
##                    print 'found match'
##                    print '###',symbol,'###'
                    newline = (line2.replace('<LI>','|')).split('|')
                    newlinedate = (line2.replace('...','|')).split('|')
                    newlineprice = (line2.replace('</LI>','@')).split('@')
                    if 'SHORT' in str(line2) or 'SELL' in str(line2) or 'SOLD' in str(line2):
                        tradeside  = 'sell'
                    if '5-min rule'.upper() in str(line2):
                        tradeside  = 'notrade'
                    if 'covered'.upper() in str(line2)  :
                        tradeside  = 'coverfull'
                    if 'covered half'.upper() in str(line2) :
                        tradeside  = 'coverhalf' 
                    if '@' in str(line2):
                        price  = newlineprice[1]
                    try:
                        trdmssg = newline[1]
                    except:
                        trdmssg = 'badline'
##                    print trdmssg, 'mssg', price, searchp, linenum, tradeside, newlinedate[1]
                    fulltrade = []
                    dateline =[]
                    
                    txtdatemth = newlinedate[1].split()[3]
##                    print txtdatemth
                    try:
                        unixdatemth = monthdict[txtdatemth]
##                        print line2
                        
                    except:
                        print newlinedate
                        print line2
                        unixdatemth = 'BLAAA'
                    unixdateyr = newlinedate[1].split()[5]
                    unixdateday = newlinedate[1].split()[4]
                    if len(unixdateday) == 2:
                        realday = ('0' + unixdateday).replace(',','')
                    else:
                        realday = ('' + unixdateday).replace(',','')
                    
                    dateline.append(linenum)
                    dateline.append(unixdateyr + unixdatemth + realday)
                    datelines.append(dateline)

                    fulltrade.append('1')#linenum)
                    fulltrade.append(symbol)
                    fulltrade.append(price)
                    fulltrade.append(tradeside)
                    fulltrade.append(unixdateyr + unixdatemth + realday)

                    tradelist.append(fulltrade)
                    linenum += 1
    prevstocksym = 'bla'
    datesarray =[]
    sortedtrades = sorted(tradelist, key=lambda bla: bla[1], reverse=True)
    sorted(tradelist, key=lambda bla: bla[1], reverse=True)
    rpu_rp.WriteArrayToCsvfile('blatrades.csv',sortedtrades)
    for t in sortedtrades:
        date = t[1]
        datesarray.append(date)
    udates =  rpu_rp.uniqArray(datesarray)
    return sortedtrades
## 3:03 pm - May 7, 2014 
#####################
#######################
stem = '1to600'
stem = '.0.to.100'
filein = 'mercwebscrapepages' + stem + '.txt'
filein = 'mercenary_pages' + stem + '.txt'
####################
####################
newtrades = parse_merc_input(filein)
##########################
def search_for_words():       
    tradewords =['Tightening risk point','New pending shorts','triggered','Reinstating','pyramid',\
                 'EXECUT','AUDIBLE:','Covering','Covered','Sold', 'Bought', 'LONG', 'SHORT ']
    for word in tradewords:
        print word
        for line in rpu_rp.TxtToLines(filein):
            if word.upper() in (str(line)).upper():
##                print line
                pass
##search_for_words()
########################################
######def tallystocktradesoldxxxxx(arrayin):
######    prevstocksym ='x'
######    for t in sorted(arrayin, key=lambda bla: bla[0], reverse=True):
######        stocksym = t[1]
######        if prevstocksym != stocksym:
######            status = 'flat'
######            value2 = 0
######            netpos = 0
######            total = 0
######        if status == 'flat' and t[3] == 'sell':
######            value2 = 2
######            status = 'short'
######        if status == 'flat' and t[3] == 'long':        
######            value2 = -2
######            status = 'long'
######        if t[3] == 'coverhalf' and status == 'short':
######            value2 = -1
######        if t[3] == 'coverhalf' and status == 'long':
######            value2 = 1
######        if t[3] == 'coverfull' and status == 'short':
######            value2 = netpos * -1
######        if t[3] == 'coverfull' and status == 'long':
######            value2 = netpos * -1
######        netpos = value2
######        if len(t[2]) < 8:
######            price = float(t[2])
######            pass
######        else:
######            price = float(0.0)
######        total += price * netpos
######        print t, total
######        prevstocksym = stocksym
########donext = tallystocktradesold(newtrades)
###############################
def grablinkpages(filein):
    for l in rpu_rp.TxtToLines(filein):
        if 'href="http://www.mercenarytrader.net/' in l and 'more' in l:
            print l
##########grablinkpages(filein)            
########################################
def tallystocktrades(arrayin):
    prevstocksym ='x'
    arrout=[]
    for l in arrayin:
        arrout.append(l[1])
        symarray = rpu_rp.uniqArray(arrout)
##    syms = arrayin[1]
    for sym in symarray:
        status = 'flat'
        value2 = 0
        netpos = 0
        total = 0
        print sym
        prevt=[]
        for t in sorted(arrayin, key=lambda bla: bla[4], reverse=False):
            stocksym = t[1]
            if stocksym == sym and t!= prevt:             
                if status == 'flat' and t[3] == 'sell':
                    value2 = 2
                    status = 'short'
                if status == 'flat' and t[3] == 'long':        
                    value2 = -2
                    status = 'long'
                if t[3] == 'coverhalf' and status == 'short':
                    value2 = -1
                    status = 'short'
                if t[3] == 'coverhalf' and status == 'long':
                    value2 = 1
                    status = 'long'
                if t[3] == 'coverfull' and status == 'short':
                    value2 = netpos * -1
                    status = 'flat'
                if t[3] == 'coverfull' and status == 'long':
                    value2 = netpos * -1
                    status = 'flat'
                netpos = value2
                if len(t[2]) < 8:
                    price = float(t[2])
                    pass
                else:
                    price = float(0.0)
                total += price * netpos
                print t, total, netpos
                prevt = t
donext = tallystocktrades(newtrades)
###############################
