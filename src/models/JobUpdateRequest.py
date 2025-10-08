from pydantic import BaseModel, Field
from typing import Optional

class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[float] = None
    is_active: Optional[bool] = None
    job_id: Optional[str] = Field(None, alias="_id")
    posted_by: Optional[str] = None