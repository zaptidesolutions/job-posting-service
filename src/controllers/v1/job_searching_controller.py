from fastapi import APIRouter, Query, HTTPException
from service.job_list_service import JobListService
from models.JobPosting import JobPosting
from bson import ObjectId
from models.JobInfo import JobInfo
from models.user_applied_job import UserAppliedJob
from config.db_config import freelance_db as db
from service.job_filtering_strategy.SkillJobFilter import SkillJobFilter
from service.job_filtering_strategy.RecentJobFilter import RecentJobFilter


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