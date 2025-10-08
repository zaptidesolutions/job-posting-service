from pydantic import BaseModel, Field

class JobInfo(BaseModel):
    job_id: str = Field(..., alias="_id")
    title: str
    company: str
    location: str
    salary: float
    posted_by: str
    skills: list[str] = []

    class Config:
        validate_by_name = True