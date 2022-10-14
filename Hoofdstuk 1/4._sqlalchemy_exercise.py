######################################
# SQL Alchemy ORM: exercise
# 0. Install PostgreSQL (including the client tool pgAdmin4) on your system (from https://www.postgresql.org/download/).
# 1. Create (using pgAdmin4) a database xtreme and the table Employee in PostgreSQL for the fields EmployeeID, LastName, FirstName, Title, BirthDate and Salary.
# 2. Migrate the selected fields from the table Employee from MS-SQL Server to PostgreSQL.
# 3. Add a column Resume to the table Employee in PostgresSQL. Choose the appropriate data type for (long) textfields. 
# 4. Import the Excel file "resume.xlsx" (with fields EmployeeID, Title and Resume) into the new table (source: https://resumegenius.com). 
#    Overwrite the Title with the new value from the Excel for each EmployeeID; 


# 1. DATAMODEL IN POSTGRESQL:
#  -- Table: xtreme.employee
'''
-- DROP TABLE IF EXISTS xtreme.employee;

CREATE TABLE IF NOT EXISTS xtreme.employee
(
    "employeeid" integer NOT NULL,
    "lastname" character varying(20) COLLATE pg_catalog."default",
    "firstname" character varying(10) COLLATE pg_catalog."default",
    "title" character varying(30) COLLATE pg_catalog."default",
    "birthdate" date,
    "salary" numeric(8,2),
    "resume" text COLLATE pg_catalog."default",
    CONSTRAINT employee_pkey PRIMARY KEY ("EmployeeID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS xtreme.employee
    OWNER to postgres;
'''

# Imports

from turtle import pd
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pandas import isna

# 2. Migrate the selected fields from the table Employee from MS SQL to PostgreSQL.
# Om een migratie uit te voeren moeten we eerst de data uit de MS SQL databank gaan halen.

# Opstarten van de MS SQL verbinding.
# 2.1 Maak een engine-object aan en start de verbinding op.
# 2.2 Maak een Base-object aan.
# 2.3 Maak een klasse aan voor de tabel dat je wilt ophalen.
# 2.4 Start een sessie op. Gebruik hiervoor het engine-object dat je net hebt aangemaakt.
ms_engine = create_engine('mssql+pyodbc://localhost\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
ms_conn = ms_engine.connect()
metadata = MetaData(ms_engine)

ms_Base = declarative_base(ms_engine)
ms_Base.metadata.reflect(ms_engine)

class MS_Employee(ms_Base):
    __table__ = ms_Base.metadata.tables['Employee']
    
Session = sessionmaker(bind=ms_engine)
ms_session = Session()

# Opstarten van de PostgreSQL verbinding.
# OPM: Zorg ervoor dat je MS SQL-objecten niet overschrijft. Deze heb je nog nodig!
# 2.5 Maak een engine-object aan en start de verbinding op.
# 2.6 Maak een Base-object aan.
# 2.7 Maak een klasse aan voor de tabel dat je wilt ophalen.
# 2.8 Start een sessie op. Gebruik hiervoor het engine-object dat je net hebt aangemaakt.
pg_engine = create_engine('postgresql://postgres:admin@localhost:5432/xtreme')
pg_conn = pg_engine.connect()
metadata = MetaData(pg_engine)  

pg_Base = declarative_base(pg_engine)
pg_Base.metadata.reflect(pg_engine)

class PG_Employee(pg_Base):
    __table__ = pg_Base.metadata.tables['employee']
    
Session = sessionmaker(bind=pg_engine)
pg_session = Session()


# 2.9 Zorg ervoor dat de Employee tabel in Postgres leeg is. Commit en voorzie uitvoer dat weergeeft hoeveel rijen er verwijderd zijn.
num_rows_deleted = pg_session.query(PG_Employee).delete()
pg_session.commit()
print(f'{num_rows_deleted} rows deleted from table Employee')

# 2.10 Voer de migratie uit. 
#    # Haal alle data uit de MS SQL databank en voer deze lijn per lijn in de Postgres databank. 
#    # Als je klaar bent met de migratie. Commit en sluit de MS SQL verbinding af. De Postgres verbinding heb je nog nodig.
emps = ms_session.query(MS_Employee.EmployeeID,MS_Employee.LastName,MS_Employee.FirstName,MS_Employee.Title,MS_Employee.BirthDate,MS_Employee.Salary)
print('')

for emp in emps:
        pg_emp = PG_Employee(employeeid=emp.EmployeeID, lastname=emp.LastName, firstname=emp.FirstName, title=emp.Title
        , birthdate=emp.BirthDate, salary=emp.Salary)
        pg_session.add(pg_emp)

pg_session.commit()
ms_conn.close()
ms_session.close()

# 3. Add a column Resume to the table Employee in PostgresSQL. Choose the appropriate data type for (long) textfields. 
"""
Dit doe je door in pgAdmin een nieuwe kolom toe te voegen. Manier via code: TODO
"""

# 4. Import Excel-file.
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