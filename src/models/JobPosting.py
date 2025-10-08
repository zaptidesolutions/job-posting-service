# Assuming this structure in models.py:
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobCreate(BaseModel):
    job_id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    description: str
    company: str
    location: str
    salary: Optional[float] = None
    posted_date: datetime
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True


class JobPosting(JobCreate):
    job_id: str = Field(..., alias="_id")