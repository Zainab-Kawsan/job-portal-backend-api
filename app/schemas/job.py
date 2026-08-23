from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    salary: str | None = None
    description: str
    requirements: str
    job_type: str


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: str | None
    description: str
    employer_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
class JobUpdate(BaseModel):
    title: str
    company: str
    location: str
    salary: str | None = None
    description: str
    
