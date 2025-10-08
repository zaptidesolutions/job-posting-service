from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserAppliedJob(BaseModel):
    user_id: str
    job_id: str = Field(..., alias="_id")
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = None
    status: Optional[str] = "applied"  # e.g., applied, interviewed, hired, rejected

    class Config:
        validate_by_name = True