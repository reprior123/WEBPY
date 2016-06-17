######### VARIABLE TO CHANGE ###############
############################################
FinanceDrive = "C:/Work/test/" ############# <----- Amend this path only
############################################
############################################
FinanceDrive = 'Y:\FINANCE_ALL\INVOICING\\2011_InvoicesINC\December'
print FinanceDrive

#####   DATE SETTINGS   #####
import datetime, shutil, os
path = os.getcwd() + '/'
today = datetime.date.today()
todayf = today.strftime('%Y%m%d')
todaystring = str(todayf)
print todaystring

#####   COPY TO Y:\ DRIVE   #####
filedate = todayf
monthtoday = todayf[0:6]
SfArea = 'Y:\EXE\DATA\INVOICES\\'
sfmonth = SfArea + 'Invoices from ' + todayf
shutil.copytree(FinanceDrive, sfmonth)
print 'WELL DONE'
