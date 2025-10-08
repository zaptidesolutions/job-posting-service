from fastapi import APIRouter, HTTPException
from models.JobPosting import JobPosting
from bson import ObjectId
from config.db_config import freelance_db as db


router = APIRouter()

# ---------------- Job Searching Endpoints ----------------
@router.get("/v1/jobs/{job_id:[0-9a-fA-F]{24}}", response_model=JobPosting)
async def get_job_by_id(job_id: str):
    job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string
    job["_id"] = str(job["_id"])
    
    return JobPosting(**job)