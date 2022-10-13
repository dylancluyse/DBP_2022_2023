# Functie dat een zoekterm en het aantal documenten als parameter opvraagt. Het resultaat zijn alle zoekresultaten.
from unittest import result

from pandas import isna



# Psychopg2
import psycopg2

print('(*’▽’)っ Initialization of PostgreSQL stuff')
conn = psycopg2.connect(database="resumes", user="postgres", password="admin", host="localhost", port="5432")
print('(*’▽’)っ Initialization complete')


# Late binding --> geen stored procedure nodig
def search_late(searchstring, limit):

    # 1. Je maakt de query aan door volgende zaken op te halen: naam + voornaam, titel en vervolgens twee bewerkingen rond FTS.
    # ts_rank(ts_document, query) as rank --> je gaat op basis van de index gaan kijken hoeveel voorkomens een woord heeft
    query = ''' select  lastname,
                        firstname,
                        title,
                        ts_rank(ts_document,query) as rank,
                        ts_headline('english', coalesce(title, '') || ' ' || COALESCE(resume, ''), query, 'MaxWords=7, MinWords=3, StartSel = [, StopSel = ], MaxFragments=7, FragmentDelimiter=...')
                from employee,to_tsquery('english',%s) query
                where query @@ ts_document
                order by rank desc 
                limit %s;
            '''
    cursor = conn.cursor()
    cursor.execute(query, (searchstring, limit))
    rows = cursor.fetchall()
    cursor.close()
    return rows


# Early binding --> stored procedure nodig.
def search_early(searchstring, limit):
    # 1. Je maakt de stored procedure 'candidates' aan. Je gebruikt altijd (), zelfs al heb je geen parameters. Hier zijn de parameters dezelfde als wat we gaan meegeven aan de python-functie: de zoekstring én de limiet.
    # 2. Je geeft de tabel terug als output. Je gebruikt met voorkeur niet dezelfde veldnamen zoals in de tabel worden gebruikt.
    # 3. Je specifieert de programmeertaal die je gaat gebruiken. Binnen deze cursus is enkel 'plpsql' te kennen.
    # 4. Je maakt de query aan door volgende zaken op te halen: naam + voornaam, titel, 
    ''' 
    create or replace function candidates(searchstring character varying, limit1 integer)
    returns table(emp_lastname character varying, emp_firstname character varying, emp_title character varying, emp_rank real, emp_headline text)
    language plpgsql
    as  $$
        begin
        return query 
		select  lastname,firstname,
                            title,
                            ts_rank(ts_document,query) as rank,
                            ts_headline('english', coalesce(title, '') || ' ' || COALESCE(resume, ''), query, 'MaxWords=7, MinWords=3, StartSel = [, StopSel = ], MaxFragments=7, FragmentDelimiter=...')
                    from employee,to_tsquery('english',searchstring) query
                    where query @@ ts_document
                    order by rank desc 
                    limit limit1;
        end;
        $$
    '''
    query = "SELECT * from candidates(%s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (searchstring, limit))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def printRows(rows):
    for row in rows:
        print('Lastname = ' + str(row[0])
        + ' | '  + 'Firstname = ' + str(row[1])
        + ' | '  + 'Title = ' + str(row[2])
        + ' | '  + 'Rank = ' + str(row[3]))
    print('')


# Applicatie:
print ('*** Late binding full text search ***')
rows = search_late("developer & (java|python)", 4)
printRows(rows)

print ('*** Early binding full text search ***')
rows = search_early("developer & (java|python)", 4)
printRows(rows)

conn.close()


## SQL Alchemy


# Imports
from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Initialisation
print('(*’▽’)っ Initialization of PostgreSQL stuff')
pg_engine = create_engine('postgresql://postgres:admin@localhost:5432/resumes')
pg_conn = pg_engine.connect()
metadata = MetaData(pg_engine)
print('(*’▽’)っ Initialization complete')

pg_Base = declarative_base(pg_engine) 
pg_Base.metadata.reflect(pg_engine)   

class PG_Employee(pg_Base):
    __table__ = pg_Base.metadata.tables['employee']
    
Session = sessionmaker(bind=pg_engine)
pg_session = Session()


def search_function_early(search_string, number_resulting_documents):
    print('(*’▽’)っ All Java or Python developers? Right away Chief! ')

    # Full-text
    results = pg_session.query(PG_Employee.employeeid, PG_Employee.firstname, PG_Employee.lastname, PG_Employee.resume.match(search_string)).all()
    
    for result in results:
        if result[3] == True:
            print(f'found {result[1]} {result[2]}')



def search_function_late(search_string, number_resulting_documents):
    print('(*’▽’)っ All Java or Python developers? Take it slow Chief! ')

    # Full-text
    results = pg_session.query(PG_Employee.resume.match(search_string)).all()
    print(results[0])





# Application
