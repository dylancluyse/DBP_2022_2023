######################################
# SQL Alchemy ORM: exercise
# 0. Install PostgreSQL (including the client tool pgAdmin4) on your system (from https://www.postgresql.org/download/)
# 1. Create (using pgAdmin4) a database xtreme and the table Employee in PostgreSQL for the fields EmployeeID, LastName, FirstName, Title, BirthDate and Salary
# 2. Migrate the selected fields from the table Employee from MS-SQL Server to PostgreSQL
# 3. Add a column Resume to the table Employee in PostgresSQL
# 4. Import the csv file "resume.csv" (with fields EmployeeID, Title and Resume) into the new table. 
#    Overwrite the Title with the new value from the csv for each EmployeeID; 
######################################
# TIP: see LinkedIn learning course "Advanced Python: working with databaseses", section "Pythonic Postgres Interactions with SQLALchemy ORM"

# INITIALIZATION CODE

from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pandas import isna

print('### initialization of MS SQL Server stuff')
ms_engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
ms_conn = ms_engine.connect()
metadata = MetaData(ms_engine)  

ms_Base = declarative_base(ms_engine) # initialize Base class
ms_Base.metadata.reflect(ms_engine)   # get metadata from database

class MS_Employee(ms_Base):  # each table is a subclass from the Base class
    __table__ = ms_Base.metadata.tables['Employee']
    
Session = sessionmaker(bind=ms_engine)
ms_session = Session()

print('### initialization of PostgreSQL stuff')
pg_engine = create_engine('postgresql:///xtreme')
pg_conn = pg_engine.connect()
metadata = MetaData(pg_engine)  

pg_Base = declarative_base(pg_engine) # initialize Base class
pg_Base.metadata.reflect(pg_engine)   # get metadata from database

class PG_Employee(pg_Base):  # each table is a subclass from the Base class
    __table__ = pg_Base.metadata.tables['employee']
    
Session = sessionmaker(bind=pg_engine)
pg_session = Session()