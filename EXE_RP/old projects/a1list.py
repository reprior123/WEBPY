
############################
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time, openpyxl, zipfile
localtag ='_RNR'
##################2##############
path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = localtag + '/'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash] ### needed to work without tags
import HVARs #rputiles
################################
EXE = rootpath + 'EXE' + localtagSLASH
DATA = rootpath + 'DATA' + localtagSLASH
TMP = rootpath + 'TMP' + localtagSLASH
chooser = DATA + 'ChoosingStocksIssues/'
print chooser
###########################################
nasarea =  rootpath 
SAGE_EXPORTS = TMP
outputarea = TMP
#######################################
import rputiles
fname = chooser + 'symbolsWtiers.csv'
print fname
tdict = rputiles.create_dict(chooser + 'symbolsWtiers.csv',0,1)

a1list = 'AGG.USA,BIV.USA,BLV.USA,BND.USA,BNO.USA,BOIL.USA,BZF.USA,CROC.USA,CVY.USA,CWB.USA,DBEF.USA,DFJ.USA,DSL.USA,DXJ.USA,DXJS.USA,ELD.USA,EMB.USA,EMLC.USA,EWV.USA,EZJ.USA,FORX.USA,FRAK.USA,FXS.USA,GASL.USA,GASX.USA,GAZ.USA,GLDI.USA,HDGE.USA,HEDJ.USA,HYS.USA,IFGL.USA,JJG.USA,JO.USA,JPNL.USA,JPNS.USA,KOLD.USA,KOLD1.USA,LEMB.USA,LTPZ.USA,MBB.USA,MUNI.USA,NIB.USA,OIL.USA,PGX.USA,PTM.USA,REM.USA,RING.USA,SCHP.USA,SCJ.USA,SEA.USA,SJB.USA,TLH.USA,TTT.USA,TTT1.USA,TYD.USA,UBT.USA,UNL.USA,UST.USA,VCIT.USA,VCLT.USA,VPL.USA,WEAT.USA,YCL.USA,ZROZ.USA'
a1list = 'ABR.USA,ACFN.USA,AEC.USA,AEG.USA,AFCE.USA,AMBA.USA,AMWD.USA,ARP.USA,ASA.USA,ASC.USA,AVD.USA,AVIV.USA,BCOV.USA,BEE.USA,BLDP.USA,BNCL.USA,BNNY.USA,BREW.USA,BSMX.USA,BSRR.USA,BTN.USA,CAJ.USA,CAMP.USA,CAP.USA,CBF.USA,CCIX.USA,CCUR.USA,CDW.USA,CLMS.USA,CLNY.USA,COLE.USA,COTY.USA,CSTM.USA,CSV.USA,CUBE.USA,DATA.USA,DFRG.USA,DLLR.USA,DOM.USA,DRD.USA,DRH.USA,DX.USA,EPAX.USA,EVC.USA,EVER.USA,EVTC.USA,FDEF.USA,FET.USA,FLY.USA,FMBI.USA,FN.USA,FRGI.USA,FUBC.USA,FWM.USA,GAIN.USA,GEOS.USA,GEVO.USA,GIFI.USA,GNE.USA,GOGO.USA,GOV.USA,GPT.USA,GST.USA,GTN.USA,HASI.USA,HAWK.USA,HDS.USA,HDSN.USA,HEES.USA,HSII.USA,HTA.USA,HTCH.USA,I.USA,ICAD.USA,IFT.USA,IMKTA.USA,IMPV.USA,ININ.USA,INTL.USA,IRC.USA,IRET.USA,ITC.USA,JONE.USA,KAR.USA,KNOP.USA,KT.USA,KTOS.USA,LINC.USA,LITB.USA,LRE.USA,MCC.USA,MEG.USA,MGEE.USA,MKTG.USA,MKTX.USA,MOVE.USA,MPLX.USA,MRIN.USA,NFBK.USA,NGVC.USA,NPO.USA,NTLS.USA,NWY.USA,NXST.USA,NYMT.USA,ORAN.USA,PAC.USA,PCOM.USA,PEIX.USA,PGEM.USA,PGTI.USA,POWR.USA,PRSC.USA,PSXP.USA,PT.USA,PZE.USA,QIWI.USA,QLTY.USA,RH.USA,RNO.USA,ROYT.USA,RP.USA,RTK.USA,RVLT.USA,SBGI.USA,SEAS.USA,SFM.USA,SGU.USA,SLRC.USA,SMFG.USA,SNBC.USA,SYA.USA,TA.USA,TAM.USA,TCRD.USA,TECUA.USA,TI.USA,TMHC.USA,TRGP.USA,TRST.USA,UGP.USA,UVE.USA,VE.USA,VIPS.USA,VVTV.USA,WETF.USA,WSTC.USA,WWAV.USA,XXIA.USA,YY.USA'

##get line from paramfile w ',V:QuoteEngine' and 'PARAMETER UnderlyingListV' and
##parse out field7 and remove double quotes


a2 = a1list.split(',')
for stock in a2:
    stk = stock.replace('.USA','')
    try:
        print stk, tdict[stk]
    except:
        pass





    
    

