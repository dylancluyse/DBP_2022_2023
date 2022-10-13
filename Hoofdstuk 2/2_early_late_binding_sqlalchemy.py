# Functie dat een zoekterm en het aantal documenten als parameter opvraagt. Het resultaat zijn alle zoekresultaten.
from unittest import result
from pandas import isna


######################################
# SQLalchemy
######################################

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
