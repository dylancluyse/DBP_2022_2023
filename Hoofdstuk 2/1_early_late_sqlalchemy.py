# Functie dat een zoekterm en het aantal documenten als parameter opvraagt. Het resultaat zijn alle zoekresultaten.
from types import NoneType
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




def search_early(search_string, number_resulting_documents):
    print('(*’▽’)っ All Java or Python developers? Right away Chief! ')

    pg_Base = declarative_base(pg_engine) 
    pg_Base.metadata.reflect(pg_engine)   

    emp_table = Table('employee', metadata, autoload=True, autoload_with=pg_engine)

    query = emp_table.select() \
            .with_only_columns([emp_table.c.lastname, emp_table.c.firstname, emp_table.c.title])\

    return pg_conn.execute(query)



def search_late(search_string, number_resulting_documents):
    print('(*’▽’)っ All Java or Python developers? Take it slow Chief! ')

    class PG_Employee(pg_Base):
        __table__ = pg_Base.metadata.tables['employee']
    
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()




def printRows(rows):
        for row in rows:
            print('Lastname = ' + str(row[0])
            + ' | '  + 'Firstname = ' + str(row[1])
            + ' | '  + 'Title = ' + str(row[2])
            #+ ' | '  + 'Rank = ' + str(row[3])
            )
        print('')




# Application
#print ('*** Late binding full text search ***')
#rows = search_late("developer & (java|python)", 4)
#printRows(rows)

print ('*** Early binding full text search ***')
rows = search_early("developer & (java|python)", 4)
printRows(rows)
