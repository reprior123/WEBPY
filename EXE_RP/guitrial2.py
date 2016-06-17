# -*- coding: utf-8 -*-
#########################################
import os, sys, glob, csv, subprocess, datetime, shutil, subprocess, time,  zipfile

path = os.getcwd() + '/'
rootpath = ((path.replace('EXE','|')).split('|'))[0]
localtagSLASH = '_RP/'
localtag = '_RP'
EXEnoslash = rootpath + 'EXE' + localtag
sys.path[0:0] = [EXEnoslash]
Cpath = 'C:/'
################
##############localtag = '_RP'
##############import ENVvars
##############nd={}
##############nd = ENVvars.ENVvars(localtag)
################resolve vardict back to normal variables
##############for var in nd.keys():
##############    locals()[var] = nd[var]
import stat,md5

import rpu_rp
from datetime import datetime
import datetime as dt
################################
import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
############################################

class SimpleExample1(BaseWidget):

    def __init__(self):
        super(SimpleExample1,self).__init__('Simple example 1')

        #Definition of the forms fields
        self._firstname     = ControlText('First name', 'Default value')
        self._middlename    = ControlText('Middle name')
        self._lastname      = ControlText('Lastname name')
        self._fullname      = ControlText('Full name')
        self._button        = ControlButton('Press this button')

        #Define the button action
        self._button.value = self.__buttonAction
        self._formset = ['_firstname','_middlename','_lastname', '_fullname', '_button', ' ']


    def __buttonAction(self):
        """Button action event"""
        self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
        " "+ self._lastname.value


 #Add this line to the constructor and you will be able to organize the forms.
    ###################################
#Execute the application
if __name__ == "__main__":   pyforms.startApp( SimpleExample1 )
