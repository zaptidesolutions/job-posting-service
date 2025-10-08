from fastapi import APIRouter
from models.JobPosting import JobPosting
from service.job_searching_service import get_job

router = APIRouter()

# ---------------- Job Searching Endpoints ----------------
@router.get("/v1/jobs/{job_id}", response_model=JobPosting)
async def get_job_by_id(job_id: str):
    return await get_job(job_id)