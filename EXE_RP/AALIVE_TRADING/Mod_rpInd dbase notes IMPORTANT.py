def mvavgToArray(arrayin,smaNum):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    slicearray =[]
    while barnum < numbars:
        if barnum < smaNum:
            slicearray = arrayin[0:(1+barnum)]
            pass
        else:
            slicearray = arrayin[(barnum-smaNum):barnum]
        c = 0
        tot = 0
        while c < len(slicearray):
            tot += float(slicearray[c])
            divisor = len(slicearray)
            c += 1
        smaval = tot/divisor
        barnum +=1
        arrayout.append(smaval)
    return arrayout
#################################################
def EMAmvavgToArray(arrayin,smaNum):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    multiplier = round(float(2.0/(smaNum+1)),4)
    while barnum < numbars:
        valuenow = (arrayin[barnum]*1)
        prevsmavalue = (arrayin[barnum-smaNum])
        if barnum < smaNum:
            tot += valuenow
            diviser = barnum + 1
            prevema = tot/diviser
            ema = prevema
        else:
            tot += (valuenow) - (prevsmavalue)
            ema = ((valuenow - prevema) * multiplier) + prevema
            diviser = smaNum
        smaval = tot/diviser
        barnum +=1
        prevema = ema
        arrayout.append(ema)
    return arrayout
######################################
def TenkanSenmvavgToArray(arrayin,arrayhighs,arraylows,smaNum):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    slicearray =[]
    while barnum < numbars:
        if barnum < smaNum:
            slicearray = arrayin[0:(1+barnum)]
            slicearrayhi = arrayhighs[0:(1+barnum)]
            slicearraylow = arraylows[0:(1+barnum)]
            pass
        else:
            slicearray = arrayin[(barnum-smaNum):barnum]
            slicearrayhi = arrayin[(barnum-smaNum):barnum]
            slicearraylow = arrayin[(barnum-smaNum):barnum]
        c = 0
        tot = 0
        low = 9999
        high = 0
        while c < len(slicearray):
            tot += slicearray[c]
            if slicearrayhi[c] > high:
                high = slicearrayhi[c]
            if slicearraylow[c] < low:
                low =  slicearraylow[c]
            
            divisor = len(slicearray)
            c += 1
        smaval = (high +low)/2
##        print smaval,arrayin[barnum]
        barnum +=1
        arrayout.append(smaval)
    return arrayout
############################
def RSImvavgToArray(arrayin,smaNum):
    barnum = 1
    arrayout =[]
    prevavg = 0
    ### first avg gain bar  = sumof gains over past 14 bars / 14...
    ##afer that it is prevgainAvg *13 + current gain]/14
    while barnum < (len(arrayin) +1):
        tot = 0
        c =0
        subarray = arrayin[max(0,(barnum-smaNum)):barnum]
        while c < len(subarray):
            tot += subarray[c]
            c+=1
        avg = tot/len(subarray)
        if barnum > (smaNum):
            avg =(( prevavg * 13 ) + arrayin[barnum-1])/14
        arrayout.append(avg)
        prevavg = avg
        barnum +=1
    return arrayout
################################################
def RSIToArray(arrayin,smaNum):
    barnum = 0
    ## needs at least 250 datapoints
    numbars = len(arrayin)
    arrayout =[]
    tot = 0
    while barnum < numbars:
        if barnum < smaNum:
            subarray = arrayin[0:smaNum]
            for val in subarray:
                tot += val              
            AvgLoss = tot / smaNum
            AvgGain = tot
            tot += arrayin[barnum]
            diviser = barnum + 1
        else:
            tot += arrayin[barnum] - arrayin[barnum-smaNum]
            diviser = smaNum
        smaval = tot/diviser
        barnum +=1
        prevAvgGain = AvgGain
        prevAvgLoss = AvgLoss
        arrayout.append(smaval)
    return arrayout
#################################################
def RSIGainLoss(arrayin,gainmode):
    barnum = 0
    numbars = len(arrayin)
    arrayout =[]
    while barnum < numbars:
        if barnum == 0:
            prevval = arrayin[0]
        val = arrayin[barnum]
        Gain = max(val - prevval,0)
        Loss = max(prevval - val,0)
##        fstring = ' %8.4f %8.4f '
##        print fstring % (Gain,Loss)
        prevval = val
        if gainmode =='gain':            
            arrayout.append(Gain)
            pass
        else:
           arrayout.append(Loss)
        barnum +=1
    return arrayout
#############################
def difftwoarrays(a1,a2):
    alength = len(a1)
    arrayout =[]
    c = 0 
    while c < alength:
        diff = a1[c] - a2[c]
        arrayout.append(diff)
        c += 1
    return arrayout
######################################
def ratiotwoarrays(a1,a2):
    alength = len(a1)
    arrayout =[]
    c = 0 
    while c < alength:
        if a2[c] == 0:
            ratio = 100
            pass
        else:        
            ratio = a1[c]/a2[c]
        arrayout.append(ratio)
        c += 1
##        print ratio, a1[c],a2[c]
##        fstring = ' %8.4f ratio '
##        print fstring % (ratio)
    return arrayout
#####################
def test_study_values(timestamparray,valuearray,pricearray,sym,testlevela2,linetext):
    barnum = 0
    rf = roundfactordict[sym]
    while barnum < len(valuearray):
        valuetotestaroundzero = (round(decimalboost*valuearray[barnum],3))
        if abs(valuetotestaroundzero) < testlevela2 :
            print str(timestamparray[barnum]),valuetotest,round(float(pricearray[barnum]),4),linetext
        barnum +=1
#######################################
def test_stoch_values(timestamparray,valuearray,pricearray,sym,testlevela2,linetext):
    barnum = 0
    while barnum < len(valuearray):
        valuetotest = (round(decimalboost*valuearray[barnum],3))
        limitup = 100 - testlevela2
        limitdown = testlevela2
        fstring = '%s %6.2f %6.4f %s\n'
        if testlevela2 ==999:
            print fstring % (str(timestamparray[barnum]),valuetotest,round(float(pricearray[barnum]),4),linetext)
        else:        
            if abs(valuetotest) < limitdown or abs(valuetotest) > limitup :
                print fstring % (str(timestamparray[barnum]),valuetotest,round(float(pricearray[barnum]),4),linetext)
        barnum +=1
##############################################
def create_stoch(arrayclose,arrayhis,arraylows,barticksize,mode):
    bararray =[]
    c = 0
    while c < len(arrayclose):       
        if c > barticksize:
            slicelo = c-barticksize
            slicehi = c
        else:
            slicelo = 0
            slicehi = c +1
        closeslicearray = arrayclose[slicelo:slicehi]
        highsslicearray = arrayhis[slicelo:slicehi]
        lowsslicearray = arraylows[slicelo:slicehi]
        price = closeslicearray[(len(closeslicearray))-1]
        p = 0        
        prevlo = 9999.0
        prevhi = 0.00000001
        while p < len(closeslicearray):
            if highsslicearray[p] > prevhi:            
                prevhi = highsslicearray[p]
            if lowsslicearray[p] < prevlo:
                prevlo = lowsslicearray[p]
            p +=1
        c +=1      
        kdivisor = (prevhi - prevlo + 0.0000000001)
        K = 100*((price - prevlo)/(kdivisor)) ##%K = 100[(C-L5close)/(H5-L5)]
        StochRSI = 100*((price - prevlo)/(kdivisor)) ##%K = 100[(C-L5close)/(H5-L5)]
##        print K,prevhi, prevlo, price,kdivisor      
        if mode == 'K':
            bararray.append(K)
    return bararray
##############################################
def makearray(a1,a2,a3,a4,a5,a6,a7,a8,mode):  ## assumes one field in postion 0
    arrayout =[]
    roundfactor = 5
    c=0
    flist = [a4,a5,a6,a7,a8]
    while c < len(a1):
        newline =[]                                                                     
        newline.append(a1[c])## this is time string
        if mode == '3strings':
            newline.append(a2[c])
            newline.append(a3[c])
            pass
        else:
            newline.append(round(a2[c],roundfactor))
            newline.append(round(a3[c],roundfactor))
            pass
        for f in flist:
            newline.append(round(f[c],roundfactor))
        arrayout.append(newline)
        c+=1
    return arrayout
##############################################
def makearrayJust2(time,slopebs,signbs,bs,indy2,slope2,sign2):  ## assumes one field in postion 0
    arrayout =[]
    c=0
    while c < len(bs):
        newline =[]
        numfields = 8
        f = 0
        flist = [time,slopebs,signbs,bs,indy2,slope2,sign2]
        for f in flist:
            newline.append(f[c])
        arrayout.append(newline)
        c+=1
    return arrayout
##############################################
def show_slope(arrayin,tag):
    arrayout =[]
    c = 0
    diff = 0
    while c < len(arrayin):
        if c == 0 :
            prevc = 0
        else:
            prevc = c-1
        diff = arrayin[c] - arrayin[prevc]
        if diff < 0 :
            result = 'slopedown'
        elif diff > 0:
            result = 'slopeupup'
        else:
            result ='flatflatt'
        final = tag+result
        arrayout.append(final)
        c +=1
    return arrayout
##############################################
def CLV_Value(Carray,Larray,Harray):
    CLVarray =[]   
    c = 0
    while c < len(Carray):

        C = Carray[c]
        H = Harray[c]
        L = Larray[c]
        CLV = ((C-L)-(H-C))/(H-L)
        CLVarray.append(round(CLV,4))
        c +=1
    return CLVarray
########################
def sushiroll_finder():
    pass
###############################################
def backtest_sigs(arrayin,texttosell,texttobuy,pricefnum):
    flag = 'flat'
    pnl = 0
    for line in arrayin:
##        print line
        curprice = float(line[pricefnum])
##        print curprice
        if texttosell in str(line):
            pnlsmax = -999.99
            pnlsmin = 999.999
            pnl = 0
            print line
            flag = 'SELL'
            sellprice = curprice
            pass
        elif texttobuy in str(line):
            print 'last sell was',pnlsmax,pnlsmin,sellprice,curprice
            flag = 'BUY'
            pnlbmax = -999.99
            pnlbmin = 999.999
            pnl = 0
            print line
            buyprice = curprice
        if flag == 'SELL':
            pnl = sellprice - curprice
            if pnl > pnlsmax:
                pnlsmax = pnl
            if pnl < pnlsmin:
                pnlsmin = pnl
##            print round(pnl,5), flag, sellprice, curprice
        elif flag == 'BUY':
            pnl = curprice - buyprice
##            print round(pnl,5), flag, sellprice, curprice
##################################  
def show_test_lines(arrayin,texttosell,texttobuy,pricefnum,testval):
    flag = 'flat'
    format8 ='%11s %13s %11s %11s %11s %9s %9s %9s %9s'
    for line in arrayin:
        curprice = float(line[pricefnum])
        if texttosell in str(line):
            flag = 'SELL'
        elif texttobuy in str(line):
            flag = 'BUY'
        else:
            pass
##################################  
def show_macd_low_lines(arrayin,texttosell,texttobuy,pricefnum,macdtestval,macdfnum):
    arrayout =[]
    for line in arrayin:
        if abs(float(line[macdfnum])) < macdtestval :
            arrayout.append(line)
    return arrayout
################################## 
def show_smi_cross_lines(arrayin,texttosell,texttobuy,pricefnum,macdtestval):
    for line in arrayin:
        if abs(float(line[5])) < macdtestval :
            print line
##################################  
def show_nearcross(arrayin,texttosell,texttobuy,pricefnum):
    flag = 'flat'
    ## try and show when a bar is close to a crossover and sloping the right direction on sma21  
    for line in arrayin:
        curprice = float(line[pricefnum])
        if texttosell in str(line):
            flag = 'SELL'
            print line, flag
        elif texttobuy in str(line):
            flag = 'BUY'
            print line, flag
##################################
def format_lines(arrayin,tailamt):
    formatl ='%11s %13s %11s %8.2f  %8.2f %11s %9s '
    linenum = 0
    cutoff = len(arrayin) - tailamt
    for line in arrayin:
        time = line[0]
        price = float(line[3])
        pslope = line[1]
        psign = line[2]
        mcd = float(line[4])
        mslope = line[5]
        msign = line[6]
        linenum +=1
        if linenum > cutoff:
            print (formatl % (time,pslope,psign,price,mcd,mslope,msign))
##################################
def format_arrays(array1,stringnums):  ## 1 is one string, 3 is 3 strings
    arrayout =[]  
    c=0
    for line in array1:
        c = 0
        fstring =''
        variables = int(0)
        while c < len(line):
            variables = line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8]
            if c < stringnums:
                fstring += '%s '
            else:
                fstring += '%8.2f '
            c +=1
        stringout = (fstring % (variables))
        arrayout.append(stringout)        
    return arrayout
######################################################
def show_crossover(signs,tag):  
    c=0
    prevsign = 'flat'
    arrayout =[]
    while c < len(signs):
        sign = signs[c]
        if sign == prevsign:
            crossflag = 'flatcr' +tag
        elif sign == 'negneg'+tag:
            crossflag = 'negcross'+tag
        else:
            crossflag = 'poscross'+tag        
        arrayout.append(crossflag)
        prevsign = sign
        c+=1
    return arrayout
##############################################
def show_sign(a1,tag):  
    c=0
    arrayout =[]
    while c < len(a1):
        diffval = a1[c]
##        print diffval
        if diffval < 0.0 :
            signof_diffval = 'neg'
        elif diffval > 0.0 :
            signof_diffval = 'pos'
        else:
            signof_diffval = 'na'
        c+=1
        arrayout.append(signof_diffval+signof_diffval+tag)   
    return arrayout
###########################################
def pivotpoint(a1,a2,a3):
    c=0
    ####    ppoint = (prevbarHi + prevbarlo +prevclose)/3
    arrayout =[]
##    arrayout.append(a1[0])
    while c < len(a1):
        c+=1
        piv = a1[c-1] + a2[c-1] + a3[c-1]
        arrayout.append(piv)
    return arrayout
######################
def R1(a1,a2):  ## S1 is the same but with lows
    c=0
    arrayout =[]
    arrayout.append(a1[0])
    while c < len(a1): #a1 is pivotpoint array a2 is highs
        if c == 0:
            R1 = (2*a1[c]) -  a2[c]
        else:
            R1 = (2*a1[c]) -  a2[c-1]
        c+=1
        arrayout.append(R1)
    return arrayout
#############################
def process_ticks(lines,sym,dur):
    bs = strip1float(lines,5,sym) ##raw close price
    bshighs = strip1float(lines,3,sym)
    bslows = strip1float(lines,4,sym)
    timestamparray = strip1string(lines,1)
    symarray = strip1string(lines,0)
    sym = symarray[1]
    durarray = []
    for b in symarray:
        durarray.append(dur) 
### create pivots rs and ss ###
    piv = pivotpoint(bs,bshighs,bslows)
##    R1 = R1(piv,bshighs)
########################################
    signbs = show_sign(bs,'price')
    slopebs = show_slope(bs,'price')
    ##### MA Cross ##
    macrossval = difftwoarrays(EMAmvavgToArray(bs,9),EMAmvavgToArray(bs,21))
    signmcd = show_sign(macrossval,'mcd') 
    crossesmcd = show_crossover(signmcd,'mcd')
    slopemcd = show_slope(macrossval,'mcd')
    MDarray = makearrayJust2(timestamparray,symarray,durarray,bs,macrossval,crossesmcd,signmcd)
    ma = rpu_rp.grep_array_to_array(MDarray,'cross')
    rpu_rp.WriteArrayToCsvfile(sigarea + today +'.' +sym+ '.' + dur +'.sigs.csv', ma)
    rpu_rp.WriteArrayToCsvfileAppend(sigarea +today + '.sigs.csv',[ ma[len(ma)-1]])
    return ma
###################################
def process_MACDticks(lines,sym,dur):
    bs = strip1float(lines,5,sym) ##raw close price
    bshighs = strip1float(lines,3,sym)
    bslows = strip1float(lines,4,sym)
    timestamparray = strip1string(lines,1)
    symarray = strip1string(lines,0)
    sym = symarray[1]
    durarray = []
    for b in symarray:
        durarray.append(dur) 
    sma26 = EMAmvavgToArray(bs,26)
    sma12 = EMAmvavgToArray(bs,12)
    sma50 = EMAmvavgToArray(bs,50)
    macddiff = difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = EMAmvavgToArray(macddiff,9)
    macddiverg = difftwoarrays(macddiff,macdavg)
    piv = pivotpoint(bs,bshighs,bslows)
    signbs = show_sign(bs,'price')
    slopebs = show_slope(bs,'price')

    signmcd = show_sign(macddiverg,'mcd') 
    crossesmcd = show_crossover(signmcd,'mcd')
    slopemcd = show_slope(macddiverg,'mcd')
    MDarray = makearrayJust2(timestamparray,symarray,durarray,bs,macddiverg,crossesmcd,signmcd)
    ma = rpu_rp.grep_array_to_array(MDarray,'cross')
    return ma
###################################
def notes():
    ################
    bs = rpInd.strip1value(lines,5) ##raw close price
    lenbs = len(bs)
    tailstart = lenbs - 50
    print tailstart,'tailstart'
    ###############
    bsshort = bs[0:1000000]
    bshighs = rpInd.strip1value(lines,3)
    bslows = rpInd.strip1value(lines,4)
    timestamparray = rpInd.strip1value(lines,1)
    ########################
    sma26 = rpInd.EMAmvavgToArray(bs,26)
    sma12 = rpInd.EMAmvavgToArray(bs,12)
    sma50 = rpInd.EMAmvavgToArray(bs,50)
    macddiff = rpInd.difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = rpInd.EMAmvavgToArray(macddiff,9)
    macddiverg = rpInd.difftwoarrays(macddiff,macdavg)
    ########## 
    RSIgain = rpInd.RSIGainLoss(bs,'gain')
    RSIloss = rpInd.RSIGainLoss(bs,'loss')
    rsiavggain = rpInd.RSImvavgToArray(RSIgain,14)
    rsiavgloss = rpInd.RSImvavgToArray(RSIloss,14)
##    print rsiavgloss
    RS = rpInd.ratiotwoarrays(rsiavggain,rsiavgloss)    
##    rsi = 100 - ( 100 / (1 + RS))
    rsiArray =[]
    for ratio in RS:
        rsi = min(100,(100 - ( 100 / (1 + ratio))))
        rsiArray.append(rsi)
        #################
    tenkan = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,9)
    kijunSen = rpInd.TenkanSenmvavgToArray(bs,bshighs,bslows,26)
    #######################
    smacrossdiff = rpInd.difftwoarrays(sma50,bs)
    diff = rpInd.difftwoarrays(tenkan,kijunSen)
    slope50 = rpInd.show_slope(sma50)
    sign50 = rpInd.show_sign_and_crosses(macddiverg)
##    newarray = rpInd.join_8arrays_to_1_array(timestamparray,bs,sma26,sma12,sma50,macddiverg,tenkan,kijunSen,'mode')
    newarray = rpInd.join_8arrays_to_1_array(timestamparray,slope50,sign50,bs,sma50,macddiverg,tenkan,kijunSen,'3strings')
##    farray = rpInd.format_arrays(newarray,3)
    ##backtest_sigs(arrayin,texttosell,texttobuy,pricefnum)
##    rpInd.backtest_sigs(newarray[0:600000],'negcross','poscross',3)
##    rpInd.backtest_sigs(newarray[tailstart:600000],'slope','slope',3)
##    rpInd.show_test_lines(newarray[tailstart:600000],'negnegcross','posposcross',3)
##    rpInd.show_macd_low_lines(newarray[tailstart:600000],'negnegcross','posposcross',3,(0.005/decimalboost))
    smiarray = rpInd.join_8arrays_to_1_array(timestamparray,slope50,sign50,bs,sma50,smacrossdiff,tenkan,kijunSen,'3strings')
    rpInd.show_macd_low_lines(smiarray[tailstart:600000],'negnegcrossxxx','posposcrossxxx',3,(1.0/decimalboost))
##############
def MACDdiverg():
    sma26 = rpInd.EMAmvavgToArray(bs,26)
    sma12 = rpInd.EMAmvavgToArray(bs,12)
    sma50 = rpInd.EMAmvavgToArray(bs,50)
    macddiff = rpInd.difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = rpInd.EMAmvavgToArray(macddiff,9)
    macddiverg = rpInd.difftwoarrays(macddiff,macdavg)
#####################
def keltner_channel_upper(smaval,mult):
    EMA20 + (mult2 * ATR(10))
##             for the first 14 bars use TR#1 = hi-low, the first 14bars ATR = avg fo daily TR till thatpoint
    ATR =((prevATR *13) + TR) / 14  ## using 14 period value
    TR = max(high-low,abs(high- prevclose),abs(low-prevclose))
##################
def keltner_channel_lower():
    EMA20 - (2 * ATR(10))
##################
def keltner_channel_mid():
    EMA20 = need
def fibbo_retrace(startbarval,endbarval):
    pass
##    32 and 68 percent are the min and max
def CCI():
##    CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)
    pass
##                  uses Typical Price TP = [Hi + lo + close ]/3
##                  MEanDev = totaldiff / 20
##                  diff = abs(TP -EMA20)
##                  totaldiff = sum last 20 diffs
##                  100 +/- is the triggerstate
###########################
def Trigger_MACD(lines,sym,dur):
    bs = strip1float(lines,5,sym) ##raw close price
    bshighs = strip1float(lines,3,sym)
    bslows = strip1float(lines,4,sym)
    timestamparray = strip1string(lines,1)
    symarray = strip1string(lines,0)
    sym = symarray[1]
    
    durarray = []
    for b in symarray:
        durarray.append(dur)
        
    sma26 = EMAmvavgToArray(bs,26)
    sma12 = EMAmvavgToArray(bs,12)
    sma50 = EMAmvavgToArray(bs,50)
    macddiff = difftwoarrays(sma12,sma26)
    ## macd is the mvavg9 on this diff
    macdavg = EMAmvavgToArray(macddiff,9)
    macddiverg = difftwoarrays(macddiff,macdavg)
    signmcd = show_sign(macddiverg,'mcd') 
    crossesmcd = show_crossover(signmcd,'mcd')
##    slopemcd = show_slope(macddiverg,'mcd')
    MDarray = makearrayJust2(timestamparray,symarray,durarray,bs,macddiverg,crossesmcd,signmcd)
    array_of_crosses = rpu_rp.grep_array_to_array(MDarray,'cross')
    return array_of_crosses
###################################
def joinArraysStates(timestamparray,indicator,sign,slope):  ## assumes one field in postion 0
    arrayout =[]
    c=0
    while c < len(indicator):
        newline =[]
        f = 0
        flist = [timestamparray,indicator,sign,slope]
        for f in flist:
            newline.append(f[c])
        arrayout.append(newline)
        c+=1
    return arrayout
#################################
def GetStates(arrayin,sym,Indtitle):  #add barr age from last cross here
    decimalboost = dboostdict[sym]
    bs = strip1float(arrayin,5,sym) ##raw close price
    bsopen = strip1float(arrayin,2,sym) ##raw open price
    bshighs = strip1float(arrayin,3,sym)
    bslows = strip1float(arrayin,4,sym)
    bsbardiff = difftwoarrays(bs,bsopen)
    barrange = difftwoarrays(bshighs,bslows)
    timestamparray = strip1string(arrayin,1)
    if Indtitle == 'MACROSS':
        indicator = difftwoarrays(EMAmvavgToArray(bs,9),EMAmvavgToArray(bs,21))
        signindicator = indicator
    elif Indtitle == 'price':
        indicator = bs
        signindicator = bsbardiff
    elif Indtitle == 'MCDiv':
        sma26 = EMAmvavgToArray(bs,26)
        sma12 = EMAmvavgToArray(bs,12)
        macddiff = difftwoarrays(sma12,sma26)
        ## macd is the mvavg9 on this diff
        macdavg = EMAmvavgToArray(macddiff,9)
        macddiverg = difftwoarrays(macddiff,macdavg)
        indicator = macddiverg
        signindicator = indicator
    else:
        print 'unknown indicator'
    sign = show_sign(signindicator,Indtitle) 
    slope = show_slope(indicator,Indtitle) 
    arrayout = joinArraysStates(timestamparray,indicator,sign,slope)
    return arrayout
###################################
###################################
