'''
Here the table models are defined using sqlalchemy by expanding the Base from database.py

models are defined as classes and columns as attributes
'''

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"  # This is used to define the table name

    id = Column(Integer, primary_key=True, nullable=False) # nullable=False means that is not Null
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="new")     # server_default is the default value
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  #this text will put in pgadmin the text inside (now()) so in this case to create the now() default value
    name = Column(String, nullable=False, server_default="New User")



# Define the Inventories table
class Data(Base):
    __tablename__ = 'datas'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  #this text will put in pgadmin the text inside (now()) so in this case to create the now() default value
    
    # Relationship to parent
    owner = relationship('Users')

    __table_args__ = (
        UniqueConstraint('name', 'owner_id', name='_name_owner_id_uc'),
    )


