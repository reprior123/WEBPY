################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = open('importmodlist.txt').readlines()
for module in moduleNames:
    if module != titleself:
        my_module = importlib.import_module(module.strip())
######################
def rounderrp(x,tickvalue):
    opptick = int(1/tickvalue)
    return round(x*opptick)/opptick
###############
def rule_tester(currentstates,rule,curprice,sym):
##    rule = ['mcross','5mins','stringtest','neg',fnum,maxval,minval,'SELL']
    flag = 'nomatch'
##    print rule
    rind = rule[0]
    rdur = rule[1]
    rinddur = rind + rdur 
    rinddursym = rind + rdur + sym
    rtype = rule[2]
    percenttest = float(rule[5])
    rulestdvalue = float(rule[8])
    rstring = rule[3]
    fnum = int(rule[4])
    rsignbase = rule[7]
    rulename = rind+rdur+rtype+rstring+rsignbase
##    print indsMIDdict
    midpoint = float(indsMIDdict[rinddursym])
    sloperule = indsVALNORMALdict[rinddursym]
    PCompare = indsSTRINGNORMALdict[rinddursym]
    maxpoint = round(float(indsMAXdict[rinddursym]),4)## not used right now..could do for extreme sigs...   
    std1value = 2*  round(float(indsStdValuedict[rinddursym]),4)
##    stdpoint = std1value * rulestdvalue   
##    rulerange = (stdpoint - midpoint)*2
##    midvalue = stdpoint - midpoint
##    trigger = percenttest * midvalue
##    hitrigger = midpoint + trigger
##    lotrigger = midpoint - trigger
    svalall =''
    normal = 'normal'
    stime = ' 2016-01-08 16:00:00'
    sigprice = 0.0
    for l in currentstates:
        if flag ==  'passedrule':
            pass
        else: #keep looking
            if len(l) > 0:
                sind = l[5]
                sslope = l[4]
                ssign = l[2]
                sdur = l[8]
                sstring = l[7]
                sindsdur = sind+sdur
                stime = l[0]
                sigprice = l[11]
                crossage = l[12]
                
##                std1value =  round(float(l[13]),4)
                stdpoint = std1value * rulestdvalue   
                rulerange = (stdpoint - midpoint)*2
                midvalue = stdpoint - midpoint
                trigger = percenttest * midvalue
                hitrigger = midpoint + trigger
                lotrigger = midpoint - trigger
                
                if rtype == 'value' or rtype == 'priceCompare':
                    sval = float(l[fnum])
                else:
                    sval = l[fnum]
                svalall = svalall + str(sval)
                if '1min' in str(l):
                    stime = l[0]
                    sigprice = l[11]
                if sind == rind and sdur == rdur :
                    if rtype == 'string':
                        if 'slope' in rstring:
##                            print sloperule
                            if sloperule == 'slopenormal' and sval == 'slopedn':
                                flag = 'SELL'
                            else:
                                flag = 'BUY'
                        else:
                            if sval == 'pos' and rsignbase == 'signbased':  ## this is for signs generally...to show a state for mcross for inst
                                flag = 'BUY'
                            elif sval == 'neg' and rsignbase == 'signbased':
                                flag = 'SELL'
                            elif rstring in sstring and sstring == 'poscrxx' :
                                flag = 'BUY'
##                                print l
                            elif rstring in sstring and sstring == 'negcrxx' :
                                flag = 'SELL'
##                                print l
                            else:
                                pass
                            ################
                    elif rtype == 'priceCompare':
##                        print 'pricecompare',curprice,'must be', PCompare, sval, 'on', sdur
                        pass
                        if PCompare == 'BELOW' and sval > float(curprice):
                            print 'price is below level,so sell on klower',sval
                            flag = 'SELL'
                        elif PCompare == 'ABOVE' and sval <  float(curprice)  :
                            flag = 'BUY'
                        else:
                            pass
                        #######################
                    elif rtype == 'value' :
                        if sval >  hitrigger:
                            if normal == normal:
                                flag = 'SELL'
                            else:
                                flag == 'BUY'
                        elif sval < lotrigger:
                            if normal == normal:
                                flag = 'BUY'
                            else:
                                flag == 'SELL'
                        else:
                            flag = 'nomatch'
                    else:
                        flag = 'nomatch'
                    if flag != 'nomatch' and rtype != 'xxvalue':
                        formatl = 'SIGNAL > %s %5s %6.2f %5s %4s %s %s %4.2f %5.3f'
                        matchline = (formatl % (sym,flag,float(sigprice),sind,sdur,rsignbase,stime,sval,trigger))
                        print matchline
                        rpu_rp.WriteStringsToFileAppend(sigarea+ 'sigsrecentfromRengine.' + sdur + '.csv',matchline)
    return flag,rulename,stime,sigprice,sval
###################
def ruleslist():
    rule1 = 'mcross on all but 1 min'
    rule2 = 'stochd under over 20 80 and sloping and crossing K'
    rule3 = 'threshold use for crosses'
    rule4 = 'if position and mcross opposite dir, close, maybe not revers'
    rule5 ='mcd 15min'
    rule6 = 'rsi'
    indlist = ['mcross','mcd','RSI','StochK','Stoch_CROSS','StochD']
###########################
def run_rulesets(sym,currentstates,sigtime,curprice):
    c=0
    rulesets =glob.glob(RulesArea +'*.linerules.csv')  #### <<<<#####
    rulesets =glob.glob(RulesArea +'*.rules.csv')  #### <<<<#####
    results=[]
    for rulefilebig in rulesets:
        rulefiler=   rulefilebig.replace('RULES\\',';')
        rulefilelen = len(rulefiler.split(';'))
        rulefile = (rulefiler.split(';'))[rulefilelen-1]
        rulenamenew = rulefile.split('.')[0] + rulefile.split('.')[1]
        ruleset = rpu_rp.CsvToLines(RulesArea +rulefile) # create list based on .rules.
        c=0
        for rule in ruleset:
            if len(rule) > 2:
                resultboth = rule_tester(currentstates,rule,curprice,sym)
                result = resultboth[0]
                sigrealprice = resultboth[3]
                sigrealtime = resultboth[2]
                sigrulename = resultboth[1]
                sval = resultboth[4]
                c+=1
                if c==1:
                    prevresult = result
                if result == prevresult:
                    fullmatch = result
                    prevresult = result
                else:
                    fullmatch = 'nomatch'
                    prevresult = 'nomatch'
        resultline=[]
        resultline.append(sym)
        resultline.append(fullmatch)
        resultline.append(rulenamenew)#(rulefile)
        resultline.append(sigrealtime)
        resultline.append(sigrealprice)
        resultline.append(curprice)#(curprice)
        resultline.append(sval)
        results.append(resultline)
    return results   ### rulesetoutput
#####################
now = datetime.strftime(datetime.now(),spaceYtime_format)
now_epoch = int(time.mktime(time.strptime(now, spaceYtime_format)))
#####################
def look_for_dupe_sig(livesigid,livesigtime,delay):
    showflag = 'show'
    livesigepoch = TicksUtile.time_to_epoch(livesigtime)
    newest = max(glob.iglob(sigarea +'2*recentsigs*.csv'), key=os.path.getctime)  
    if os.path.isfile(newest):
        tradedsigs= rpu_rp.CsvToLines(newest)
        showflag = 'show'
        for lin in tradedsigs:
##            print lin
            if len(lin) > 3:
                sigid = lin[7]
                sigtime = lin[3]
                sigtimeepoch = TicksUtile.time_to_epoch(sigtime)
                timediff = livesigepoch - sigtimeepoch
                if sigid == livesigid and timediff < delay:
                    showflag = 'supress'
    return showflag
#################################
delaydupetime = 90
def parse_signalsNEW(rulesetoutput,btmode,date):
    dur = ''
    if len(rulesetoutput) > 0:
        sigcount =0
        for sig in rulesetoutput:
            if len(sig) > 0  and sig[1] != 'nomatch':
##                sig = sym,buysell,rulename,sigtime,(sigrealprice)(curprice)(sval),livesigid,boostprice
                sig.append(now)
                priceinsignal = float(sig[4]) ### need to unboost the price...
                curprice = float(sig[5]) ### need to unboost the price...
                sym = sig[0]
                tside =sig[1]
                sigtime = sig[3]
                sigtype = sig[2]
                nowepoch  =  TicksUtile.time_to_epoch(now)
                sigepoch  =  TicksUtile.time_to_epoch(sigtime)
                elapsed = nowepoch - sigepoch
                sval = float(sig[6])  # <<<<<<<<<<<<<<<<<<
                dboost = dboostdict[sym]
                boostprice = priceinsignal / float(dboost)
                livesigid = sym+tside+sigtype
                sig.append(livesigid)
                sig.append(boostprice)
                showflag = look_for_dupe_sig(livesigid,sigtime,delaydupetime)   #'notsupress'
                sigcount+=1
                if btmode == 'BACKTEST':
                    showflag = 'supress'
                if showflag != 'supress':
                    if tside == 'SELL':
####                        beep(soundarea+'sell')
##                        print sig
                        pass
####                        beep(soundarea+sym)
                    elif tside == 'BUY':
####                        beep(soundarea+'buy')
##                        print sig
                        pass
####                        beep(soundarea+sym)
                    else:
                        print 'supressing'
                    frsigline=[]
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + date +'.recentsigs.csv', [sig])
                    rpu_rp.WriteArrayToCsvfileAppend(sigarea + date +'.recentsigsexec.csv', [sig])
