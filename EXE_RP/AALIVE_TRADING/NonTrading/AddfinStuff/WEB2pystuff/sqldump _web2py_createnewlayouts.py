# -*- coding: utf-8 -*-
################################
import os, sys, importlib,glob, csv, subprocess, datetime, shutil, time
from time import sleep, strftime, localtime
from datetime import datetime
titleself = (os.path.basename(__file__)).replace('.pyc','')
print titleself
###########
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts,rpu_rp 
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format,sym, symbol_list, symdict
moduleNames = ['rpu_rp'] #open(EXE +'importmodlist.txt').readlines()
for module in moduleNames:
    modulestripped = module.strip()
    if modulestripped != titleself:
##        print '...',modulestripped,'xxx',titleself
        my_module = importlib.import_module(modulestripped)
        pass
    else:
        print 'is self'
######################
## first get the table list you want to use from tablesnfields file....need to make this into csv and clean
basedir = 'C:/WEB2PY/EXE_RP/web2py/applications/'
##appdir = desktop
appdir = basedir +'AddfinV4/'
modelsdir = appdir + 'models/'
def tnamearray():
    tlist = modelsdir + 'tableslist.txt'
    tlistarray = rpu_rp.TxtToLines(modelsdir + 'sugar3_db.py')
    fieldlistarray = rpu_rp.TxtToLines(modelsdir + 'tablesNfields.csv')
    tarray=[]
    farray=[]
    for l in tlistarray:
        if 'db.define_table' in l:
            tname= l.split('\'')[1]
            print tname
            tarray.append(tname)
    return tarray
tarray = tnamearray()
##print tarray
###############
oldword = 'address_book'
#########  this routine writes the basic fields to a table list ####
def write_basicdbase(tname):
    basicfieldsfile = 'basicDbaseFields.csv'
    basiclinesarray = rpu_rp.TxtToLines(basicfieldsfile)
    print 'db.define_table(' + '\'' + tname + '\'' + ','
    countb=0
    for b in basiclinesarray:
        countb +=1
        bs = b.split(',')
        lengthf = bs[3].strip()
        if countb < 4:
            if lengthf =='':
                print 'Field(\''+bs[1].strip()+'\', \''+bs[2].strip()+'\', '+'default=None, required=False),'
                pass
            else:
                print 'Field(\''+bs[1].strip()+'\', \''+bs[2].strip()+'\', '+bs[3].strip()+',default=None, required=False),'
#####################################
def write_fdbase(tname):
    basicfieldsfile = 'basicDbaseFields.csv'
    basicfieldsfile = modelsdir + 'sugar3_db.py'
    basiclinesarray = rpu_rp.TxtToLines(basicfieldsfile)
    countb=0
    tnameloc = ''
    for l in basiclinesarray:
##        print l
        if  'db.define_table' in l:
            tnameloc= l.split('\'')[1]
##            print tnameloc
            countb +=1
        bs = l.split(',')
##        print bs
##            lengthf = bs[3].strip()
        if len(bs) > 3 and tnameloc == tname:
            print ','+tname+','+bs[0].strip()+','+bs[1]+','+bs[2]+',defquired=False),'

#####################################
#### this routine
def copyfiles(oldword,newword):
    newwordplural = newword + 's'
    oldwordplural = oldword + 's'

    viewsdir = appdir +'views/default/'
    viewssugardir = appdir +'views/sugar/'
    oldfile = viewssugardir + 'list_' +  oldword + '.html'
    newfile = viewsdir + 'list_' +  newword + '.html'

    lines = rpu_rp.TxtToLines(oldfile)
    os.system('rm ' + newfile)
    for line in lines:
        newline = line.replace(oldword,newword).replace(oldwordplural,newwordplural)
        rpu_rp.WriteStringsToFileAppend(newfile,newline)
#########################       
def create_controller_menu(t):
    newword = t.strip()
    newwordplural = newword + 's'
    titlename = newword
    lname = 'list_' + titlename
    aword = newword
    print '  [\''+newword +'\',False,url(\'list_'+newword+'\')],'  ## this si for the layout default in views
#############################      
def create_controller_views(t):
    newword = t.strip()
    newwordplural = newword + 's'
    titlename = newword
    lname = 'list_' + titlename
    aword = newword
    print 'def list_'+aword+'():' ## all this for default controller response menu
    print '\tform=crud.create(db.'+aword+' )'
    print '\t'+aword+'=db(db.'+aword+'.id>0).select(orderby=db.'+aword+'.id)'
    print '\treturn dict('+aword+'='+aword+',form=form)'
##############################
for t in tarray:
##    write_basicdbase(t)
##    create_controller_menu(t)
##    create_controller_views(t)
##    copyfiles(oldword,t)
    write_fdbase(t)
###############
    '''

response.menu=[
  ['companies',False,url('list_companies')],
  ['persons',False,url('list_persons')],
  ['kreports',False,url('list_kreports')],
  ['leads',False,url('list_leads')],
]
         #phones
         Field('phone_fax', 'string', length=100,default=None, required=False),
         Field('phone_office', 'string', length=100,default=None, required=False),


TASK_TYPES = ('Phone', 'Fax', 'Mail', 'Meet')

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

   ###########  CONTROLLER LINES
         
this bit for the controller default....:
if not session.recent_companies: session.recent_companies=[]
if not session.recent_persons: session.recent_persons=[]
if not session.recent_tasks: session.recent_tasks=[]
if not session.recent_accounts: session.recent_accounts=[]


db.person.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'person.name')]
db.person.company.requires=IS_IN_DB(db,'company.id','%(name)s')
db.person.phone.requires=is_phone
db.person.fax.requires=is_phone

db.define_table('task',
    Field('person',db.person,default=None),
    Field('start_time','datetime'),
    Field('stop_time','datetime'),
    
db.task.title.requires=IS_NOT_EMPTY()
db.task.task_type.requires=IS_IN_SET(TASK_TYPES)
db.task.person.requires=IS_IN_DB(db,'person.id','%(name)s')
db.task.start_time.default=request.now
db.task.stop_time.default=request.now
    Field('person',db.person),
    Field('body','text'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))
db.log.person.requires=IS_IN_DB(db,'person.id','%(name)s')
db.log.body.requires=IS_NOT_EMPTY()
    Field('person',db.person),
    Field('file','upload'),
db.document.person.requires=IS_IN_DB(db,'person.id','%(name)s')
db.document.name.requires=IS_NOT_EMPTY()
db.document.file.requires=IS_NOT_EMPTY()

'''
