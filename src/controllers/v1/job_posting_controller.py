from src.config.config_setup import freelance_db

from fastapi import APIRouter, HTTPException, Body
from models.JobPosting import JobCreate, JobPosting

router = APIRouter()

# ---------------- Job Posting Endpoints ----------------
@router.post("/v1/jobs", response_model=JobPosting)
async def create_job_posting(job: JobCreate = Body(...)):
    existing_job = await freelance_db.jobs.find_one({"job_id": job.job_id, "user_id": job.user_id})
    if existing_job:
        raise HTTPException(status_code=400, detail="Job with this job_id and user_id already exists")

    job_dict = job.dict()
    inserted_record = await freelance_db.jobs.insert_one(job_dict)
    
    # Convert ObjectId to string
    job_dict["_id"] = str(inserted_record.inserted_id)
    
    return JobPosting(**job_dict)
