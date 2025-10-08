from fastapi import APIRouter, HTTPException, Body
from models.JobPosting import JobCreate, JobPosting
from models.JobUpdateRequest import JobUpdateRequest
from bson import ObjectId
from config.db_config import freelance_db as db
from service.job_posting_service import add_job_post, update_job_post

router = APIRouter()

# ---------------- Job Posting Endpoints ----------------
@router.post("/v1/jobs", response_model=JobPosting)
async def create_job_posting(job: JobCreate = Body(...)):
    return await add_job_post(job)

@router.patch("/v1/jobs/{job_id}")
async def update_job_posting(job_id: str, job_update: JobUpdateRequest = Body(...)):
    return await update_job_post(job_id, job_update)

@router.get("/v1/jobs/{job_id}", response_model=JobPosting)
async def get_job_by_id(job_id: str):
    job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string
    job["_id"] = str(job["_id"])
    
    return JobPosting(**job)