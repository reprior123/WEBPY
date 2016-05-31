# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

##error_page=URL('error')
##
##if not session.recent_companies: session.recent_companies=[]
##if not session.recent_persons: session.recent_persons=[]
##
##
##response.menu=[
##  ['Companies',False,url('list_companies')],
##  ['Contacts',False,url('list_persons')],
##  ['Tasks',False,url('list_tasks')],
##]


def index():
    return dict()

###########################
def addrecordpersons():
    import sqlite3
    import rpu_rp
    # If no database exists, generate a database of 101 unique records
    # with names in the form John1 Smith1, John43 Smith43, etc.
######    if db(db.person).isempty():
######        for eachName in range(5):
######    ##        print eachName
######            nextNumber=str(eachName)
######            db.person.update_or_insert(name='Smith'+nextNumber,address='street'+nextNumber)
##    import sqlanydb    
##    import pandas as pd

    user_id = 'dba'
    password = 'sql'
    maindir = ''#'C:/Users/bob/Google Drive/Drive/EXE_RP/web2py/applications/crmraw/databases/'
    dbname = maindir + 'storage.sqlite'
    print dbname
    db = sqlite3.connect(dbname)
    ################
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    tabinfo = str(tables)
    alltabs =''
    print tabinfo
    for table_name in tables:
        table_name = table_name[0]
        print table_name,'ddddd'
        stringc = 'SELECT * from ' + table_name + ' '

        cursor.execute(stringc)
##        cursor.execute("SELECT * from %s" % table_name, db)
        tabinfo = cursor.fetchall()

        rpu_rp.WriteArrayToCsvfile(table_name + '.csv',tabinfo)
        alltabs += str(tabinfo)
##        table.to_csv(table_name + '.csv', index_label='index')
    return alltabs
##    return dict(index=index)
##addrecordpersons()
