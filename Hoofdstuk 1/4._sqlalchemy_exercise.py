######################################
# SQL Alchemy ORM: exercise
# 0. Install PostgreSQL (including the client tool pgAdmin4) on your system (from https://www.postgresql.org/download/).
# 1. Create (using pgAdmin4) a database xtreme and the table Employee in PostgreSQL for the fields EmployeeID, LastName, FirstName, Title, BirthDate and Salary.
# 2. Migrate the selected fields from the table Employee from MS-SQL Server to PostgreSQL.
# 3. Add a column Resume to the table Employee in PostgresSQL. Choose the appropriate data type for (long) textfields. 
# 4. Import the Excel file "resume.xlsx" (with fields EmployeeID, Title and Resume) into the new table (source: https://resumegenius.com). 
#    Overwrite the Title with the new value from the Excel for each EmployeeID; 
######################################
# TIP: see LinkedIn learning course "Advanced Python: working with databaseses", section "Pythonic Postgres Interactions with SQLALchemy ORM"

# INITIALIZATION CODE

from turtle import pd
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pandas import isna

# initialization of MS SQL Server stuff
ms_engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
ms_conn = ms_engine.connect()
metadata = MetaData(ms_engine)  
ms_Base = declarative_base(ms_engine) # initialize Base class
ms_Base.metadata.reflect(ms_engine)   # get metadata from database

class MS_Employee(ms_Base):  # each table is a subclass from the Ba#se class
    __table__ = ms_Base.metadata.tables['Employee']
    
Session = sessionmaker(bind=ms_engine)
ms_session = Session()

# initialization of PostgreSQL stuff
pg_engine = create_engine('postgresql://postgres:root@localhost/xtreme')
pg_conn = pg_engine.connect()
metadata = MetaData(pg_engine)  

pg_Base = declarative_base(pg_engine) # initialize Base class
pg_Base.metadata.reflect(pg_engine)   # get metadata from database

class PG_Employee(pg_Base):  # each table is a subclass from the Base class
    __table__ = pg_Base.metadata.tables['employee']
    
Session = sessionmaker(bind=pg_engine)
pg_session = Session()

num_rows_deleted = pg_session.query(PG_Employee).delete()
pg_session.commit()
print(f'{num_rows_deleted} rows deleted from table Employee')

emps = ms_session.query(MS_Employee.EmployeeID,MS_Employee.LastName,MS_Employee.FirstName,MS_Employee.Title,MS_Employee.BirthDate,MS_Employee.Salary)
print('')

for emp in emps:
        pg_emp = PG_Employee(employeeid=emp.EmployeeID, lastname=emp.LastName, firstname=emp.FirstName, title=emp.Title
        , birthdate=emp.BirthDate, salary=emp.Salary)
        pg_session.add(pg_emp)

pg_session.commit()
ms_conn.close()
ms_session.close()


## import excel file
import pandas as pd
xlsx = pd.ExcelFile("resumes.xlsx")
resumes = pd.read_excel(xlsx)
print(resumes)

for index,row in resumes.iterrows():
    emps = pg_session.query(PG_Employee).filter(PG_Employee.employeeid == row ['EmployeeID'])
    emp = emps[0]
    emp.title = row['Title']
    emp.resume = row['Resume']
    pg_session.commit()

pg_conn.close()
pg_session.close()