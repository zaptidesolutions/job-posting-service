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
@router.get("/v1/jobs/search-by", response_model=list[JobInfo])
async def list_jobs(
    page: int = 1,
    page_size: int = 20,
    days: int = Query(7, description="Recent posts in last X days"),
    skills: list[str] = Query(None, description="Filter by required skills")
):
    if skills:
        strategy = SkillJobFilter(required_skills=skills)
    else:
        strategy = RecentJobFilter(days=days)

    jobs = await JobListService(db).get_jobs(strategy, page, page_size)
    return jobs

@router.get("/v1/jobs/{job_id}", response_model=JobPosting)
async def get_job_by_id(job_id: str):
    job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string
    job["_id"] = str(job["_id"])
    
    return JobPosting(**job)