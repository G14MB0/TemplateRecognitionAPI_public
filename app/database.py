'''
Database connection usin sqlalchemy
It create a local session to our database and also define a declarative_base() that will
be extended in the models.py to create our table models
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# Ottieni il percorso assoluto della directory dello script corrente
dir_path = os.path.dirname(os.path.abspath(__file__))
# Costruisci il percorso del database relativamente a quella directory
db_path = os.path.join(dir_path, 'DATABASE.db')

SQLALCHEMY_DATABASE_URL = f'sqlite:///{db_path}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """This method will create a connection to the database and yield.
    'db' can be used in other modules to work with db.

    Yields:
        _type_: the database connection
    """    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





#####################################
#   part to use with postgresql
#####################################
        
# SQLACLHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine = create_engine(SQLACLHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def get_db():
#     """This method will create a connection to the database and yield.
#     "db" can be used in other module to work with db

#     Yields:
#         _type_: the database connection
#     """    
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
