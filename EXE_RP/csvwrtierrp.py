#!/usr/bin/python
#-*- coding: latin-1 -*-
import sys
print 'loading rpu'
import os, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile
############################
print 'rpudone loaded'
localtag = '_RP'
import ENVvars
nd ={}
nd = ENVvars.ENVvars(localtag)
##resolve vardict back to normal variables
for var in nd.keys():
    locals()[var] = nd[var]
####################################
####import openpyxl 
yesterdayoffset = 1
from datetime import date, timedelta
today = datetime.date.today()
yesterday = datetime.date.today() - timedelta(yesterdayoffset)
todayf = today.strftime(date_format)
todayfunix = today.strftime(unix_format)
todayspaceY = today.strftime(spaceY_format)
yesterdayf = yesterday.strftime(date_format)
yesterdayfunix = yesterday.strftime(unix_format)
todaydir = DATA + todayfunix
import datetime
## time functions ##
timenow = time.strftime(unixmin_format)
#####################################
import csv, codecs, cStringIO
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")
class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
rows= [['wwww','eee'],['rrrr']]
tfile =open('bla','w')

writer = UnicodeWriter(tfile)
writer.writerows(rows)
tfile.close()
##############
def WriteArrayToCsvfile(fileoutname, arrayname):
    targetcsvfile = open(fileoutname,'wb')
    filecsvwriter = csv.writer(targetcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    for row in arrayname:
        filecsvwriter.writerow(row)
    targetcsvfile.close()
