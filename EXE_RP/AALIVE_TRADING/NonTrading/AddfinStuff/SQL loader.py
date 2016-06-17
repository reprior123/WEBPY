# -*- coding: utf-8 -*-
################################
import os, sys
localtag = '_RP'
sys.path[0:0] = [((os.getcwd().replace('EXE','|')).split('|'))[0] + 'EXE' +localtag]
#########################################
import ENVdicts
nd ={}
nd = ENVdicts.ENVdicts(localtag)
for var in nd.keys():
##    print var
    locals()[var] = nd[var]
##################
global timedate_format, nextorderID, date, today,recentlimit, time_format
from time import sleep, strftime, localtime
import  rpu_rp, rpInd, ibutiles, TicksUtile, RP_Snapshot, glob, csv, subprocess, datetime, shutil, time, BarUtiles
from time import sleep, strftime, localtime
import RulesEngine
from datetime import datetime
import ctypes
######################
from ib.ext.Contract import Contract  
from ib.opt import ibConnection, message
from ib.ext.Order import Order
from ib.opt import Connection, message   ##??
#############################
global  sym, symbol_list, symdict
########################################
import sqlanydb
user_id = 'dba'
password = 'sql'
dbname = 'tradesRPDB' # 'demo' # 'C:\Users\bob\Documents\tradesRPDB.db'
##conn.execute('insert into Login values("%s", "%s")' % \
##             (user_id, password))
conn = sqlanydb.connect(uid=user_id, pwd=password, eng=dbname, dbn=dbname)
curs = conn.cursor()
curs.execute("select 'Connected to '")
print "SQL Anywhere says: %s" % curs.fetchone()
print dbname

## if no database file specified error, mysql is not running....!!
## login ro trades RPDB in sqlanywhere console tool...is in documents area
tablename = 'Persons' #'tradesdbase'
tablename = 'Barssdbase'
# Execute a SQL string
sql = 'SELECT * FROM ' + tablename +' '
curs.execute(sql)
##################
def show_data(tname):
    # Get a cursor description which contains column names
    desc = curs.description
    ##for x in desc:
    ##    print x
    ##    for b in x:
    ##        print b
    ####print desc
    print len(desc)
    # Fetch all results from the cursor into a sequence, 
    # display the values as column name=value pairs,
    sql = 'SELECT * FROM ' + tname +' '
    curs.execute(sql)
    rowset = curs.fetchall()
    print rowset
    print rowset
    for row in rowset:
        for col in range(len(desc)):
            print "%s=%s" % (desc[col][0], row[col] )
#####################################
def create_table(tname,numfields):
    field1 = 'TickID'
    field2 = 'Sym'
    field3 = 'timedate'
    field4 = 'POpen'
    field5 = 'PClose'
    field6 = 'PHigh'
    field7 = 'PLow'
    field8 = 'barstatus'
    field9 = 'volume'
    field10 ='tickcount'    
    curs.execute('DROP TABLE IF EXISTS '+ tname)
##    print 'got here'
    sql = 'CREATE TABLE '+tname + '('+\
    field1 + ' int,' +\
    field2 + ' varchar(255),' +\
    field3 + ' varchar(255),' +\
    field4 + ' varchar(255),' +\
    field5 + ' varchar(255),' +\
    field6 + ' varchar(255),' +\
    field7 + ' varchar(255),' +\
    field8 + ' varchar(255),' +\
    field9 + ' varchar(255),' +\
    field10 + ' varchar(255),' +\
    ')'
    curs.execute(sql)
##############################################
#####################################
def create_BARStable(tname,numfields):
    fieldlist = ['TickID','Sym','timedate','POpen','PClose' ,\
                 'PHigh', 'PLow' ,'barstatus' , 'volume' , 'tickcount' ,'bardur' , 'barday']
    c=0
    fdict = {}
    curs.execute('DROP TABLE IF EXISTS '+ tname)
    sqlfstring = 'CREATE TABLE '+tname + '('
    endstring = ')'
    while c < len(fieldlist) :
        fdict[c]  = str(fieldlist[c])  ### this uses a string
        ftype= ' varchar(255),'
        if c==0:
            ftype =' int,'
        sqlfstring += str(fieldlist[c]) + ftype
        print c,fieldlist[c],ftype
        c+=1
        finalstring = sqlfstring +endstring
    curs.execute(finalstring)
    print 'just created table ', tname, ' if not already there'

##############################################
def insertLoop(tname,numfields):
    fieldlist = ['TickID','Sym','timedate','POpen','PClose' ,\
                 'PHigh', 'PLow' ,'barstatus' , 'volume' , 'tickcount' ,'bardur' , 'barday']
    c=0
    fdict = {}
    sqlfstring1 = 'INSERT INTO '+ tname +'('
    sqlfstring2 =''
    endstring = ')'
    while c < len(fieldlist) :
        fdict[c]  = str(fieldlist[c])  
        datainsert = 'blastring'
        if c!=len(fieldlist)-1:
            comma = ', '
            comma2 = comma
            pass
        else:
            comma =') VALUES  ('
            comma2 =')'
        sqlfstring1 += str(fieldlist[c]) + comma
        sqlfstring2 += datainsert + comma2 
        print c,fieldlist[c],comma2
        c+=1
        finalstring = sqlfstring1 + sqlfstring2 
        print finalstring
    print len(fieldlist)
    curs.execute(finalstring)
    print 'just inserted records table ', tname, ' if not already there'
##############################################        
def insert_records(tname,records):
    print 'inserting records....'
    field1 = 'TickID'
    field2 = 'Sym'
    field3 = 'timedate'
    field4 = 'POpen'
    field5 = 'PClose'
    field6 = 'PHigh'
    field7 = 'PLow'
    field8 = 'barstatus'
    field9 = 'volume'
    field10 ='tickcount'

    field1data = '8888'
    field2data = '8888'
    sql = 'INSERT INTO '+ tname +'('+ field1+', ' + field2+') VALUES  (' + field1data + ', ' + field2data+ ')'
    curs.execute(sql)    
##    sql = 'INSERT INTO '+ tname +'('+ field1 + ', ' + field2 + ', ' + field3 + ', ' + field4 + ' ) VALUES  (%d, %s, %s, %s)' %\
##    (1, field1, field2, field3)
##    curs.execute(sql)
    trades = [(1,'2','3','4','5','6','7','8','9','1'),(1,'2','3','4','5','6','7','8','9','1')]
##    sql = ('INSERT INTO '+ tname +' VALUES (?,?,?,?,?,?,?,?,?,?)')
##    curs.executemany(sql,trades)
    conn.commit()
############################
def updated_records(tname):
    symdata = 'newsym'
    tdata = 'time item'
    curs.execute ('UPDATE '+tname+' SET Sym=%s, timedate=%s, WHERE TickID=%s', (symdata,tdata, 1))
    conn.commit()
##################
##    '('%d', '%s', '%s', '%c', '%d' )" % \
###########
records =[]
tname = tablename
##show_data(tname)
##insert_records(tname,records)
insertLoop('Barssdbase',records)
create_BARStable('Barssdbase',10)
####show_data(tname)
####updated_records(tname)
##########################
curs.close()
conn.close()

'''
##    field5 + ', ' +\
##    field6 + ', ' +\
##    field7 + ', ' +\
##    field8 + ', ' +\
##    field9 + ', ' +\
##    field10 + \

$$$$$$$$$$$$
INSERT Operation
It is required when you want to create your records into a database table.
Example
The following example, executes SQL INSERT statement to create a record into EMPLOYEE table −
# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES \
       ('%s', '%s', '%d', '%c', '%d' )" % \
       ('Mac', 'Mohan', 20, 'M', 2000)

READ Operation on any database means to fetch some useful information from the database.
Once our database connection is established, you are ready to make a query into this database.
fetchone(): It fetches the next row of a query result set.
A result set is an object that is returned when a cursor object is used to query a table.
fetchall(): It fetches all the rows in a result set. If some rows have already been extracted from the result set, then it retrieves the remaining rows from the result set.
rowcount: This is a read-only attribute and returns the number of rows that were affected by an execute() method.

Example
The following procedure queries all the records from EMPLOYEE table having salary more than 1000 −
# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > '%d'" % (1000)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # Now print fetched result
      print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
             (fname, lname, age, sex, income )
except:
   print "Error: unable to fecth data"
#############################################
UPDATE Operation on any database means to update one or more records, which are already available in the database.
Example
# Prepare SQL query to UPDATE required records

sql = "UPDATE EMPLOYEE SET AGE = AGE + 1
                          WHERE SEX = '%c'" % ('M')

sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
DELETE Operation
DELETE operation is required when you want to delete some records from your database. Following is the procedure to delete all the records from EMPLOYEE where AGE is more than 20 −

Example
# Prepare SQL query to DELETE required records

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
Performing Transactions
Transactions are a mechanism that ensures data consistency. Transactions have the following four properties:

Atomicity: Either a transaction completes or nothing happens at all.

Consistency: A transaction must start in a consistent state and leave the system in a consistent state.

Isolation: Intermediate results of a transaction are not visible outside the current transaction.

Durability: Once a transaction was committed, the effects are persistent, even after a system failure.

The Python DB API 2.0 provides two methods to either commit or rollback a transaction.

Example
You already know how to implement transactions. Here is again similar example −

# Prepare SQL query to DELETE required records
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
COMMIT Operation
Commit is the operation, which gives a green signal to database to finalize the changes, and after this operation, no change can be reverted back.

Here is a simple example to call commit method.

 db.commit()
ROLLBACK Operation
If you are not satisfied with one or more of the changes and you want to revert back those changes completely, then use rollback() method.

Here is a simple example to call rollback() method.

 db.rollback()
Disconnecting Database
To disconnect Database connection, use close() method.

 db.close()
If the connection to a database is closed by the user with the close() method, any outstanding transactions are rolled back by the DB. However, instead of depending on any of DB lower level implementation details, your application would be better off calling commit or rollback explicitly.

Handling Errors
There are many sources of errors. A few examples are a syntax error in an executed SQL statement, a connection failure, or calling the fetch method for an already canceled or finished statement handle.

The DB API defines a number of errors that must exist in each database module. The following table lists these exceptions.

Exception	Description
Warning	Used for non-fatal issues. Must subclass StandardError.
Error	Base class for errors. Must subclass StandardError.
InterfaceError	Used for errors in the database module, not the database itself. Must subclass Error.
DatabaseError	Used for errors in the database. Must subclass Error.
DataError	Subclass of DatabaseError that refers to errors in the data.
OperationalError	Subclass of DatabaseError that refers to errors such as the loss of a connection to the database. These errors are generally outside of the control of the Python scripter.
IntegrityError	Subclass of DatabaseError for situations that would damage the relational integrity, such as uniqueness constraints or foreign keys.
InternalError	Subclass of DatabaseError that refers to errors internal to the database module, such as a cursor no longer being active.
ProgrammingError	Subclass of DatabaseError that refers to errors such as a bad table name and other things that can safely be blamed on you.
NotSupportedError	Subclass of DatabaseError that refers to trying to call unsupported functionality.
Your Python scripts should handle these errors, but before using any of the above exceptions, make sure your MySQLdb has support for that exception. You can get more information about them by reading the DB API 2.0 specification.

##################################################



Inserting rows
The simplest way to insert rows into a table is to use a non-parameterized INSERT statement, meaning that values are specified as part of the SQL statement. A new statement is constructed and executed for each new row. As in the previous example, a cursor is required to execute SQL statements.
The following sample program inserts two new customers into the sample database. Before disconnecting, it commits the transactions to the database.
import sqlanydb

# Create a connection object, then use it to create a cursor
con = sqlanydb.connect( userid="DBA", pwd="sql" )
cursor = con.cursor()
cursor.execute("DELETE FROM Customers WHERE ID > 800")

rows = ((801,'Alex','Alt','5 Blue Ave','New York','NY',
        'USA','10012','5185553434','BXM'),
        (802,'Zach','Zed','82 Fair St','New York','NY',
        'USA','10033','5185552234','Zap'))

# Set up a SQL INSERT
parms = ("'%s'," * len(rows[0]))[:-1]
sql = "INSERT INTO Customers VALUES (%s)" % (parms)
print sql % rows[0]
cursor.execute(sql % rows[0]) 
print sql % rows[1]
cursor.execute(sql % rows[1]) 
cursor.close()
con.commit()
con.close()
Copy example
An alternate technique is to use a parameterized INSERT statement, meaning that question marks are used as place holders for values. The executemany method is used to execute an INSERT statement for each member of the set of rows. The new row values are supplied as a single argument to the executemany method.
import sqlanydb

# Create a connection object, then use it to create a cursor
con = sqlanydb.connect( userid="DBA", pwd="sql" )
cursor = con.cursor()
cursor.execute("DELETE FROM Customers WHERE ID > 800")

rows = ((801,'Alex','Alt','5 Blue Ave','New York','NY',
        'USA','10012','5185553434','BXM'),
        (802,'Zach','Zed','82 Fair St','New York','NY',
        'USA','10033','5185552234','Zap'))

# Set up a parameterized SQL INSERT
parms = ("?," * len(rows[0]))[:-1]
sql = "INSERT INTO Customers VALUES (%s)" % (parms)
print sql
cursor.executemany(sql, rows)  
cursor.close()
con.commit()
con.close()
Copy example
Although both examples may appear to be equally suitable techniques for inserting row data into a table, the latter example is superior for a couple of reasons. If the data values are obtained by prompts for input, then the first example is susceptible to injection of rogue data including SQL statements. In the first example, the execute method is called for each row to be inserted into the table. In the second example, the executemany method is called only once to insert all the rows into the table.
############
##########
Once you have obtained a handle to an open connection, you can access and modify data stored in the database. Perhaps the simplest operation is to retrieve some rows and print them out.
The cursor method is used to create a cursor on the open connection. The execute method is used to create a result set. The fetchall method is used to obtain the rows in this result set.
import sqlanydb

# Create a connection object, then use it to create a cursor
con = sqlanydb.connect( userid="DBA", 
                        password="sql" )
cursor = con.cursor()

# Execute a SQL string
sql = "SELECT * FROM Employees"
cursor.execute(sql)

# Get a cursor description which contains column names
desc = cursor.description
print len(desc)

# Fetch all results from the cursor into a sequence, 
# display the values as column name=value pairs,
# and then close the connection
rowset = cursor.fetchall()
for row in rowset:
    for col in range(len(desc)):
        print "%s=%s" % (desc[col][0], row[col] )
    print
cursor.close()
con.close()
##############
Converter Functions

This library wraps around the sqlanydb dbcapi C library. When retrieving values from the database, the C API returns one of these types:

A_INVALID_TYPE
A_BINARY
A_STRING
A_DOUBLE
A_VAL64
A_UVAL64
A_VAL32
A_UVAL32
A_VAL16
A_UVAL16
A_VAL8
A_UVAL8
Other types are returned as the above types. For example, the NUMERIC type is returned as a string.

To have sqlanydb return a different or custom python object, you can register callbacks with the sqlanydb module, using register_converter(datatype, callback). Callback is a function that takes one argument, the type to be converted, and should return the converted value. Datatype is one of the DT_ variables present in the module.

The types available to register a converter for:

DT_NOTYPE
DT_DATE
DT_TIME
DT_TIMESTAMP
DT_VARCHAR
DT_FIXCHAR
DT_LONGVARCHAR
DT_STRING
DT_DOUBLE
DT_FLOAT
DT_DECIMAL
DT_INT
DT_SMALLINT
DT_BINARY
DT_LONGBINARY
DT_TINYINT
DT_BIGINT
DT_UNSINT
DT_UNSSMALLINT
DT_UNSBIGINT
DT_BIT
DT_LONGNVARCHAR
For example, to have NUMERIC types be returned as a python Decimal object:

import decimal

def decimal_callback(valueToConvert):
    return decimal.Decimal(valueToConvert)

sqlanydb.register_converter(sqlanydb.DT_DECIMAL, decimal_callback)
'''
