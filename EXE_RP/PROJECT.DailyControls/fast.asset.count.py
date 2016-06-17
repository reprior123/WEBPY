
import os, sys, glob, csv, subprocess, datetime, shutil
path = os.getcwd() + '/'    ### grabs current directory ##
ifile  = open(path + '\Assets.csv', "rb")
reader = csv.reader(ifile)
afile  = open(path + '\Accounts.csv', "rb")
areader = csv.reader(afile)
wfile=open(path + '\AssetsLive.csv', "wb")

w=csv.writer(wfile)

rowcount=0

arowcount=0

for row in reader:

        if rowcount>1:

            afile.seek(0)

            try:

                today=datetime.datetime.today()

                if datetime.datetime.strptime(row[21],"%Y-%m-%d").strftime("%Y%m%d")>today.strftime("%Y%m%d"):

                    for arow in areader:

                        arowcount+=1

                        if arow[0]==row[2]:

                            ###print '%s: %-8s / %-8s' % (datetime.datetime.strptime(row[21],"%Y-%m-%d").strftime("%Y%m%d"),row[12],arow[3])

                            w.writerow([datetime.datetime.strptime(row[21],"%Y-%m-%d").strftime("%Y%m%d"),row[12],arow[3]])

                            val.add(arow[3])

                            break

                    areader.close

            except:

                #####print 'error'

                a=1

        rowcount+=1

rfile=open('C:\Users\dan.sacks\Desktop\EXE\AssetsLive.csv', "rb")

rfile2=open('C:\Users\dan.sacks\Desktop\EXE\AssetsLive.csv', "rb")

wr=csv.reader(rfile)

vallist=[]

for wrow in wr:

        found = False

        for i in vallist:

                try:

                        if i == wrow[2]:

                                found = True

                                break

                except:

                        continue

        try:        

                if found == False:

                        vallist.append(wrow[2])

        except:

                continue

rfile.seek(0)

for i in vallist:

        acount=0

        rfile.seek(0)

        for wrow in wr:

                try:

                        if wrow[2]==i:

                                acount+=1

                except:

                        a=1

        print '%s : %g ' % (i,acount)

 
 
 
 
  
 
 
 
 
 
 

 

 

 
