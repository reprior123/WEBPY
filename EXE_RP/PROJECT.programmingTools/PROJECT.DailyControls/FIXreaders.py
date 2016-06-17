import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,loop_filedate_names
############################
path = os.getcwd() + '/'
test = path + 'test/'
SageOut = path + 'SageOut/'
drivelet = path[0]
datapath = drivelet + ':/'
TMP = datapath + 'TMP/'
EXE = datapath + 'EXE/'
##########
DATA = datapath + 'DATA/'
dataarea = DATA + 'SFDATA/'
##################2##############
##def mainVariables():
##    TMP = datapath + 'TMP/'
    ####################



##
##
##Tag	 Field	 Value	 Description
##8	BeginString	FIX.4.2	
##9	BodyLength	331	
##35	MsgType	8	Execution Report
##34	MsgSeqNum	001438	
##43	PossDupFlag	N	Original transmission
##49	SenderCompID	IB	
##52	SendingTime	20130411-17:49:19	
##56	TargetCompID	actant	
##128	DeliverToCompID	ACTANT	
##1	Account	U163194	
##6	AvgPx	0	
##11	ClOrdID	RP1130411000008	
##14	CumQty	0	
##15	Currency	USD	
##17	ExecID	108922.1365702559.1	
##20	ExecTransType	0	New
##31	LastPx	0.00	
##32	LastQty	0	
##37	OrderID	00094eac.0001a97a.51663b5e.0001	
##38	OrderQty	1	
##39	OrdStatus	0	New
##40	OrdType	2	Limit
##44	Price	1590.75	
##54	Side	2	Sell
##55	Symbol	ES	
##60	TransactTime	20130411-17:49:19	
##77	PositionEffect	C	Close
##109		actant	
##150	ExecType	0	New
##151	LeavesQty	1	
##167	SecurityType	FUT	Future
##200	MaturityMonthYear	201306	
##204		0	
##440		U163194	
##6122		c	
##6722		ACTANT	
##10		142
##
##






