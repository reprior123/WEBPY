#!/usr/bin/python
"""\
Check.py  Check class for PyCheckbook
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
from Date import *
from CBUtils import string_limit

class Check:
    def __init__(self):
        self.date = Date()
        self.number = None
        self.payee = None
        self.cleared = 0
        self.comment = None
        self.memo = None
        self.amount = None

    def __str__(self):
        str = "%10s " % self.date.formatUS()
        if self.number:
            str = str + "%5d " % self.number
        else:
            str = str + "      "
        str = str + "%-20s " % string_limit(self.payee,20)
        if self.cleared:
            str = str + "x "
        else:
            str = str + "  "
        if self.comment:
            str = str + "%-10s " % string_limit(self.comment,10)
        else:
            str = str + "           "
        if self.memo:
            str = str + "%-10s " % string_limit(self.memo,10)
        else:
            str = str + "           "
        str = str + "%8.2f " % self.amount
        return str

    def lb_repr(self):
        return str(self)

    def __cmp__(self,other):
        return cmp(self.date,other.date)

    def qif_repr(self):
        str = "D%s\n" % self.date.formatUS()
        str = str + "T%.2f\n" % self.amount
        if self.cleared:
            str = str + "Cx\n"
        else:
            str = str + "C*\n"
        if self.number:
            str = str + "N%d\n" % self.number
        str = str + "P%s\n" % self.payee
        if self.comment:
            str = str + "L%s\n" % self.comment
        if self.memo:
            str = str + "M%s\n" % self.memo
        str = str + "^\n"
        return str
            
    def setamount(self,rest):
        words = string.split(rest)
        # some broken qif files have numbers of the form: 1,839.41
        amount = string.replace(words[0], ',', '')
        self.amount = float(amount)
        return 

    def setdate(self,rest):
        self.date = Date(rest)
        return 

    def setpayee(self,rest):
        self.payee = rest
        return

    def setcleared(self,rest):
        if rest[0] == "x":
            self.cleared = 1
        else:
            self.cleared = 0
        return

    def setnumber(self,rest):
        words = string.split(rest)
        if not words:
            self.number = 0
        else:
            self.number = int(words[0])
        return

    def setcomment(self,rest):
        self.comment = rest
        return

    def setmemo(self,rest):
        self.memo = rest
        return

