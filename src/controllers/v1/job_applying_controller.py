from fastapi import APIRouter, Body,status
from models.user_applied_job import UserAppliedJob
from service.job_applying_service import apply_to_job

router = APIRouter()

# ---------------- Job Applying Endpoints ----------------
@router.post("/v1/jobs/apply", status_code=status.HTTP_201_CREATED)
async def apply_to_job(application: UserAppliedJob = Body(...)):
    await apply_to_job(application)