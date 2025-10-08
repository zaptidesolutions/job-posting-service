from fastapi import APIRouter, HTTPException, Body, status, Response
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

@router.patch("/v1/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_job_posting(job_id: str, job_update: JobUpdateRequest = Body(...)):
    await update_job_post(job_id, job_update)
