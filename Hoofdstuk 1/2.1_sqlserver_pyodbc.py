######################################
# USE CASE: (DB xtreme) Find EmployeeID, LastName, FirstName and Salary from employees with 5 largest salaries lower than 40000. Order descending by salary. 
######################################

# Imports
import pyodbc  



######################################
# PyODBC with plain SQL 
######################################

# Dit is een vorm van early binding. De SQL-query wordt direct op de databank uitgevoerd. Dit kan je zien omdat er (onder andere) geen stored procedures aangesproken..

# 1. Verbinding aanmaken.
conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-1R9KU2AQ\MSSQLSERVER01;DATABASE=xtreme;Trusted_Connection=yes;')

# 2. Query volgens early binding aanmaken.
# We gebruiken voorlopig geen parameters. 
# We slaan de query hier op als een string. 
query = "SELECT TOP 5 employeeid,lastname,firstname,salary FROM employee WHERE salary < 40000 order by salary desc"

# 3. Je maakt een cursor aan met het object dat de verbinding bijhoudt 'conn'. Dit sla je op onder een ander object.
cursor = conn.cursor()

# 4. Je voert de query uit met de cursor. 
#    Alle rijen die voldoen aan de query kan je ophalen met de functie 'fetchall()'. 
#    De rijen worden als array opgeslaan met de bedoeling om ze later te doorlopen.
cursor.execute(query)
rows = cursor.fetchall()
print('')

# 5. Je verzorgt een mooie uitvoer door de array van rijen te gaan itereren. Iedere tabel kan opgehaald worden volgens hun respectievelijke volgorde.
#    Hier baseren we ons op de SELECT in de plaintekst-query. (lijn 22)
#    [0] zal employeeid zijn, [1] zal lastname zijn, etc.
print ('*** PyODBC with plain SQL ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))

# 6. We sluiten de cursor.
cursor.close()

# 7. We sluiten de verbinding.
conn.close()
    





######################################
# PyODBC with stored procedure call.
######################################

# Dit is een vorm van late binding. Er wordt eerst een SP aangesproken dat de data ophaalt.

# 1. Verbinding aanmaken.
conn = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-1R9KU2AQ\MSSQLSERVER01;DATABASE=xtreme;Trusted_Connection=yes;')

# 2. Stored Procedure aanmaken. Doe dit in SQL Server Management Studio. Rechtermuisklik op de databank en kies voor een nieuwe query.
#    OPM: Je krijgt gegarandeerd een foutmelding. Voeg de procedure toe in SQL Server Management Studio.
'''
In database xtreme: 
    create procedure Emps30000
    as
        SELECT TOP 5 employeeid,lastname,firstname,salary FROM employee WHERE salary < 40000 order by Salary desc
'''
# 3. Query aanmaken. Hier spreken we de SP aan om data op te halen. 
query = "exec Emps30000"

# 4. Je maakt een cursor aan met het object dat de verbinding bijhoudt 'conn'. Dit sla je op onder een ander object.
cursor = conn.cursor()

# 5. Je voert de query uit met de cursor. 
#    Alle rijen die voldoen aan de query kan je ophalen met de functie 'fetchall()'. 
#    De rijen worden als array opgeslaan met de bedoeling om ze later te doorlopen.
cursor.execute(query)
rows = cursor.fetchall()
print('')

# 6. Je verzorgt een mooie uitvoer door de array van rijen te gaan itereren. Iedere tabel kan opgehaald worden volgens hun respectievelijke volgorde.
#    Hier baseren we ons op de SELECT in de stored procedure. (lijn 67)
#    [0] zal employeeid zijn, [1] zal lastname zijn, etc.
print ('*** PyODBC with stored procedure ***')
for row in rows:
    print('ID = ' + str(row[0]) + ', '  + 'Name = ' + row[1] + ' ' + row[2] + ', salary = ' + str(row[3]))

# 7. Sluit de cursor af.
cursor.close()

# 8. Sluit de verbinding af.
conn.close()
