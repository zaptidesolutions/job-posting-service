# Assuming this structure in models.py:
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    user_id: str
    title: str
    description: str
    company: str
    location: str
    salary: Optional[float] = None
    posted_date: datetime
    is_active: bool = True

    class Config:
        validate_by_name = True


class JobPosting(JobCreate):
    job_id: str = Field(..., alias="_id")