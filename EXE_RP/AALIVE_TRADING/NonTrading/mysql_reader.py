# -*- coding: utf-8 -*-

import MySQLdb
from os import getenv
##import pymssql

user_id = 'mysql'
password = 'xxx'
heredir = 'C:/Users/bob/Google Drive/EXE_RP/AALIVE_TRADING/NonTrading/'
dbname = 'addfinnewdb'
dbserver = getenv(dbname)
print dbserver
##dbnamefull = heredir +dbname
print dbname
##lhost =  heredir
##lhost = '127.0.0.1:3306'
##lhost = '127.0.0.1:/xampp/mysql'
lhost = '127.0.0.1'
##conn.execute('insert into Login values("%s", "%s")' % \

##conn = MySQLdb.connect(uid=user_id, pwd=password, eng=dbname, dbn=dbname)
conn = MySQLdb.connect( host = lhost,user = user_id, db = dbname)
##conn = MySQLdb.connect( host=lhost, db=dbname)

######import mysql.connector
######cnx = mysql.connector.connect(user='scott', password='tiger', host='127.0.0.1',database='employees')
######cnx.close()

##conn = MySQLdb.connect(host='localhost',user = user_id,passwd =  password, db =  dbname)
##conn = MySQLdb.connect(dbnamefull,user_id,password,dbn)
##conn = pymssql.connect('localhost',user_id,password,dbname)
##conn = pymssql.connect(host=heredir,user=user_id,password=password,database=dbname)
##conn = sqlite3.connect('localhost',user_id, password, heredir +dbname)
##conn = sqlanydb.connect(uid=user_id, pwd=password, eng=dbnamefull, dbn=dbnamefull)
##conn = sqlanydb.connect(dbnamefull)
##conn = MySQLdb.connect(dbnamefull)

cursor = conn.cursor()
##cursor.execute("select 'Connected to '")
##print "SQL Anywhere says: %s" % cursor.fetchone()
print dbname
############
sql = 'SELECT sql  FROM sqlite_master WHERE type=\'table\''
cursor.execute(sql)
arr = (cursor.fetchall())
for l in arr:
    print 'x'
# execute SQL query using execute() method.
##cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# disconnect from server
db.close()



##sql = 'SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE=\'BASE TABLE\''
sql = 'SELECT sql  FROM sqlite_master WHERE type=\'table\''
##sql = 'SELECT .tables  FROM sqlite_master ' #WHERE type=\'table\''
##sql = '.tables'

curs.execute(sql)
arr = (curs.fetchall())
for l in arr:
    print 'x'

##with open('dump.sql', 'w') as f:
##    for line in conn.iterdump():
##        f.write('%s\n' % line)
##        print line



import sqlite3
import pandas as pd

##dbname = 'storagenewxxxx' # 'demo' # 'C:\Users\bob\Documents\tradesRPDB.db'

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
'''
tablename = 'Persons' #'tradesdbase'
tablename = 'tradesdbase'
# Execute a SQL string
sql = 'SELECT * FROM ' + tablename +' '
curs.execute(sql)
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
# and then close the connection
rowset = curs.fetchall()
for row in rowset:
    for col in range(len(desc)):
        print "%s=%s" % (desc[col][0], row[col] )
    print
#####################################
def createtable(tname,numfields):
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
createtable('tradesdbase',10)
###########
curs.close()
conn.close()

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
fetchone(): It fetches the next row of a query result set. A result set is an object that is returned when a cursor object is used to query a table.
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
There are many sources of errors. A few examples are a syntax error in an executed SQL statement,
a connection failure, or calling the fetch method for an already canceled or finished statement handle.

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

The simplest way to insert rows into a table is to use a non-parameterized
INSERT statement, meaning that values are specified as part of the SQL statement.
A new statement is constructed and executed for each new row. As in the previous
example, a cursor is required to execute SQL statements.
The following sample program inserts two new customers into the sample database.
Before disconnecting, it commits the transactions to the database.
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
An alternate technique is to use a parameterized INSERT statement,
meaning that question marks are used as place holders for values.
The executemany method is used to execute an INSERT statement for
each member of the set of rows. The new row values are supplied as
a single argument to the executemany method.
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
Although both examples may appear to be equally suitable techniques for
inserting row data into a table, the latter example is superior for
a couple of reasons. If the data values are obtained by prompts for input,
then the first example is susceptible to injection of rogue data including
SQL statements. In the first example, the execute method is called for each
row to be inserted into the table. In the second example, the executemany
method is called only once to insert all the rows into the table.
############
##########
Once you have obtained a handle to an open connection,
you can access and modify data stored in the database.
Perhaps the simplest operation is to retrieve some rows and print them out.
The cursor method is used to create a cursor on the open
connection. The execute method is used to create a result set.
The fetchall method is used to obtain the rows in this result set.
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

This library wraps around the sqlanydb dbcapi C library.
When retrieving values from the database, the C API returns
one of these types:

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
Other types are returned as the above types.
For example, the NUMERIC type is returned as a string.

To have sqlanydb return a different or custom python object,
you can register callbacks with the sqlanydb module, using
register_converter(datatype, callback). Callback is a function
that takes one argument, the type to be converted, and should return
the converted value. Datatype is one of the DT_ variables present in the module.

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
################
'''
SQLite

SQLite is a simple relational data base system, which saves its data in regular data files or even in the internal memory of the computer, i.e. the RAM. It was developped for embedded applications, like Mozilla-Firefox (Bookmarks), Symbian OS or Android. SQLITE is "quite" fast, even though it uses a simple file. It can be used for large data bases as well. If you want to use SQLite, you have to import the module sqlite3. To use a database, you have to create first a Connection object. The connection object will represent the database. The argument of connection - in the following example "companys.db" - functions both as the name of the file, where the data will be stored, and as the name of the database. If a file with this name exists, it will be opened. It has to be a SQLite database file of course! In the following example, we will open a database called company. The file does not have to exist.: 
>>> import sqlite3
>>> connection = sqlite3.connect("company.db")

We have now created a database with the name "company". It's like having sent the command "CREATE DATABASE company;" to a SQL server. If you call "sqlite3.connect('company.db')" again, it will open the previously created database. 

After having created an empty database, you will most probably add one or more tables to this database. The SQL syntax for creating a table "employee" in the database "company" looks like this:
CREATE TABLE employee ( 
staff_number INT NOT NULL AUTO_INCREMENT, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE,
birth_date DATE,  
PRIMARY KEY (staff_number) );
This is the way, somebody might do it on a SQL command shell. Of course, we want to do this directly from Python. To be capable to send a command to "SQL", or SQLite, we need a cursor object. Usually, a cursor in SQL and databases is a control structure to traverse over the records in a database. So it's used for the fetching of the results. In SQLite (and other Python DB interfaces)it is more generally used. It's used for performing all SQL commands. 

We get the cursor object by calling the cursor() method of connection. An arbitrary number of cursors can be created. The cursor is used to traverse the records from the result set. A complete Python program for creating a database company and creating an employee table looks like this:
sql_command = """
CREATE TABLE employee ( 
staff_number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE,
birth_date DATE);"""
Concerning the SQL syntax: You may have noticed that the AUTOINCREMENT field is missing in the SQL code within our Python program. We have defined the staff_number field as "INTEGER PRIMARY KEY" A column which is labelled like this will be automatically auto-incremented in SQLite3. To put it in other words: If a column of a table is declared to be an INTEGER PRIMARY KEY, then whenever a NULL will be used as an input for this column, the NULL will be automatically converted into an integer which will one larger than the highest value so far used in that column. If the table is empty, the value 1 will be used. If the largest existing value in this column has the 9223372036854775807, which is the largest possible INT in SQLite, an unused key value is chosen at random. 

Now we have a database with a table but no data included. To populate the table we will have to send the "INSERT" command to SQLite. We will use again the execute method. The following example is a complete working example. To run the program you will either have to remove the file company.db or uncomment the "DROP TABLE" line in the SQL command: 

import sqlite3
connection = sqlite3.connect("company.db")

cursor = connection.cursor()

# delete 
#cursor.execute("""DROP TABLE employee;""")

sql_command = """
CREATE TABLE employee ( 
staff_number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE,
birth_date DATE);"""

cursor.execute(sql_command)

sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    VALUES (NULL, "William", "Shakespeare", "m", "1961-10-25");"""
cursor.execute(sql_command)


sql_command = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17");"""
cursor.execute(sql_command)

# never forget this, if you want the changes to be saved:
connection.commit()

connection.close()
Of course, in most cases, you will not literally insert data into a SQL table. You will rather have a lot of data inside of some Python data type e.g. a dictionary or a list, which has to be used as the input of the insert statement. 

The following working example, assumes that you have already an existing database company.db and a table employee. We have a list with data of persons which will be used in the INSERT statement:
import sqlite3
connection = sqlite3.connect("company.db")

cursor = connection.cursor()

staff_data = [ ("William", "Shakespeare", "m", "1961-10-25"),
               ("Frank", "Schiller", "m", "1955-08-17"),
               ("Jane", "Wall", "f", "1989-03-14") ]
               
for p in staff_data:
    format_str = """INSERT INTO employee (staff_number, fname, lname, gender, birth_date)
    VALUES (NULL, "{first}", "{last}", "{gender}", "{birthdate}");"""

    sql_command = format_str.format(first=p[0], last=p[1], gender=p[2], birthdate = p[3])
    cursor.execute(sql_command)

The time has come now to finally query our employee table: 

import sqlite3
connection = sqlite3.connect("company.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM employee") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM employee") 
print("\nfetch one:")
res = cursor.fetchone() 
print(res)
If we run this program, saved as "sql_company_query.py", we get the following result, depending on the actual data: 

$ python3 sql_company_query.py 
fetchall:
(1, 'William', 'Shakespeare', 'm', None, '1961-10-25')
(2, 'Frank', 'Schiller', 'm', None, '1955-08-17')
(3, 'Bill', 'Windows', 'm', None, '1963-11-29')
(4, 'Esther', 'Wall', 'm', None, '1991-05-11')
(5, 'Jane', 'Thunder', 'f', None, '1989-03-14')

fetch one:
(1, 'William', 'Shakespeare', 'm', None, '1961-10-25')


MySQL

The module MySQLdb has to be installed,
which is quite easy under Debian or Ubuntu:
sudo apt-get install python-MySQLdb
Except the import and the parameters in the connect methods everything
else works exactly the same way as described
in the previous chapter on SQLite. Therefore it works like this:
import MySQLdb modul
Open a connection to the SQL server
Sending and receiving commands
Closing the connection to SQL
Importing and connecting looks like this:
import MySQLdb

connection = MySQLdb.connect (host = "localhost",
                              user = "testuser",
                              passwd = "testpass",
                              db = "company")


'''
#######################
