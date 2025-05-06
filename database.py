from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database setup
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:////app/offline_pos.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cache_sale(db, sale_data):
    from models import CachedSale
    cached_sale = CachedSale(
        user_id=sale_data["user_id"],
        customer_id=sale_data.get("customer_id"),
        total_amount=sale_data["total_amount"],
        payment_method=sale_data["payment_method"]
    )
    db.add(cached_sale)
    db.commit()
