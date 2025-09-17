from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Change to your own DB (MySQL, PostgreSQL, etc.)
# Example MySQL:
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/college_db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./college.db"  # For quick testing

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
