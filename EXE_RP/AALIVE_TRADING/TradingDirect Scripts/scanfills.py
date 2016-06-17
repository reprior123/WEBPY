#############
########def scan_for_fills():
########    openarray = []
########    fillNoProf = []
########    filledNProfSent = []
########    replys = rpu_rp.CsvToLines( TMP + 'entryreplys') ## this reads the replies from the sigcreate login
########    for l in  rpu_rp.CsvToLines(entrysSentFile):
########        if len(l) > 0:
########            print l, 'checking for this in entries with a status poll'
########            status ='open'
########            listordid = l[0]
########            #poll for status
########            tws_conn.orderStatus(listordid)
########            sleep(1) ### give it time to read list
########    ##        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
########            for rep in replys:
########                ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
########                if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
########                    print 'found a fill in entry orders', listordid
########                    status='filled'
########                if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##########                    print 'found a fill in entry orders', listordid
########                    status='cxld'
########            if status  == 'filled':
########                fillNoProf.append(l)
########                pass
########            elif status == 'cxld':
##########                print 'was cxld, deleting from list',l
########                pass
########            else:
########                openarray.append(l)
##########                print 'is open still',l
########    rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
########    rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
########
########    ##########
########def scan_for_fillsfromfile():
########    openarray = []
########    fillNoProf = []
########    filledNProfSent = []
########    replys = rpu_rp.CsvToLines( repliesfile) ## this reads the replies from the sigcreate login
########    status ='open'
########    listordid = parent_order_id
########
##########        filledstring = 'orderStatus orderId='+listordid +', ' status=Filled'
########    for rep in replys:
########        ## CAPTURE FILL PRICE HERE AND USE INSTEAD OF ENTRYPRICE IN FILE
########        if len(rep) > 1 and  rep[1] == ' status=Filled' and rep[0] == '<orderStatus orderId='+listordid:
########            print 'found a fill in entry orders', listordid
########            status='filled'
########        if len(rep) > 1 and  rep[1] == ' status=Cancelled' and rep[0] == '<orderStatus orderId='+listordid:
##########                    print 'found a fill in entry orders', listordid
########            status='cxld'
########    if status  == 'filled':
########        fillNoProf.append(l)
########        pass
########    elif status == 'cxld':
##########                print 'was cxld, deleting from list',l
########        pass
########    else:
########        openarray.append(l)
##########                print 'is open still',l
##########rpu_rp.WriteArrayToCsvfile(entrysSentFile,openarray)
##########rpu_rp.WriteArrayToCsvfile(filledNoProfFile,fillNoProf)
