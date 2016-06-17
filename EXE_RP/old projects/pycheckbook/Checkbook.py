#!/usr/bin/python
"""\
Checkbook.py  Checkbook class for PyCheckbook
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
"""

import string
from Check import *

class Checkbook:
    def __init__(self,filename = None):
        self.name = ''
        self.filename = None
        self.checks = []
        self.total = 0.
        if filename:
            self.read_qif(filename)
        return

    def __len__(self):
        return len(self.checks)

    def __getitem__(self,i):
        return self.checks[i]

    def __setitem__(self,i,val):
        self.checks[i] = val
        return

    def __str__(self):
        return " %-10s $%8.2f\n" % (self.name,self.total)

    def __delitem__(self,i):
        del self.checks[i]
        return

    def append(self,item):
        self.checks.append(item)
        return

    def read_qif(self,filename,readmode='normal'):
        if readmode=='normal':
            self.filename = filename
        recs = self.checks
        self.name = string.replace(filename,'.qif','')
        file = open(filename,'r')
        lines = file.readlines()
        file.close()
        check = Check()
        type = lines.pop(0)
        for line in lines:
            type,rest = line[0],string.strip(line[1:])
            if type == "D":
                check.setdate(rest)
            elif type == "T":
                check.setamount(rest)
            elif type == "P":
                check.setpayee(rest)
            elif type == "C":
                check.setcleared(rest)
            elif type == "N":
                check.setnumber(rest)
            elif type == "L":
                check.setcomment(rest)
            elif type == "M":
                check.setmemo(rest)
            elif type == "^":
                recs.append(check)
                self.total = self.total + check.amount
                check = Check()
            else:
                print "Unparsable line: ",line[:-1]
        self.checks.sort()
        return

    def write_qif(self,filename=None):
        if not filename:
            if not self.filename:
                NoFileError = "Don't have a checkbook filename defined"
                raise NoFileError
            filename = self.filename
        self.filename = filename
        file = open(filename,'w')
        file.write("%s" % self.qif_repr())
        file.close()
        return

    def write_txt(self):
        filename = 'pycb.txt'
        file = open(filename,'w')
        file.write("%s" % self.long_repr())
        file.close()
        return

    def long_repr(self):
        repr = ''
        for check in self.checks:
            repr = repr + str(check) + "\n"
        return repr

    def qif_repr(self):
        str = 'Type:Bank\n'
        for check in self.checks:
            str = str + check.qif_repr() 
        return str

