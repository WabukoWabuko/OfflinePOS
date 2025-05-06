from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    barcode = Column(String, unique=True)

class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    customer_id = Column(Integer)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

class SaleItem(Base):
    __tablename__ = "sale_items"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

class CachedSale(Base):
    __tablename__ = "cached_sales"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    customer_id = Column(Integer)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    synced = Column(Boolean, default=False)

class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:////app/offline_pos.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cache_sale(db, sale_data):
    cached_sale = CachedSale(
        user_id=sale_data["user_id"],
        customer_id=sale_data.get("customer_id"),
        total_amount=sale_data["total_amount"],
        payment_method=sale_data["payment_method"]
    )
    db.add(cached_sale)
    db.commit()
