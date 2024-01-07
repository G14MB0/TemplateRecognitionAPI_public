'''
Here the table models are defined using sqlalchemy by expanding the Base from database.py

models are defined as classes and columns as attributes
'''

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
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

    # Relationships to children
    inventories = relationship("Inventories", cascade="delete, merge, save-update")


# Define the Inventories table
class Inventories(Base):
    __tablename__ = 'inventories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  #this text will put in pgadmin the text inside (now()) so in this case to create the now() default value

    # Relationships to parent
    # user = relationship('Users', back_populates='inventories')   # This create the fkey and the join capabilities to inventory.user

    # Relationship to children
    items = relationship('Items', cascade="delete, merge, save-update")
    items = relationship('Products', cascade="delete, merge, save-update")


# Define the Items table
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventories.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    estimated_arrival = Column(TIMESTAMP(timezone=True))
    tag = Column(String)
    quantity = Column(Numeric(13,4))
    measurement_unit = Column(String)
    cost = Column(Numeric(10,3))

    # Relationships
    # inventory = relationship('Inventories', cascade="delete, merge, save-update")
    items_mapping = relationship('Items_Product_Mapping', cascade="delete, merge, save-update")


# Define the Products table
class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventories.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    quantity = Column(Integer)
    tag = Column(String)
    selling_price = Column(Numeric(10,3))
    cost = Column(Numeric(10,3))

    # Relationships
    product_mapping = relationship('Items_Product_Mapping', cascade="delete, merge, save-update")


# Define the Items_Product_Mapping table
class Items_Product_Mapping(Base):
    __tablename__ = 'items_product_mapping'

    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    item_quantity = Column(Numeric(13,4), nullable=False)

    # Relationships
    # item = relationship('Items', back_populates='product_mapping')
    # product = relationship('Products', back_populates='item_mappings')


# # Define back_populates for Users and Inventories
# Users.inventories = relationship('Inventories', order_by=Inventories.id, back_populates='user')

# # Define back_populates for Products and Items_Product_Mapping
# Products.item_mappings = relationship('Items_Product_Mapping', back_populates='product')