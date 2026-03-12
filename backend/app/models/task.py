from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Task(Base):
    """Defines SQL schema for the Task model."""
    __tablename__ = "tasks"  # Name of the table the class maps to
    id = Column(Integer, primary_key=True, index=True)  # PK adds a unique id, index creates a lookup table
    title = Column(String(200), nullable=False)  # Max 200 char strings, no null values allowed
    description = Column(Text, nullable=True) # Null values allowed
    status = Column(String(20), default="pending")  # Sets pending as the default status
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # db creates the timestamp (not Python)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # db creates the timestamp (not Python)