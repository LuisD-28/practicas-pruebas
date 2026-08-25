from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Date, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
SCHEMA_NAME = 'address_book'

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class LoginHistory(Base):
    __tablename__ = 'login_history'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.users.id'), nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    ip_address = Column(String(45), nullable=False)
    success = Column(Boolean, nullable=False)
