from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
SCHEMA_NAME = 'fruitsales'

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    invoices = relationship("Invoice", back_populates="user")

class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    entry_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    items = relationship("InvoiceItem", back_populates="product")

class Invoice(Base):
    __tablename__ = 'invoices'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.users.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="invoices")
    items = relationship("InvoiceItem", 
                        back_populates="invoice",
                        cascade="all, delete-orphan",# If an invoice is deleted, its items will also be deleted.
    )

class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    invoice_id = Column(
        Integer,
        ForeignKey(f"{SCHEMA_NAME}.invoices.id", ondelete="CASCADE"),
        nullable=False
    )    
    product_id = Column(
        Integer,
        ForeignKey(f"{SCHEMA_NAME}.products.id"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="items")