#!/usr/bin/python
"""\
Date.py  Simple Date class for PyCheckbook
Copyright (c) 2000, Richard P. Muller. All rights reserved. 

This code is in development -- use at your own risk. Email
comments, patches, complaints to rpm@wag.caltech.edu.

This program is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation; either version 2 
of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
GNU General Public License for more details. 

You should have received a copy of the GNU General Public License 
along with this program; if not, write to the Free Software 
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

Change Log:
1/13/01   Fixed a bug in parse_datestring; now can either enter no date,
          month/day, or month/day/year and the program responds
          intelligently.
"""

import string,time

class Date:
    def __init__(self,datestring=None):
        self.year = 0
        self.month = 0
        self.day = 0
        if datestring:
            self.parse_datestring(datestring)
        else:
            self.set_today()

    def __cmp__(self,other):
        val = cmp(self.year,other.year)
        if val:
            return val
        val = cmp(self.month,other.month)
        if val:
            return val
        val = cmp(self.day,other.day)
        return val

    def __str__(self):
        return self.formatUS()

    def formatUS(self):
        return "%02d/%02d/%02d" % (self.month,self.day,self.year2digit())

    def year2digit(self):
        if self.year >= 2000:
            return self.year - 2000
        return self.year - 1900

    def parse_datestring(self,datestring):
        # set the date to today, then overwrite if more data
        today = Date()
        month,day,year = today.month, today.day, today.year
        
        words = string.split(datestring,'/')
        if len(words) == 3:
            month,day,year = int(words[0]),int(words[1]),int(words[2])
        elif len(words) == 2:
            month,day = int(words[0]),int(words[1])
        # Don't support any other options
            
        if month > 12 or month < 1:
            print "Error: Bad month: %d/%d/%d " % (month,day,year)
        if year < 10:
            year = year + 2000
        elif year < 100:
            year = year + 1900
        elif year < 1970:
            print "Error: Bad year: %d/%d/%d " % (month,day,year)

        self.year = year
        self.month = month
        self.day = day
        return
        

    def set_today(self):
        today = time.localtime(time.time())
        self.year = today[0]
        self.month = today[1]
        self.day = today[2]
        return
    
if __name__ == '__main__':
    today = Date()
    print today
