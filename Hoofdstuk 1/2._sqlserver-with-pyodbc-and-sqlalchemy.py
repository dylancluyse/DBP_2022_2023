######################################
# USE CASE: (DB xtreme) Find EmployeeID, LastName, FirstName and Salary from employees with 5 largest salaries lower than 40000. Order descending by salary. 
######################################
# See LinkedIn learning course "Advanced Python: working with databaseses"
#
######################################
# PyODBC with plain SQL 
######################################
'''
Check what ODBC drivers are installed on your PC by navigating to 
'Control Panel -> Administrative Tools -> Data Sources (ODBC)' and clicking on the 'Drivers' tab. 
You can also get to this ODBC Administrator window by running 'odbcad32.exe'. 
Be aware there are separate 32-bit and 64-bit versions of the ODBC Administrator.
'''
# execute "pip install pyodbc" from the OS prompt
import pyodbc  

# connect to database using Windows authentication (Trusted_Connection=yes)
conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-1R9KU2AQ\MSSQLSERVER01;DATABASE=xtreme;Trusted_Connection=yes;')

query = "SELECT TOP 5 employeeid,lastname,firstname,salary FROM employee WHERE salary < 40000 order by salary desc"
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
print('')
print ('*** PyODBC with plain SQL ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))
cursor.close()
conn.close()
    
######################################
# PyODBC with stored procedure call 
######################################
'''
In database xtreme: 
    create procedure Emps30000
    as
        SELECT TOP 5 employeeid,lastname,firstname,salary FROM employee WHERE salary < 40000 order by Salary desc
'''


conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-1R9KU2AQ\MSSQLSERVER01;DATABASE=xtreme;Trusted_Connection=yes;')
query = "exec Emps3s0000"
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
print('')
print ('*** PyODBC with stored procedure ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))
cursor.close()
conn.close()

######################################
# SQL Alchemy Core 
######################################
from sqlalchemy import create_engine  
from sqlalchemy import Table, MetaData, desc

engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')

conn = engine.connect()
metadata = MetaData(engine)  
emp_table = Table('Employee', metadata, autoload=True, autoload_with=engine)

query = emp_table.select() \
            .with_only_columns([emp_table.c.EmployeeID,emp_table.c.LastName,emp_table.c.FirstName,emp_table.c.Salary])\
            .where(emp_table.c.Salary < 40000)  \
            .order_by(desc("Salary")) \
            .limit(5)

rows = conn.execute(query)
print('')
print ('*** SQL Alchemy Core ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))
conn.close()   

######################################
# SQL Alchemy ORM 
######################################   

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
conn = engine.connect()
metadata = MetaData(engine)  

Base = declarative_base(engine) # initialize Base class
Base.metadata.reflect(engine)   # get metadata from database

class Employee(Base):  # each table is a subclass from the Base table
    __table__ = Base.metadata.tables['Employee']
    
Session = sessionmaker(bind=engine)
session = Session()

rows = session.query(Employee.EmployeeID,Employee.LastName,Employee.FirstName,Employee.Salary) \
                .where(Employee.Salary < 40000) \
                .order_by(Employee.Salary.desc()) \
                .limit(5)

print('')
print ('*** SQL Alchemy ORM ***')
for row in rows:
    print('ID = ' + str(row.EmployeeID) + ', '  + 'Name = ' + row.LastName + ' ' + row.FirstName + ', salary = ' + str(row.Salary))
conn.close()
print('')
    