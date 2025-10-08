from fastapi import HTTPException
from models.JobPosting import JobPosting
from bson import ObjectId
from config.db_config import freelance_db as db


async def get_job(job_id: str):
    job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string
    job["_id"] = str(job["_id"])
    
    return JobPosting(**job)