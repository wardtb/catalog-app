import datetime
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

''' Registered user information is stored in the User table '''

'''
    Columns:

    id - system-generated user ID, primary key for the User table
    name - user's name
    email - user's email address
'''

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)

''' Sporting Goods categories are stored in the Categories table '''

'''
    Columns:

    id - system-generated category ID, primary key for the Category table
    name - category name
'''
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name' : self.name,
        }

''' Sporting Goods items are stored in the Items table '''

'''
    Columns:

    id - system-generated category ID, primary key for the Item table
    name - item name provided by the user
    description - description of the item
    user_id - ID of the user who created the item
    category_id - ID of the category the item belongs to
    created_date - datetime stamp of when the item was created
'''

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer,primary_key=True)
    name = Column(String(250), nullable = False)
    description = Column(String(2000), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'category_id': self.category_id,
        }

engine = create_engine('postgresql:///catalog.db')

Base.metadata.create_all(engine)
