
def get_sql():
    # If no database exists, generate a database of 101 unique records
    # with names in the form John1 Smith1, John43 Smith43, etc.
    if db(db.person).isempty():
        for eachName in range(5):
    ##        print eachName
            nextNumber=str(eachName)
            db.person.update_or_insert(name='Smith'+nextNumber,address='street'+nextNumber)



    import sqlanydb
    import sqlite3
    user_id = 'dba'
    password = 'sql'
    dbname = 'storage.sqlite' # 'demo' # 'C:\Users\bob\Documents\tradesRPDB.db'
    ##dbfullname = 'tradesRPDB' # 'demo' # 'C:\Users\bob\Documents\tradesRPDB.db'
    ##conn.execute('insert into Login values("%s", "%s")' % \
    ##             (user_id, password))
    ##conn = sqlite3.connect(uid=user_id, pwd=password, eng=dbname, dbn=dbname)
    '''
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("select 'Connected to '")
    print "SQL Anywhere says: %s" % curs.fetchone()
    ############
    sql = 'SELECT sql  FROM sqlite_master WHERE type=\'table\''
    curs.execute(sql)
    arr = (curs.fetchall())
    for l in arr:
        print 'x'
        '''
################
import sqlite3
import pandas as pd
dbname = 'storage.sqlite' # 'demo' # 'C:\Users\bob\Documents\tradesRPDB.db'

def to_csv():
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        print table_name
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_csv(table_name + '.csv', index_label='index')

to_csv()      
