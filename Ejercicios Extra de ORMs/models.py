from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'sqlalchemy'}

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    # Relationship
    addresses = relationship("Address", back_populates="user")
    cars = relationship("Car", back_populates="user")

class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'schema': 'sqlalchemy'}
    
    id = Column(Integer, primary_key=True)
    street = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)

    # FK, every address belongs to a user
    user_id = Column(Integer, ForeignKey('sqlalchemy.users.id'), nullable=False)
    user = relationship("User", back_populates="addresses")

class Car(Base):
    __tablename__ = 'cars'
    __table_args__ = {'schema': 'sqlalchemy'}

    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    manufacture_year = Column(Integer, nullable=False)

    # FK optional, cars can belong to a user, but not all cars have owners
    user_id = Column(Integer, ForeignKey('sqlalchemy.users.id'), nullable=True)
    user = relationship("User", back_populates="cars")