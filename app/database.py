'''
Database connection usin sqlalchemy
It create a local session to our database and also define a declarative_base() that will
be extended in the models.py to create our table models
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLACLHEMY_DATABASE_URL = 'postgresql://postgres:Ginopino96@127.0.0.1/simpleApp_Backend'

engine = create_engine(SQLACLHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """This method will create a connection to the database and yield.
    "db" can be used in other module to work with db

    Yields:
        _type_: the database connection
    """    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()