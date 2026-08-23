from sqlalchemy import Column, Integer, String, Enum, Text,ForeignKey, DateTime

from sqlalchemy.sql import func
from app.db.database import Base

class Job(Base):
    __tablename__="jobs"
    
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(200),nullable=False)
    company=Column(String(200),nullable=False)
    location=Column(String(200),nullable=False)
    salary=Column(String(100),nullable=False)
    description=Column(Text,nullable=False)
    
    employer_id=Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
        
    created_at=Column(
        DateTime,
        nullable=False, 
        server_default=func.now()
        )
    