'''
Here the table models are defined using sqlalchemy by expanding the Base from database.py

models are defined as classes and columns as attributes
'''

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.database import Base




# Define the Inventories table
class Data(Base):
    __tablename__ = 'datas'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))  #this text will put in pgadmin the text inside (now()) so in this case to create the now() default value
    


