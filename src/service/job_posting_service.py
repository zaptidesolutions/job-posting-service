from config.db_config import freelance_db as db
from models.JobPosting import JobCreate, JobPosting
from fastapi import HTTPException, Body
from bson import ObjectId


async def add_job_post(job: JobCreate = Body(...)):
    existing_job = await db.jobs.find_one({"user_id": job.user_id, "title": job.title})
    
    if existing_job:
        raise HTTPException(status_code=400, detail="Job already exists")

    job_dict = job.dict()
    inserted_record = await db.jobs.insert_one(job_dict)
    
    # Convert ObjectId to string
    job_dict["_id"] = str(inserted_record.inserted_id)
    
    return JobPosting(**job_dict)

async def update_job_post(job_id: str, job_update: dict = Body(...)):
    existing_job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = {k: v for k, v in job_update.dict().items() if v is not None}
    
    if update_data:
        await db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})
    
    updated_job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    
    # Convert ObjectId to string
    updated_job["_id"] = str(updated_job["_id"])
    
    return JobPosting(**updated_job)