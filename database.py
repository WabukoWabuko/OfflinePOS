import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:////app/offline_pos.db"
print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")
print(f"File exists: {os.path.exists('/app/offline_pos.db')}")

# Ensure the file exists
if not os.path.exists('/app/offline_pos.db'):
    print("Creating offline_pos.db file...")
    open('/app/offline_pos.db', 'a').close()
    os.chmod('/app/offline_pos.db', 0o777)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        raise

def cache_sale(db, sale_data):
    """Cache a sale for offline use."""
    from models import CachedSale
    cached_sale = CachedSale(**sale_data)
    db.add(cached_sale)
    db.commit()
    print(f"Cached sale: {sale_data}")
