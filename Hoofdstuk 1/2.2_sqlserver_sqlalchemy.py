######################################
# USE CASE: (DB xtreme) Find EmployeeID, LastName, FirstName and Salary from employees with 5 largest salaries lower than 40000. Order descending by salary. 
######################################

# Imports
from sqlalchemy import create_engine  
from sqlalchemy import Table, MetaData, desc
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Algemene opmerkingen:
# -- Je werkt hier niet met een cursor!
# -- Je moet de naam van je MS SQL server aanpassen in de create_engine functie. 
#    Pas dit aan naar de naam van je systeem + sql server. 
#    Dit vindt je terug wanneer je SQL Server Management Studio opstart.
# -- Het parameteriseren van gegevens is toegankelijker vergeleken met psycobg2. 
#    Hier werk je met een syntax waar je zonder formatting de variabele (zoals een integer bij limit) kan ingeven.

######################################
# SQL Alchemy Core 
######################################

# Verschillen (TODO)
# Hier ga je expliciet moeten aangeven welk soort query je wilt uitvoeren. Bij de select-statement zal je 'with only ...' moeten meegeven.

# 1. Verbinding aanmaken.
engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
conn = engine.connect()
metadata = MetaData(engine)  

# 2. Tabel opslaan onder een variabele. Je slaat enkel de verwijzing op, niet data rechtstreeks uit de databank.
emp_table = Table('Employee', metadata, autoload=True, autoload_with=engine)

# 3. Je bouwt de query op met aparte functies. De query sla je op als een object van het type 'query'.
#    Eerst maak je een SELECT-statement aan. Je geeft met 'with only columns' mee welke kolommen je wilt meenemen in de select-statement.
#    In de where-clause wordt er hier gevraagd naar alle werknemers met een salaris groter dan 40000.
#    'Limit' en 'order by' komen overeen met de SQL-syntax.
query = emp_table.select() \
            .with_only_columns([emp_table.c.EmployeeID,emp_table.c.LastName,emp_table.c.FirstName,emp_table.c.Salary])\
            .where(emp_table.c.Salary < 40000)  \
            .order_by(desc("Salary")) \
            .limit(5)

# 4. Je voert de query uit door het mee te geven als parameter bij de execute-functie. 
#    De rijen worden bijgehouden als een array.
rows = conn.execute(query)
print('')

# 5. Om een mooi formaat te behouden maak je gebruik van foreach. 
#    Iedere rij ga je gaan aflopen en daaruit haal je de velden op. De velden worden in dezelfde volgorde opgeslaan zoals je ze uit de select haalt.
#    Voorbeeld: row[0] zal employeeID zijn, row[1] zal familienaam zijn, etc. 
print ('*** SQL Alchemy Core ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))


conn.close()   

######################################
# SQL Alchemy ORM 
######################################   

# 1. Verbinding aanmaken.
engine = create_engine('mssql+pyodbc://LAPTOP-1R9KU2AQ\MSSQLSERVER01/xtreme?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
conn = engine.connect()
metadata = MetaData(engine)  

# 1.2 Het aanmaken van de mapper.
# Het Base-object heb je nodig voor zometeen de klasse op te maken.
Base = declarative_base(engine)
Base.metadata.reflect(engine) 

# 2. De tabel sla je op onder een klasse. Je geeft hiermee het mapper-object mee (Base).
#    Het is mogelijk om meerdere klassen aan te maken. Een voorbeeld (dat niet gebruikt wordt) vindt je hieronder.
# -- Je geeft voorlopig één eigenschap mee: de naam van de tabel. 

class Employee(Base):
    __table__ = Base.metadata.tables['Employee']


#class Resumes(Base):
#    __table__ = Base.metadata.tables['Resumes']

# 3. Sessie aanmaken.
Session = sessionmaker(bind=engine)
session = Session()

# 4. Je bouwt de query op. Bij ORM moet je niet meer 'SELECT' en 'with_only' gebruiken. De query weet direct dat je te maken hebt met een select-statement. 
#    Je spreekt de klasse 'Employee' aan en je haalt hieruit ieder veld op dat je nodig hebt.
rows = session.query(Employee.EmployeeID,Employee.LastName,Employee.FirstName,Employee.Salary) \
                .where(Employee.Salary < 40000) \
                .order_by(Employee.Salary.desc()) \
                .limit(5)

# 6. Om een mooi formaat te behouden maak je gebruik van foreach. 
#    Iedere rij ga je gaan aflopen en daaruit haal je de velden op. De velden worden in dezelfde volgorde opgeslaan zoals je ze uit de select haalt.
#    Voorbeeld: row[0] zal employeeID zijn, row[1] zal familienaam zijn, etc. 
print ('*** SQL Alchemy ORM ***')
for row in rows:
    print('ID = ' + str(row.EmployeeID) + ', '  + 'Name = ' + row.LastName + ' ' + row.FirstName + ', salary = ' + str(row.Salary))

# 7. Verbinding afsluiten.
conn.close()