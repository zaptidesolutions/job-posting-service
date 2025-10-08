from fastapi import APIRouter, HTTPException, Body
from models.JobPosting import JobCreate, JobPosting
from bson import ObjectId
from config.db_config import freelance_db

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

@router.get("/v1/jobs/{job_id}", response_model=JobPosting)
async def get_job_by_id(job_id: str):
    job = await freelance_db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string
    job["_id"] = str(job["_id"])
    
    return JobPosting(**job)