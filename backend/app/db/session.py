from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connection before using it
    echo=settings.DEBUG,  # Turns on debug mode, prints SQL queries to console
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Creates a class aka a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Registry of mapped Python classes to  their corresponding db tables
Base = declarative_base()

def get_db():
    """
    FastAPI dependency.
    Used before a route runs. Grabs a fresh db session and hands it to route. Closes session when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()